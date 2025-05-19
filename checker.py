from telethon.sync import TelegramClient
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.functions.contacts import DeleteContactsRequest
from telethon.tl.types import InputPhoneContact
import os

API_ID = YOUR_API_ID
API_HASH = 'YOUR_API_HASH'
USER_PHONE = 'YOUR_PHONE_NUMBER'  # Used only on first login


# This function accepts a list of phone numbers and returns two lists

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
