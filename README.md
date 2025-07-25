# Discord Voice Chat Notification Bot

A Discord bot that pings specified roles when someone joins an empty voice channel, inspired by Dan Petrolito's "Batsignal" concept.

## Features

- Notifies users with specific roles when someone joins an empty voice channel
- Self-role assignment via reaction to messages
- Only notifies on first person joining (prevents spam)
- Auto-deletes notifications after 5 minutes

## Discord Setup

### 1. Create Discord Application
1. Go to https://discord.com/developers/applications
2. Click "New Application" 
3. Name it (e.g., "Voice Chat Bot")

### 2. Create Bot
1. Click "Bot" in sidebar
2. Click "Add Bot"
3. Set "Public Bot" to true
4. Enable "Message Content Intent" and "Server Members Intent"
5. Copy the bot token (keep secure)

### 3. Generate Invite Link
1. Go to "OAuth2" → "URL Generator"
2. Check "bot" scope
3. Check permissions:
   - Send Messages
   - Read Message History  
   - Use Slash Commands
   - Manage Roles
   - View Channels
4. Use generated URL to invite bot to server

### 4. Server Configuration
1. Create role "Voice Chat Notifications" in Server Settings → Roles
2. Ensure bot's role is above this role in hierarchy
3. Post reaction message in rules channel
4. Get message ID (right-click → Copy Message ID, requires Developer Mode)

## Server Deployment

### 1. Setup Environment
```bash
python3 -m venv dcbot-env
source dcbot-env/bin/activate
pip install -r requirements.txt
```

### 2. Configuration Files

Create `.env`:
```
DISCORD_TOKEN=your_bot_token_here
```

Update `config.yaml` with your settings:
```yaml
notification_channel: "voice-chat-text"
ping_roles:
  - "Voice Chat Notifications"
reaction_message_id: your_message_id_here
reaction_roles:
  "🎤": "Voice Chat Notifications"
```

### 3. Run Bot

Test run:
```bash
python voicechat-bot.py
```

Background run:
```bash
nohup python voicechat-bot.py > bot.log 2>&1 &
```

## Files

- `voicechat-bot.py` - Main bot script
- `config.yaml` - Bot configuration
- `.env` - Environment variables (not in git)
- `requirements.txt` - Python dependencies
- `.gitignore` - Git ignore rules

## Usage

1. Users react 🎤 to designated message to get notifications
2. When someone joins empty voice channel, bot pings role members
3. Only first person joining triggers notification (prevents spam)

## Requirements

- Python 3.7+
- discord.py
- PyYAML  
- python-dotenv
