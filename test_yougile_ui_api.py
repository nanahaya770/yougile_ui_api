"""
UI‑тест для yougile:
Создаёт через API несколько подзадач и основную задачу с ними,
выполняет вход в интерфейс и проверяет счётчик подзадач на странице
до и после пометки подзадач как выполненных.
"""

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import pytest
import requests
from conftest import COUNTER_SUBTASKS, COUNTER_COMPLETED
from fixtures import (
    driver,
    autorization,
    subtask_ids,
    create_task,
    completed_subtasks
)

    



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

    # Импорты (добавьте в начало файла вместе с остальными импортами)





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
V декомпозиция, структурировать код(разделить на тестовые, фикстуры, на функции, на классы, на модули, на пакеты, библиотеки)
V все константы перенести в conftest 
V все секретные данные перенести в .env
- V указать type hints в определении функций (запустить mypy - лучше в конце)
V написать справку в виде DocString 
создание файла readme с кратким описанием проекта --start
привести в соответствии с pep8 - лучше в конце
по необходимости использовать allure(если работодатель требует, чаще allure размывает код)
V использовать git
интеграция тестов CI/CD (в основном это задача devops)
"""