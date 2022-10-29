# Slack Pings Bot

### Requirements

1. Python 3.10+ https://www.python.org/downloads/

### Creating the bot on Slack

1. Go to https://api.slack.com/
2. Log into your account. You may be redirected to another page. Please return to the page above if redirected after logging in
3. Click on Create a new App
4. Choose from Manifest
5. Choose JSON
6. Copy all the contents in the manifest.json file inside this folder and paste it there
7. Create bot
8. Install bot in your workspace. Copy the bot token and paste it inside of the quotation marks in the SLACK_BOT_TOKEN variable in the `settings.json` file
9. Copy the app token and paste it inside of the quotation marks in the SLACK_APP_TOKEN variable in the `settings.json` file.

### Installation

1. Extract the zip onto a folder
2. Open terminal or CMD and cd onto the folder. (If you're on mac just drag the folder to the terminal!)
3. Rename `sample_settings.json` to `settings.json`
3. Run `python3 main.py` or `py main.py`
4. The bot is running!
