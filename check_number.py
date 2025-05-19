from telethon.sync import TelegramClient
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.functions.contacts import DeleteContactsRequest
from telethon.tl.types import InputPhoneContact
import os

# Replace these with your actual credentials
API_ID = 28484734
API_HASH = 'b4931c4a7ea9c22b3cc72a725c6c0276'
USER_PHONE = '+989034521723'  # Used only on first login

# === Input file ===
INPUT_FILE = 'numbers.txt'  # one number per line, e.g. +1234567890

# === Output files ===
HAS_TELEGRAM_FILE = 'has_telegram.txt'
NO_TELEGRAM_FILE = 'no_telegram.txt'

def read_numbers(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip().startswith('+')]

def write_list(file_path, data):
    with open(file_path, 'w') as f:
        f.write('\n'.join(data))



def check_numbers(numbers):
    with TelegramClient("session", API_ID, API_HASH) as client:
        contacts = [
            InputPhoneContact(client_id=i, phone=number, first_name="Temp", last_name="")
            for i, number in enumerate(numbers)
        ]
        result = client(ImportContactsRequest(contacts))

        found_ids = {contact.client_id for contact in result.imported}
        has_telegram = [numbers[i] for i in found_ids]
        no_telegram = [num for i, num in enumerate(numbers) if i not in found_ids]

        # --- Delete all imported users to clean up contact list ---
        users_to_delete = result.users  # users = list of User objects
        if users_to_delete:
            client(DeleteContactsRequest(id=[user.id for user in users_to_delete]))

        return has_telegram, no_telegram

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Input file '{INPUT_FILE}' not found.")
        return

    print("📥 Reading numbers...")
    numbers = read_numbers(INPUT_FILE)

    if not numbers:
        print("❌ No valid numbers found.")
        return

    print(f"🔍 Checking {len(numbers)} numbers via Telethon...")
    has_telegram, no_telegram = check_numbers(numbers)

    print(f"✅ {len(has_telegram)} numbers found on Telegram.")
    print(f"❌ {len(no_telegram)} numbers not found.")

    write_list(HAS_TELEGRAM_FILE, has_telegram)
    write_list(NO_TELEGRAM_FILE, no_telegram)

    print(f"📁 Results written to '{HAS_TELEGRAM_FILE}' and '{NO_TELEGRAM_FILE}'")

if __name__ == '__main__':
    main()
