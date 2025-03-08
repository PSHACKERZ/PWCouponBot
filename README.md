# PW Coupon Bot

A Telegram bot that provides coupon codes for Physics Wallah (PW) batches to users who join a specific Telegram channel.

## Features

- Verifies if users have joined the required Telegram channel
- Provides coupon codes for different PW batches (Class 9, 10, 11, 12, JEE, NEET)
- User-friendly interface with buttons for easy navigation

## Setup Instructions

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables**

   Edit the `.env` file with your specific details:
   
   - `BOT_TOKEN`: Your Telegram bot token (from BotFather)
   - `CHANNEL_ID`: The username or ID of your Telegram channel (e.g., @yourchannel)
   - `CHANNEL_LINK`: The invite link to your Telegram channel

3. **Update coupon codes**

   Edit the `coupon_codes` dictionary in `bot.py` to include your actual coupon codes.

4. **Run the bot**

   ```bash
   python bot.py
   ```

## Deployment

For continuous availability, deploy the bot on a server:

### Using a VPS or Cloud Service

1. Set up a virtual machine on a cloud provider (AWS, DigitalOcean, etc.)
2. Clone this repository to the server
3. Install dependencies and configure environment variables
4. Use a process manager like PM2 or Supervisor to keep the bot running:

   ```bash
   # Using PM2
   npm install pm2 -g
   pm2 start bot.py --name pw-coupon-bot --interpreter python3
   ```

### Using PythonAnywhere or Heroku

Follow the platform-specific deployment instructions for Python applications.

## Bot Usage

1. Users start the bot with `/start`
2. If not a channel member, they're prompted to join
3. After joining, they select their batch
4. The bot provides the corresponding coupon code

## Customization

- Add more batches and coupon codes in the `coupon_codes` dictionary
- Modify the messages to suit your needs
- Add additional features like admin commands to update coupon codes 