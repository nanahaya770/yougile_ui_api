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

# фикстуры нужны для запуска кода
from fixtures import (
    driver,
    autorization,
    subtask_ids,
    create_task,
    completed_subtasks,
)


def get_counter(driver: WebDriver) -> WebElement:
    """
    Функция находит элемент счетчика, принимает driver,
    возвращает WebElement

    Args:
        driver (WebDriver): Экземпляр браузерного драйвера.

    Returns:
        WebElement: Элемент счётчика на странице.
    """
    counter = driver.find_element(
        By.CSS_SELECTOR, "div.text-12.leading-4.min-w-32"
    )
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", counter
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


def test_counter_completed_subtasks(
    driver: WebDriver, completed_subtasks: None
) -> None:
    """
    Тестовая функция проверяет счетчик выполненных подзадач,
    принимает driver и completed_subtasks

    Args:
        driver (WebDriver): Экземпляр браузерного драйвера.

        completed_subtasks (None):
        Фикстура, помечающая подзадачи как выполненные.

        Не используется внутри функции, предназначена для запуска
        фикстуры перед выполнением теста.

    Returns:
        None: Нет возвращаемого значения; содержит утверждения (assert).
    """
    driver.get("https://ru.yougile.com/team/941b14bd11e9/api-in-ui")
    counter = get_counter(driver)
    assert counter.text == COUNTER_COMPLETED, "счетчик работает не корректно"
