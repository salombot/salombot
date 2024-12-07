from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import logging
import requests
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv('token')



# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user = message.from_user
    name = user.full_name

    # Ask for phone number
    phone_button = KeyboardButton("📱 Share Phone Number", request_contact=True)
    phone_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(phone_button)

    await message.answer(
        f"Hi {name}! Please share your phone number:",
        reply_markup=phone_keyboard
    )


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def handle_contact(message: types.Message):
    contact = message.contact
    user_id = contact.user_id
    phone_number = contact.phone_number
    name = message.from_user.full_name

    # API URL
    url = os.getenv('url') # Fixed the double slash

    # Prepare the data
    data = {
        'name': name,
        'user_id': user_id,
        'phone_number': phone_number  # Fixed the key
    }

    # Send data to the API
    try:
        response = requests.post(url, json=data)
        if response.status_code == 201:  # Assuming your API returns 201 for success
            await message.answer(
                "Thank you! Your data has been saved successfully.",
                reply_markup=types.ReplyKeyboardRemove()
            )
        else:
            await message.answer(
                f"An error occurred: {response.status_code} {response.text}",
                reply_markup=types.ReplyKeyboardRemove()
            )
    except requests.RequestException as e:
        await message.answer(
            f"Failed to save your data due to a server error: {e}",
            reply_markup=types.ReplyKeyboardRemove()
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
