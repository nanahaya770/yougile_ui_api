import os
from dotenv import load_dotenv

load_dotenv()

LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")
TOKEN = os.getenv('TOKEN')
IMPLICITLY_WAIT = 10

TITLE = "задача 1"
COLUMN_ID= "9650c331-4a86-40be-b73f-01e36928a2e0"

NUMBER_OF_SUBTASKS = 100
COUNTER_SUBTASKS = f'0/{NUMBER_OF_SUBTASKS}'
COUNTER_COMPLETED = f'{NUMBER_OF_SUBTASKS}/{NUMBER_OF_SUBTASKS}'

BASE_URL = 'https://ru.yougile.com/api-v2'

HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}

MY_PROFILE_TEXT = 'Мой профиль'