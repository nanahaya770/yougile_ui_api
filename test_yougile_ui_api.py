"""
UI-test для сайта yougile
с применением api
"""
from typing import Generator
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import pytest
import time
from selenium.webdriver.common.keys import Keys
import requests
from conftest import HEADERS, BASE_URL, LOGIN, PASSWORD
    

@pytest.fixture(scope='module')
def driver() -> Generator[WebDriver, None]:
    """
    Фикстура открывает браузер
    
    :return: Description
    :rtype: Generator[WebDriver, None, None]
    """
    service = ChromeService(ChromeDriverManager().install())
    driver: WebDriver = webdriver.Chrome(service=service)
    driver.implicitly_wait(10)
    driver.get("https://ru.yougile.com/team/")
    yield driver
    driver.quit()

def counter(driver):
    counter = driver.find_element(By.CSS_SELECTOR, 'div.text-12.leading-4.min-w-32')
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        counter
    )


def test_autorization(driver):
    login = driver.find_element(By.CSS_SELECTOR, 'form > div:nth-child(1) input')
    password = driver.find_element(By.CSS_SELECTOR, 'form > div:nth-child(2) input')

    login.send_keys(LOGIN)
    password.send_keys(PASSWORD)
    
    button_enter = driver.find_element(By.CSS_SELECTOR, 'form div.justify-center')
    button_enter.click()

    my_profile = driver.find_element(By.CSS_SELECTOR, 'div.truncate.ml-6.text-14.leading-4')
    assert my_profile.text == 'Мой профиль'
    
# TODO после добавления 1ой подзадачи, счетчик - 0/1
# TODO после добавления 100 подзадач, счетчик - 0/100
# TODO перевести подзадачи в статус - выполнено, -> 100/100

    """
     body создания задачи (в "subtasks" id ранее созданной задачи)
    {
  "title": "задача 2",
  "columnId": "9650c331-4a86-40be-b73f-01e36928a2e0",
  "subtasks": [
    "45f66fe6-037d-48d0-b068-85e78cc9e841"
  ]
}
    """

# TODO создать задачу, скопировать id, добавить в список "subtasks"


def test_create_subtask(driver):
    # переходим на страницу проекта
    driver.get("https://ru.yougile.com/team/941b14bd11e9/api-in-ui")
    
    # создаем задачи и записывает id задач в subtask_list
    subtask_list = []
    for num_subtask_id in range(1, 6):
        URL = f'{BASE_URL}/tasks'
        body = {
            "title": f"подзадача {num_subtask_id}"
        }
        response = requests.post(URL, headers=HEADERS, json=body)
        assert response.status_code == 201
        subtask_id = response.json()['id']
        subtask_list.append(subtask_id)
        print(num_subtask_id)
    
    # создаем задачи  и передаем список ранее созданных подзадач
    body_for_task = {
        "title": "задача 1",
        "columnId": "9650c331-4a86-40be-b73f-01e36928a2e0",
        "subtasks": subtask_list
    }
    response = requests.post(URL, headers=HEADERS, json=body_for_task)
    assert response.status_code == 201

    # проверяем счетчик
    counter = driver.find_element(By.CSS_SELECTOR, 'div.text-12.leading-4.min-w-32')
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        counter
    )
    time.sleep(0.2)
    assert counter.text == "0/5"
    time.sleep(3)
    
    # подзадачи переводим в статус - выполнено
    for subtask_id in subtask_list:
        URL = f'{BASE_URL}/tasks/{subtask_id}'
        body = {
            "completed": True
        }
        response = requests.put(URL, headers=HEADERS, json=body)
        assert response.status_code == 200

    time.sleep(2)

    # проверяем счетчик
    counter = driver.find_element(By.CSS_SELECTOR, 'div.text-12.leading-4.min-w-32')
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        counter
    )
    time.sleep(1)
    assert counter.text == "5/5"
    time.sleep(3)

    # TODO исправить test_check_counter - уже созданные подзадачи перевести в статус выполнено
    