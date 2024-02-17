import functools
from datetime import timedelta, date

import pytest
import time
import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager

# библиотеки для скачивания драйверов браузеров


class Site:
    # проверка на то какой браузер используется в тесте
    def __init__(self, browser, address):
        self.address = address
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(testdata['sleep_time'])
        self.driver.maximize_window()
        self.driver.get(address)
        self.browser = browser
        time.sleep(testdata["sleep_time"])
        self.address = address

    def registration_on_the_website(self):
        x_selector1 = """//*[@id="login"]/div[1]/label/input"""  # вводим Username
        input1 = self.find_element("xpath", x_selector1)
        input1.send_keys(username)

        x_selector2 = """//*[@id="login"]/div[2]/label/input"""  # вводим passwd
        input2 = self.find_element("xpath", x_selector2)
        input2.send_keys(passwd)

        btn_selector = "button"
        btn = self.find_element("css", btn_selector)
        btn.click()


    def find_element(self, mode, path):
        print(f'find element, {mode} = {path}')
        if mode == "css":
            element = self.driver.find_element(By.CSS_SELECTOR, path)
        elif mode == "xpath":
            element = self.driver.find_element(By.XPATH, path)
        else:
            element = None
        return element

    def get_element_property(self, mode, path, property):
        element = self.find_element(mode, path)
        return element.value_of_css_property(property)

    def go_to_site(self):
        return self.driver.get(self.address)

    def close(self):
        self.driver.close()


# файл конфигурации теста
with open("./testdata.yaml") as f:
    testdata = yaml.safe_load(f)
    browser = testdata["browser"]
    username = testdata['user_name']
    passwd = testdata['passwd']
    addres = testdata['addres']
    # site = Site(testdata["browser"],testdata['addres'])


# def test_step1():
#     # Тест при не правильном вводе данных пользователя
#     x_selector1 = """//*[@id="login"]/div[1]/label/input"""  # вводим Username
#     input1 = site.find_element("xpath", x_selector1)
#     input1.send_keys("test")
#
#     x_selector2 = """//*[@id="login"]/div[2]/label/input"""  # вводим passwd
#     input2 = site.find_element("xpath", x_selector2)
#     input2.send_keys("test")
#
#     btn_selector = "button"
#     btn = site.find_element("css", btn_selector)
#     btn.click()
#
#     x_selector3 = """//*[@id="app"]/main/div/div/div[2]/h2"""  # Поиск сообщения об ошибке после неверного ввода
#     err_label = site.find_element("xpath", x_selector3)
#     assert err_label.text == "401"


def test_step2(site_connect):
    # Тест при правильном вводе данных пользователя


    # Ищу слово Blog, которое высвечивается после успешной регистрации
    site_connect.registration_on_the_website()
    x_selector3 = """//*[@id="app"]/main/div/div[1]/h1"""
    flag_text_blog = site_connect.find_element("xpath", x_selector3)
    time.sleep(1)
    assert flag_text_blog.text == "Blog"

#
def test_step3(site_connect):
    # Тест создание нового поста

    # Нажимаю на кнопку Нового поста

    btn_selector = """//*[@id="create-btn"]"""
    btn = site_connect.find_element("xpath", btn_selector)
    btn.click()

    time.sleep(2)

    # Создание тайтла у поста
    x_titel = """/html/body/div/main/div/div/form/div/div/div[1]/div/label/input"""
    input_titel = site_connect.find_element("xpath", x_titel)
    input_titel.send_keys("test_titel")

    # Создание дискрипшена
    x_discription = """//*[@id="create-item"]/div/div/div[2]/div/label/span/textarea"""
    input_discription = site_connect.find_element("xpath", x_discription)
    input_discription.send_keys("test_discription")

    # Создание контента
    x_content = """//*[@id="create-item"]/div/div/div[3]/div/label/span/textarea"""
    input_content = site_connect.find_element("xpath", x_content)
    input_content.send_keys("test_content")

    # # Создание колендаря
    # ddd1 = date.today()  # создание даты для ввода
    # ddd1 = ddd1 - timedelta(days=1)
    # i = int(ddd1.day) + 1  # вводим дату на "завтра"
    #
    # x_calendar = """//*[@id="create-item"]/div/div/div[5]/div/div/label"""
    # input_calendar = site.find_element("xpath", x_calendar)
    # input_calendar[i].click()

    #Кликаю на кнопку Save
    x_btm_save = """/html/body/div/main/div/div/form/div/div/div[7]/div/button/span"""
    btn_save = site_connect.find_element("xpath", x_btm_save)
    btn_save.click()
    time.sleep(1)


    # Ищу название нового поста, если посту успешно будет создан то название поста будет верное

    x_name_post = """/html/body/div[1]/main/div/div[1]/h1"""
    flag_name_post = site_connect.find_element("xpath", x_name_post)
    print(f"{flag_name_post.text = } | {flag_name_post.text}")
    time.sleep(1)

    assert flag_name_post.text == "test_titel"

# def test_test1(site_connect):
#     a = True
#
#     with open("./test.txt", 'w') as f:
#         f.write(str(site_connect.__dir__()))
#     time.sleep(2)
#     assert a == True
