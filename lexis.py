import time
import random

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Edge(executable_path=r"C:\Users\Sergey\Desktop\New folder\edgedriver_win64\msedgedriver.exe")
driver.get("https://plus.lexis.com/practice?config=00JABiY2NmNDQyYy00YzVkLTQ1ZTEtOTlmOC1iZWY3ODJhMGU1MmMKAFBvZENhdGFsb2dvYAlCefLrCgCo7TDuPYU3&crid=2fccf270-a8a7-48a2-9131-46370b8d990f")

userid = driver.find_element_by_id("userid")
time.sleep(random.randint(1, 10))
userid.clear()
userid.send_keys("p5vps06280gn@tuta.io")

password = driver.find_element_by_id("password")
time.sleep(random.randint(1, 10))
password.clear()
password.send_keys("0U5o#PVw&&y$")

time.sleep(random.randint(1, 10))
driver.find_element_by_id("chkrmflag").click()
time.sleep(random.randint(1, 10))
driver.find_element_by_id("signInSbmtBtn").click()

driver.implicitly_wait(10)
time.sleep(random.randint(1, 10))
driver.find_element_by_link_text("International By Country and Region").click()

driver.implicitly_wait(10)
time.sleep(random.randint(1, 10))
driver.find_element_by_link_text("China & Hong Kong").click()

driver.implicitly_wait(10)
time.sleep(random.randint(1, 10))
driver.find_element_by_link_text("People's Daily Online - English").click()

title = driver.find_element_by_id("title")
time.sleep(random.randint(1, 10))
title.clear()
title.send_keys("[vaccine OR vaccines OR jabs OR vaccinat* OR inoculat* OR vax OR shots]")

time.sleep(random.randint(1, 10))
driver.find_element_by_id("date").click()
driver.find_element_by_xpath(r'//*[@id="date"]/option[5]').click()

dateFrom = driver.find_element_by_id("dateFrom")
time.sleep(random.randint(1, 10))
dateFrom.clear()
dateFrom.send_keys("08/31/2020")

dateTo = driver.find_element_by_id("dateTo")
time.sleep(random.randint(1, 10))
dateTo.clear()
dateTo.send_keys("08/29/2021")

time.sleep(random.randint(1, 10))
driver.find_element_by_xpath(r'//*[@id="J8shk"]/div[1]/div/span/button[1]').click()

pages = 0
page = 1
while True:
    # Get pages
    if page == 1:
        driver.implicitly_wait(10)
        time.sleep(5)
        pages = int(driver.find_element_by_css_selector('#tf4k > ln-searchresults > div > div.column.column-80-all.pageWrapperRight > div:nth-child(2) > div.results.resultsListWrapper > div > div.resultsColumn.column > div > div.paging > pagination > button:nth-child(6)').text)

    # Select all
    driver.implicitly_wait(10)
    time.sleep(random.randint(1, 10))
    driver.find_element_by_xpath(r'//*[@id="tf4k"]/ln-searchresults/div/div[3]/div[2]/div[3]/div/div[2]/div/toolbar/div/div/ul[1]/li[1]/input').click()

    # Click download button
    driver.implicitly_wait(10)
    time.sleep(5)
    driver.find_element_by_css_selector("#tf4k > ln-searchresults > div > div.column.column-80-all.pageWrapperRight > div:nth-child(2) > div.results.resultsListWrapper > div > div.resultsColumn.column > div > toolbar > div > div > ul:nth-child(1) > li.expandable > ul > li.lastUsed > toolbarbutton > button").click()
    
    # Set file name
    FileName = driver.find_element_by_id("FileName")
    driver.implicitly_wait(10)
    time.sleep(5)
    FileName.clear()
    FileName.send_keys(page)

    # Download
    driver.implicitly_wait(10)
    time.sleep(5)
    driver.find_element_by_css_selector("#typk > ln-delivery > lib-dialog > aside > footer > div.button-group.actions > button.button.primary.contained").click()

    driver.implicitly_wait(10)
    time.sleep(30)
    try:
        driver.find_element_by_css_selector("#tf4k > ln-searchresults > div > div.column.column-80-all.pageWrapperRight > div:nth-child(2) > div.results.resultsListWrapper > div > div.resultsColumn.column > div > div.paging > pagination > button:last-child").click()
    except selenium.common.exceptions.ElementClickInterceptedException:
        print("ERROR")

    if page == pages:
        break
    page += 1

    time.sleep(15)

time.sleep(15)
driver.close()