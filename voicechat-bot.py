import discord
from discord.ext import commands
import yaml
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix='!', intents=intents)

def load_config():
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

@bot.event
async def on_ready():
    print(f'{bot.user} is ready!')

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return
    
    try:
        config = load_config()
        if payload.message_id == config['reaction_message_id']:
            guild = bot.get_guild(payload.guild_id)
            if not guild:
                print(f"Guild not found: {payload.guild_id}")
                return
                
            user = guild.get_member(payload.user_id)
            if not user:
                print(f"User not found: {payload.user_id}")
                return
            
            emoji_to_role = config['reaction_roles']
            if str(payload.emoji) in emoji_to_role:
                role_name = emoji_to_role[str(payload.emoji)]
                role = discord.utils.get(guild.roles, name=role_name)
                if not role:
                    print(f"Role '{role_name}' not found in guild {guild.name}")
                    return
                
                if role in user.roles:
                    print(f"User {user.display_name} already has role {role_name}")
                    return
                
                await user.add_roles(role)
                print(f"Added role '{role_name}' to {user.display_name}")
    except Exception as e:
        print(f"Error in on_raw_reaction_add: {e}")

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.user_id == bot.user.id:
        return
    
    try:
        config = load_config()
        if payload.message_id == config['reaction_message_id']:
            guild = bot.get_guild(payload.guild_id)
            if not guild:
                print(f"Guild not found: {payload.guild_id}")
                return
                
            user = guild.get_member(payload.user_id)
            if not user:
                print(f"User not found: {payload.user_id}")
                return
            
            emoji_to_role = config['reaction_roles']
            if str(payload.emoji) in emoji_to_role:
                role_name = emoji_to_role[str(payload.emoji)]
                role = discord.utils.get(guild.roles, name=role_name)
                if not role:
                    print(f"Role '{role_name}' not found in guild {guild.name}")
                    return
                
                if role not in user.roles:
                    print(f"User {user.display_name} doesn't have role {role_name}")
                    return
                
                await user.remove_roles(role)
                print(f"Removed role '{role_name}' from {user.display_name}")
    except Exception as e:
        print(f"Error in on_raw_reaction_remove: {e}")

@bot.event
async def on_voice_state_update(member, before, after):
    # Someone joined a voice channel
    if before.channel is None and after.channel is not None:
        try:
            voice_channel = after.channel
            
            # Check if channel was empty before this person joined (only non-bot users)
            current_members = [m for m in voice_channel.members if not m.bot]
            if len(current_members) == 1:  # Only the person who just joined
                config = load_config()
                guild = member.guild
                
                # Find notification channel
                text_channel = discord.utils.get(guild.text_channels, name=config['notification_channel'])
                if not text_channel:
                    if guild.text_channels:
                        text_channel = guild.text_channels[0]
                    else:
                        print(f"No text channels found in guild {guild.name}")
                        return
                
                # Build ping message
                role_mentions = []
                for role_name in config['ping_roles']:
                    role = discord.utils.get(guild.roles, name=role_name)
                    if role:
                        role_mentions.append(role.mention)
                    else:
                        print(f"Ping role '{role_name}' not found in guild {guild.name}")
                
                ping_text = " ".join(role_mentions) if role_mentions else ""
                message = f"{ping_text} 🎤 **{member.display_name}** started hanging out in **{voice_channel.name}**!"
                
                await text_channel.send(message, delete_after=300)
                print(f"Sent voice notification for {member.display_name} in {voice_channel.name}")
        except Exception as e:
            print(f"Error in on_voice_state_update: {e}")

bot.run(os.getenv('DISCORD_TOKEN'))
