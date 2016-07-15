# -*- coding: utf-8 -*-
import csv
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Firefox()

# browser.get('https://login.aliexpress.com/')
#
# input("登录完成了请输入")

browser.set_page_load_timeout(3)

try:
    browser.get('http://www.aliexpress.com/category/200010196/smart-electronics.html')
except:
    pass

with open('output/products.csv', 'w') as file:
    writer = csv.writer(file)

    writer.writerow(('产品链接', '订单数'))

    while True:

        lis = browser.find_elements(By.XPATH, "//div[@id='main-wrap']/ul/li")

        if lis is None and len(lis) == 0:
            break

        print "products:", len(lis)

        for li in lis:
            try:
                link = li.find_element(By.XPATH, ".//h3/a")
                href = link.get_attribute('href')
                col1 = href[:href.index('?')]

                order = li.find_element(By.XPATH, ".//a/em")
                size = order.text
                col2 = size[size.index('(') + 1:size.index(')')].strip()

                print col1, col2

                writer.writerow((col1, col2))
            except:
                print '------'

        if 'ui-pagination-disabled' in browser.find_element(By.CLASS_NAME, "ui-pagination-next").get_attribute('class'):
            break

        browser.find_element(By.CLASS_NAME, "ui-pagination-next").click()

        time.sleep(3)
