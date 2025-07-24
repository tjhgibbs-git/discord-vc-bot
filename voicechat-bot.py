import discord
from discord.ext import commands
import yaml

intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True

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
    
    config = load_config()
    if payload.message_id == config['reaction_message_id']:
        guild = bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)
        
        emoji_to_role = config['reaction_roles']
        if str(payload.emoji) in emoji_to_role:
            role_name = emoji_to_role[str(payload.emoji)]
            role = discord.utils.get(guild.roles, name=role_name)
            if role:
                await user.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.user_id == bot.user.id:
        return
    
    config = load_config()
    if payload.message_id == config['reaction_message_id']:
        guild = bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)
        
        emoji_to_role = config['reaction_roles']
        if str(payload.emoji) in emoji_to_role:
            role_name = emoji_to_role[str(payload.emoji)]
            role = discord.utils.get(guild.roles, name=role_name)
            if role:
                await user.remove_roles(role)

@bot.event
async def on_voice_state_update(member, before, after):
    # Someone joined a voice channel
    if before.channel is None and after.channel is not None:
        voice_channel = after.channel
        
        # Check if channel was empty before this person joined (only non-bot users)
        current_members = [m for m in voice_channel.members if not m.bot]
        if len(current_members) == 1:  # Only the person who just joined
            config = load_config()
            guild = member.guild
            
            # Find notification channel
            text_channel = discord.utils.get(guild.text_channels, name=config['notification_channel'])
            if not text_channel:
                text_channel = guild.text_channels[0]
            
            # Build ping message
            role_mentions = []
            for role_name in config['ping_roles']:
                role = discord.utils.get(guild.roles, name=role_name)
                if role:
                    role_mentions.append(role.mention)
            
            ping_text = " ".join(role_mentions) if role_mentions else ""
            message = f"{ping_text} 🎤 **{member.display_name}** started hanging out in **{voice_channel.name}**!"
            
            await text_channel.send(message, delete_after=300)

bot.run('YOUR_BOT_TOKEN_HERE')
