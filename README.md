# Point Bot

A Discord bot for managing points and rewards in your server.

## Setup

1. Clone this repository:
```bash
git clone https://github.com/vangauthic/point-bot.git
cd point-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Edit the `config.yml` file with your information (i.e.):
```
General:
    TOKEN: "YOUR_TOKEN_HERE"
    ACTIVITY: "watching" # playing, watching, listening
    DOING_ACTIVITY: "everyone" # what you want it to be playing, watching, listening, competing
    STATUS: "online" # online, idle, dnd, invisible

    ADMIN_GUILD_ID: YOUR_GUILD_ID_HERE
    LEADERBOARD_CHANNEL_ID: YOUR_CHANNEL_ID_HERE
    STAFF_ROLE_ID: YOUR_ROLE_ID_HERE
    STAFF_USERS: [STAFF_USER_1_ID, STAFF_USER_2_ID, STAFF_USER_3_ID]

DefaultStyles:
    EMBED_COLOR: "#7289DA"

PointRewards:
    MESSAGE: 1
    REACTION: 1
    VOICE: 1
    INVITE: 5
    DAILY: 20
```

4. Start the bot:
```bash
python main.py
```

## Features

### AUTOMATICALLY UPDATED LEADERBOARD
### POINT MANAGEMENT
### DAILY REWARDS
### EARN POINTS FOR SERVER INTERACTION
### TRANSLATE MESSAGES

## Commands

### Points Management
- `/points add @user <amount>` - Add points to a user
- `/points remove @user <amount>` - Remove points from a user

### Basic Commands
- `/help` - Displays helpful information about the bot
- `/claim` - Claim your daily points
- `/checkpoints` - Check your or another user's points
- `Translate` - Translate messages to another language

## Support

For issues and feature requests, please open an issue in the repository.
