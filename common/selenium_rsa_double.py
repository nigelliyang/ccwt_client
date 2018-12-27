#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/12/21 10:10    @Author  : xycfree
# @Descript: 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# ========================================================== #
# chrome headless, 设置无头浏览器
# http://brucedone.com/archives/1201
# http://www.cnblogs.com/fnng/p/7797839.html
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# driver = webdriver.Chrome(chrome_options=chrome_options)
# ========================================================== #


chrome_driver = r"D:\tools\chrome_driver\chromedriver.exe"
driver = webdriver.Chrome()
driver.get("https://cn.tradingview.com/chart/rP0mQCuj/")
driver.maximize_window()
driver.implicitly_wait(3)

driver.find_element_by_link_text("登录").click()

driver.find_element_by_name("username").send_keys('bingpoli')
driver.find_element_by_name("password").send_keys('bingpoli123')
driver.find_element_by_class_name("tv-button__loader").click()
driver.implicitly_wait(3)

cookies = driver.get_cookies()
print('cookies: {}'.format(cookies))

# js = ""
# driver.execute_script()