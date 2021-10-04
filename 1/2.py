#coding:utf-8
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.webdriver import ChromeOptions

option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
brower = webdriver.Firefox(options=option)
time.sleep(3)
brower.get("https://www.mafengwo.cn")
time.sleep(3)

brower.close()