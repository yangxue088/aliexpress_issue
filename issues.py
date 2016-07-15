# -*- coding: utf-8 -*-
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

browser = webdriver.Firefox()

# browser = webdriver.Chrome('/home/mike/Downloads/chromedriver')

browser.get('https://login.aliexpress.com/')

input("登录完成了请输入")

browser.get('http://trade.aliexpress.com/issue/issue_list.htm')

order_detail_urls = []

for issue_state in ['finish']:

    Select(browser.find_element(By.ID, 'order-status')).select_by_value(issue_state)

    browser.find_element(By.ID, 'search-btn').click()

    while True:
        order_detail_elements = browser.find_elements(By.XPATH, "//table[@id='dispute-table']/tbody/tr/td[1]/strong/a")

        if order_detail_elements is None and len(order_detail_elements) == 0:
            break

        order_detail_urls.extend([order_detail_element.get_attribute('href') for order_detail_element in order_detail_elements])

        if 'ui-pagination-disabled' in browser.find_element(By.CLASS_NAME, "ui-pagination-next").get_attribute('class'):
            break

        browser.find_element(By.CLASS_NAME, "ui-pagination-next").click()

print 'order count:', len(order_detail_urls)

with open('output/issues.csv', 'w') as file:
    writer = csv.writer(file)

    writer.writerow(('订单号', '订单时间', '订单金额', '退款时间', '退款金额'))

    for order_detail_url in order_detail_urls:

        browser.get(order_detail_url)

        order_no = browser.find_element(By.CLASS_NAME, 'order-no').text

        browser.find_element(By.XPATH, "//ul[@class='ui-tab-nav']/li[2]/a").click()

        order_price_text = browser.find_element(By.XPATH, "//td[@class='order-price']").text

        order_price = order_price_text
        if '\n' in order_price_text:
            order_price = order_price_text[:order_price_text.index('\n')]

        try:
            refund_date = browser.find_element(By.XPATH, "//td[@class='refund-data']").text

            refund_amount_text = browser.find_element(By.XPATH, "//td[@class='refund-amount']").text

            refund_amount = refund_amount_text
            if '\n' in refund_amount_text:
                refund_amount = refund_amount_text[:refund_amount_text.index('\n')]
        except:
            refund_date = '-'
            refund_amount = '-'

        browser.find_element(By.XPATH, "//ul[@class='ui-tab-nav']/li[3]/a").click()

        order_time = browser.find_element(By.XPATH, "//div[@id='operate-pnl']/ul/li[3]/span").text

        print order_no, order_time, order_price, refund_date, refund_amount

        writer.writerow((order_no, order_time, order_price, refund_date, refund_amount))
