import os
from dotenv import load_dotenv

load_dotenv()

LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")
TOKEN = os.getenv('TOKEN')

BASE_URL = 'https://ru.yougile.com/api-v2'

HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}

MY_PROFILE_TEXT = 'Мой профиль'