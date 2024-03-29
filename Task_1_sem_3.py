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

with open("./locators.yaml") as f:
    locators = yaml.safe_load(f)


class Site:
    # проверка на то какой браузер используется в тесте
    def __init__(self, browser, address):
        self.browser = browser
        self.address = address

        if self.browser == 'chrome':
            self.driver = webdriver.Chrome()
        elif self.browser == 'firefox':
            self.driver = webdriver.Chrome()

        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(testdata['sleep_time'])
        self.driver.maximize_window()
        self.driver.get(address)



    def registration_on_the_website(self):
        x_selector1 = locators['LOCATOR_USER_NAME']  # вводим Username
        input1 = self.find_element("xpath", x_selector1)
        input1.send_keys(username)

        x_selector2 = locators['LOCATOR_PASSWORD']  # вводим passwd
        input2 = self.find_element("xpath", x_selector2)
        input2.send_keys(passwd)

        btn_selector = "button"
        btn = self.find_element("css", btn_selector)
        btn.click()

    def bed_registration_on_the_website(self):
        x_selector1 = locators['LOCATOR_USER_NAME']  # вводим Username
        input1 = self.find_element("xpath", x_selector1)
        input1.send_keys("test")

        x_selector2 = locators['LOCATOR_PASSWORD']  # вводим passwd
        input2 = self.find_element("xpath", x_selector2)
        input2.send_keys("test")

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

def test_step1():
    # Тест при не правильном вводе данных пользователя
    site_bed = Site(testdata["browser"], testdata['addres'])
    site_bed.bed_registration_on_the_website()

    site_bed.driver.implicitly_wait(testdata['sleep_time'])

    # /html/body/div/main/div/div/div[2]/h2
    x_selector3 = locators['LOCATOR_ERROR_401']  # Поиск сообщения об ошибке после неверного ввода
    err_label = site_bed.find_element("xpath", x_selector3)

    print(err_label.text)
    site_bed.driver.implicitly_wait(testdata['sleep_time'])
    assert str(err_label.text) == '401'
    site_bed.close()


def test_step2(site_connect):
    # Тест при правильном вводе данных пользователя

    # Ищу слово Blog, которое высвечивается после успешной регистрации
    site_connect.registration_on_the_website()
    x_selector3 = locators['LOCATOR_WORD_BLOCK']
    flag_text_blog = site_connect.find_element("xpath", x_selector3)
    site_connect.driver.implicitly_wait(testdata['sleep_time'])
    assert flag_text_blog.text == "Blog"


def test_step3(site_connect):
    # Тест создание нового поста

    # Нажимаю на кнопку Нового поста

    btn_selector = locators['LOCATOR_BOTTOM_NEWPOST']
    btn = site_connect.find_element("xpath", btn_selector)
    btn.click()
    btn.click()

    site_connect.driver.implicitly_wait(testdata['sleep_time'])

    # Создание тайтла у поста
    x_titel = locators['LOCATOR_TITEL_IN_NEWPOST']
    input_titel = site_connect.find_element("xpath", x_titel)
    input_titel.send_keys("test_titel")

    # Создание дискрипшена
    x_discription = locators['LOCATOR_DISCCRIPTION_IN_NEWPOST']
    input_discription = site_connect.find_element("xpath", x_discription)
    input_discription.send_keys("test_discription")

    # Создание контента
    x_content = locators['LOCATOR_CONTENT_IN_NEWPOST']
    input_content = site_connect.find_element("xpath", x_content)
    input_content.send_keys("test_content")

    # Кликаю на кнопку Save
    x_btm_save = locators['LOCATOR_BOTTOM_SAVE']
    btn_save = site_connect.find_element("xpath", x_btm_save)
    btn_save.click()

    site_connect.driver.implicitly_wait(testdata['sleep_time'])

    # Ищу название нового поста, если посту успешно будет создан то название поста будет верное
    x_name_post =locators['LOCATOR_FIND_NAME_NEWPOST_CSS']
    flag_name_post = site_connect.find_element("css", x_name_post)
    site_connect.driver.implicitly_wait(testdata['sleep_time'])
    print(f"{flag_name_post.text = } | {flag_name_post.text}")
    time.sleep(2)

    assert flag_name_post.text == "test_titel"

def test_step4(site_connect):
    a = True
    btn_selector = locators['LOCATOR_BOTTOM_CONTACT']
    btn = site_connect.find_element("xpath", btn_selector)
    btn.click()
    site_connect.driver.implicitly_wait(testdata['sleep_time'])

    # Заполнить поле имени
    x_name = locators['LOCATOR_YOUR_CONTACT_NAME']
    input_name= site_connect.find_element("xpath", x_name)
    input_name.send_keys("test_name")

    # Заполнить поле email
    x_email = locators['LOCATOR_YOUR_CONTACT_EMAIL']
    input_email = site_connect.find_element("xpath", x_email)
    input_email.send_keys("test_email@test")

    # Заполнить поле contant
    x_contant = locators['LOCATOR_YOUR_CONTACT_CONTENT']
    input_contant = site_connect.find_element("xpath", x_contant)
    input_contant.send_keys("TEST!")

    # Кликнуть на кнопку Contact Us
    btn_selector_contact = locators['LOCATOR_BOTTOM_IN_CONTACT_US']
    btn_contact = site_connect.find_element("xpath", btn_selector_contact)
    btn_contact.click()

    site_connect.driver.implicitly_wait(testdata['sleep_time'])
    time.sleep(1)

    alert = site_connect.driver.switch_to.alert  # отлавливаю контекстное окно alert
    alert_text = alert.text
    site_connect.driver.implicitly_wait(testdata['sleep_time'])
    alert.dismiss() # клик на кнопку ОК в alert

    time.sleep(2)
    assert alert_text == 'Form successfully submitted'

