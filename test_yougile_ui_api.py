"""
UI‑тест для yougile:
Создаёт через API несколько подзадач и основную задачу с ними,
выполняет вход в интерфейс и проверяет счётчик подзадач на странице
до и после пометки подзадач как выполненных.
"""

from typing import Generator
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
import pytest
import requests
from conftest import (
    HEADERS, 
    BASE_URL, 
    LOGIN, 
    PASSWORD, 
    MY_PROFILE_TEXT, 
    IMPLICITLY_WAIT,
    NUMBER_OF_SUBTASKS,
    TITLE,
    COLUMN_ID,
    COUNTER_SUBTASKS,
    COUNTER_COMPLETED
)
    

@pytest.fixture(scope='module', autouse=True)
def driver() -> Generator[WebDriver, None]:
    """Фикстура открывает браузер, возвращает driver

    Args:
        None

    Returns:
        Generator[WebDriver, None]: Объект драйвера для браузера
    """
    service = ChromeService(ChromeDriverManager().install())
    browser: WebDriver = webdriver.Chrome(service=service)
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
def subtask_ids() -> Generator[list[str], None]:
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
    response = requests.post(URL, headers=HEADERS, json=body_for_task)
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


def get_counter(driver: WebDriver) -> WebElement:
    """Функция находит элемент счетчика, принимает driver, возвращает WebElement

    Args:
        driver (WebDriver): Экземпляр браузерного драйвера.

    Returns:
        WebElement: Элемент счётчика на странице.
    """
    counter = driver.find_element(By.CSS_SELECTOR, 'div.text-12.leading-4.min-w-32')
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        counter
    )
    return counter


def test_counter_of_new_subtasks(driver: WebDriver) -> None:
    """Тестовая функция проверяет счетчик новых подзадач, принимает driver

    Args:
        driver (WebDriver): Экземпляр браузерного драйвера.

    Returns:
        None: Нет возвращаемого значения; содержит утверждения (assert).
    """
    driver.get("https://ru.yougile.com/team/941b14bd11e9/api-in-ui")
    counter = get_counter(driver)
    assert counter.text == COUNTER_SUBTASKS, "счетчик работает некорректно"


def test_counter_completed_subtasks(driver: WebDriver, completed_subtasks: None) -> None:
    """Тестовая функция проверяет счетчик выполненных подзадач, принимает driver и completed_subtasks

    Args:
        driver (WebDriver): Экземпляр браузерного драйвера.
        completed_subtasks (None): Фикстура, помечающая подзадачи как выполненные. Не используется внутри функции, предназначена для запуска фикстуры перед выполнением теста.

    Returns:
        None: Нет возвращаемого значения; содержит утверждения (assert).
    """
    driver.get("https://ru.yougile.com/team/941b14bd11e9/api-in-ui")
    counter = get_counter(driver)
    assert counter.text == COUNTER_COMPLETED, "счетчик работает не корректно"


"""
ВАЖНО!!! прописать шаги как для ручного тестирования!!!
Автоматизировать повторяющие шаги
Стратегические шаги не должны быть автоматизированы
указывать типы данных(type hints) в определении функции аргументам и что функция возвращает
запустить mypy, это поможет избежать неявные ошибки

1.Открытие браузера - фикстура, область действия - модуль
2.Авторизация UI - фикстура, область действия - модуль
3.Создать 5 задач с помошью API, и получить список их id - фикстура, область действия - модуль
4.Создать основную задачу с помошью API, с 5ю задачами из 3его пункта - фикстура, область действия - модуль
5.Тест счетчика 0/5 UI - тестовая функция 
6.Перевести подзадачи в статус выполнено с помошью API - фикстура, область действия - функция(по умолчанию)
7.Тест счетчика 5/5 UI - тестовая функция
8.удаление основной задачи и подзадач

"""

"""
TODO
V соблюдать грамотный naming(название)
? декомпозиция, структурировать код(разделить на тестовые, фикстуры, на функции, на классы, на модули, на пакеты, библиотеки)
V все константы перенести в conftest --start
V все секретные данные перенести в .env
- V указать type hints в определении функций (запустить mypy)
V написать справку в виде DocString 
создание файла readme с кратким описанием проекта 
привести в соответствии с pep8
по необходимости использовать allure(если работодатель требует, чаще allure размывает код)
использовать git
интеграция тестов CI/CD (в основном это задача devops)
"""