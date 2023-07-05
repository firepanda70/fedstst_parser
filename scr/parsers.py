import time

from bs4 import BeautifulSoup, PageElement
from selenium import webdriver
from selenium.webdriver.common.by import By


def load_urban_env_stat() -> PageElement:
    browser = webdriver.Edge()
    browser.get('https://www.fedstat.ru/indicator/59146')
    grid = browser.find_element(By.ID, 'grid')
    time.sleep(2)
    year_filter = grid.find_element(By.XPATH, './/div[2]/div[1]/div[1]/div[2]/table/thead/tr[1]/th/a')
    year_filter.click()
    form_checkbox = grid.find_element(By.XPATH, './/div[2]/div[2]/form/ul/li/label/span')
    form_checkbox.click()
    form_button = grid.find_element(By.XPATH, './/div[2]/div[2]/form/button[1]')
    form_button.click()
    time.sleep(2)
    okado_filter = grid.find_element(By.XPATH, './/div[2]/div[1]/div[1]/div[1]/table/thead/tr/th/a')
    okado_filter.click()
    form_checkbox = grid.find_element(By.XPATH, './/div[2]/div[2]/form/ul/li/label')
    form_checkbox.click()
    form_button = grid.find_element(By.XPATH, './/div[2]/div[2]/form/button[1]')
    form_button.click()
    time.sleep(2)
    data = grid.get_attribute('innerHTML')
    browser.close()
    return BeautifulSoup(data).contents[1].div

def load_rel_urban_stat() -> PageElement:
    browser = webdriver.Edge()
    browser.get('https://www.fedstat.ru/indicator/61116')
    grid = browser.find_element(By.ID, 'grid')
    time.sleep(2)
    period_filer = grid.find_element(By.XPATH, './/div[2]/div[1]/div[1]/div[2]/table/thead/tr[2]/th[6]/a[1]')
    period_filer.click()
    form_checkbox = grid.find_element(By.XPATH, './/div[2]/div[2]/form/ul/li/label')
    form_checkbox.click()
    form_button = grid.find_element(By.XPATH, './/div[2]/div[2]/form/button[1]')
    form_button.click()
    time.sleep(2)
    data = grid.get_attribute('innerHTML')
    browser.close()
    return BeautifulSoup(data).contents[1].div
