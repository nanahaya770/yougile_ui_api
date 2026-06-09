from typing import Generator
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver 
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import pytest
import requests
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from conftest import (
    HEADERS, 
    BASE_URL, 
    LOGIN, 
    PASSWORD, 
    MY_PROFILE_TEXT, 
    IMPLICITLY_WAIT,
    NUMBER_OF_SUBTASKS,
    TITLE,
    COLUMN_ID
)


@pytest.fixture(params=["edge", "firefox", "chrome"], scope="module", autouse=True)
def driver(request) -> Generator[WebDriver, None, None]:
    browser: WebDriver
    if request.param == "edge":
        service_1 = EdgeService(EdgeChromiumDriverManager().install())
        browser = webdriver.Edge(service=service_1)
    elif request.param == "firefox":
        service_2 = FirefoxService(GeckoDriverManager().install())
        browser = webdriver.Firefox(service=service_2)
    else:
        service_3 = ChromeService(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service_3)
    browser.implicitly_wait(IMPLICITLY_WAIT)
    yield browser
    browser.quit()


@pytest.fixture(scope='module', autouse=True)
def autorization(driver: WebDriver) -> None:
    """Фикстура выполняет авторизацию на сайте yougile, принимает driver

    Args:
        driver (WebDriver): Экземпляр браузерного драйвера.

    Returns:
        None: Нет возвращаемого значения, выполняет действия в браузере.
    """
    driver.get("https://ru.yougile.com/team/")
    login = driver.find_element(By.CSS_SELECTOR, 'form > div:nth-child(1) input')
    password = driver.find_element(By.CSS_SELECTOR, 'form > div:nth-child(2) input')

    assert type(LOGIN) == str, "логин не загрузился"
    assert type(PASSWORD) == str, "пароль не загрузился"
    login.send_keys(LOGIN)
    password.send_keys(PASSWORD)
    
    button_enter = driver.find_element(By.CSS_SELECTOR, 'form div.justify-center')
    button_enter.click()

    my_profile = driver.find_element(By.CSS_SELECTOR, 'div.truncate.ml-6.text-14.leading-4')
    assert my_profile.text == MY_PROFILE_TEXT, "не произошел переход на страницу личного кабинета"


@pytest.fixture(scope='module', autouse=True)
def subtask_ids(driver: WebDriver) -> Generator[list[str], None, None]:
    """Создаёт подзадачи, возвращает список id подзадач

    Args:
        None

    Returns:
        Generator[list[str], None]: Генератор, дающий список идентификаторов созданных подзадач.
    """
    subtask_list = []
    URL = f'{BASE_URL}/tasks'
    for num_subtask_id in range(1, NUMBER_OF_SUBTASKS + 1):
        body = {
            "title": f"подзадача {num_subtask_id}"
        }
        response = requests.post(URL, headers=HEADERS, json=body)
        subtask_id = response.json()['id']
        subtask_list.append(subtask_id)
    yield subtask_list
    for subtask_id in subtask_list:
        URL = f'{BASE_URL}/tasks/{subtask_id}'
        body_for_del = {
            "deleted": True
        }
        response = requests.put(URL, headers=HEADERS, json=body_for_del)
        assert response.status_code == 200, f'подзадача {subtask_id} не удалена'


@pytest.fixture(scope='module', autouse=True)
def create_task(subtask_ids: Generator[list[str], None]) -> Generator[None, None]:
    """Фикстура создаёт основную задачу с подзадачами и удаляет её по завершении, принимает список подзадач

    Args:
        subtask_ids (Generator[list[str], None]): Генератор со списком id подзадач.

    Returns:
        Generator[None, None]: Генератор без значения; ресурс удаляется в teardown.
    """
    URL = f'{BASE_URL}/tasks'
    body_for_task = {
        "title": TITLE,
        "columnId": COLUMN_ID,
        "subtasks": subtask_ids
    }
    response = requests.post(URL, headers=HEADERS, data=body_for_task)
    task_id = response.json()['id']
    yield 
    URL = f'{BASE_URL}/tasks/{task_id}'
    body = {
            "deleted": True
        }
    response = requests.put(URL, headers=HEADERS, json=body)
    assert response.status_code == 200, "основная задача не удалена"
    

@pytest.fixture
def completed_subtasks(subtask_ids: Generator[list[str], None]) -> None:
    """Фикстура переводит подзадачи в статус выполнено, принимает фикстуру subtask_ids

    Args:
        subtask_ids (Generator[list[str], None]): Генератор со списком id подзадач.

    Returns:
        None: Нет возвращаемого значения; изменяет статус подзадач через API.
    """
    for subtask_id in subtask_ids:
        URL = f'{BASE_URL}/tasks/{subtask_id}'
        body = {
            "completed": True
        }
        response = requests.put(URL, headers=HEADERS, json=body)
        assert response.status_code == 200, "подзадача не переведена в статус - выполнено"

