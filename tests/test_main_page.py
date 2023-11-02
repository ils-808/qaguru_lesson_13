import allure
import pytest

from models.application_manager import app

value = [('asd',)]

#ToDo не доработал передачу параметра как paramitrize
@allure.title('Добавить дело в список')
@pytest.mark.parametrize(("arg",), value)
def test_add_item(arg):
    v = arg
    with allure.step('Открываем страницу'):
        app.main_page.open()
    with allure.step(f'Добавляем значение {v}'):
        app.main_page.add_todo(v)
    with allure.step(f'Проверить, что значение добавлено {v}'):
        app.main_page.check_value_exist(v)
