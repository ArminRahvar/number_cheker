import requests
import time
import os
from checker import check_numbers

BOT_TOKEN = "5854476610:AAEkH7Xoz5p7-TjDNQGtbLytpHriaUQKObQ"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
FILE_URL = f"https://api.telegram.org/file/bot{BOT_TOKEN}"

OFFSET = 0  # Used for polling

def get_updates(offset):
    url = f"{BASE_URL}/getUpdates?timeout=100&offset={offset}"
    response = requests.get(url)
    return response.json()

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, data=payload)

def download_file(file_id, filename):
    file_info = requests.get(f"{BASE_URL}/getFile?file_id={file_id}").json()
    file_path = file_info['result']['file_path']
    file_content = requests.get(f"{FILE_URL}/{file_path}").content

    with open(filename, 'wb') as f:
        f.write(file_content)
    return filename

def handle_text_file(chat_id, file_id):
    tmp_path = download_file(file_id, f"/tmp/numbers.txt")

    # Read phone numbers from file
    with open(tmp_path, 'r') as f:
        numbers = [line.strip() for line in f if line.strip().startswith('+')]

    has_telegram, no_telegram = check_numbers(numbers)

    msg = (
        f"✅ Found on Telegram ({len(has_telegram)}):\n" +
        "\n".join(has_telegram[:50]) + "\n\n" +
        f"❌ Not Found ({len(no_telegram)}):\n" +
        "\n".join(no_telegram[:50])
    )
    send_message(chat_id, msg)

def main():
    global OFFSET
    print("Bot is running...")

    while True:
        updates = get_updates(OFFSET)

        if 'result' in updates:
            for update in updates['result']:
                OFFSET = update['update_id'] + 1

                if 'message' in update:
                    message = update['message']
                    chat_id = message['chat']['id']

                    if 'document' in message:
                        document = message['document']
                        file_name = document['file_name']
                        file_id = document['file_id']

                        if file_name.endswith('.txt'):
                            send_message(chat_id, "Processing your file...")
                            handle_text_file(chat_id, file_id)
                        else:
                            send_message(chat_id, "Please upload a .txt file with phone numbers.")

                    elif 'text' in message and message['text'] == '/start':
                        send_message(chat_id, "Send me a .txt file with phone numbers (one per line).")

        time.sleep(1)

if __name__ == '__main__':
    main()
