# number_cheker
telegram bot that checks a list of number that has telegram or not
# Telegram Phone Number Checker Bot

This is a Telegram bot that allows users to upload a `.txt` file containing phone numbers (one per line), and it checks which numbers are registered on Telegram.

## Features

- Users can send a `.txt` file with phone numbers.
- The bot processes the file and checks each number using Telegram's API.
- It replies with a list of numbers found and not found on Telegram.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/telegram-checker-bot.git
cd telegram-checker-bot
```

## 2. Install Dependencies
Ensure you have Python 3 installed, and install required libraries:

```bash
pip install -r requirements.txt
```
## 3. Add Your Credentials
bot.py
Open bot.py and replace the placeholder with your actual Telegram bot token:

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

checker.py
Open checker.py and add your Telegram API credentials:

API_ID = 'YOUR_API_ID'
API_HASH = 'YOUR_API_HASH'
USER_PHONE = '+YOUR_PHONE_NUMBER'
You can obtain your API_ID and API_HASH by logging into my.telegram.org.

## How to Use
Start the bot via your terminal:

```bash
python bot.py
```
Open Telegram and search for your bot.

Send the /start command to initiate.

Upload a .txt file containing phone numbers (one per line, in international format starting with +).

The bot will respond with which numbers are on Telegram and which are not.

## Example Input File
```bash
+1234567890
+1987654321
+441234567890
```

## 🧾 Standalone Script: number_checker.py
 - You can also use the number_checker.py script independently to check phone numbers from a local file.

## 🔧 How to Use
Create a file named numbers.txt in the project root. Each line should contain one phone number, starting with +.

## Run the script:
```bash
python number_checker.py
```

- After processing, it will generate:

has_telegram.txt — Numbers found on Telegram.

no_telegram.txt — Numbers not found on Telegram.