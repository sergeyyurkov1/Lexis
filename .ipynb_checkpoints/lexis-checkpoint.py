# msedge-selenium-tools

import time, random, os

import config

from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions

# from msedge.selenium_tools import Edge
# from msedge.selenium_tools import EdgeOptions

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# edge_options = EdgeOptions()
# edge_options.use_chromium = True
# edge_options.add_argument("user-data-dir=")

chrome_options = ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument(r"user-data-dir=C:\Users\Sergey\Desktop\New folder\Profile")

path_ = os.path.join(r"C:\Users\Sergey\Desktop\Data", config.navigation[-1])
os.makedirs(path_, exist_ok=True)
prefs = {"profile.default_content_settings.popups": 0,
            "download.default_directory": path_,
            "directory_upgrade": True}
chrome_options.add_experimental_option("prefs", prefs)

# driver = Edge(executable_path=r"C:\Users\Sergey\Desktop\New folder\edgedriver_win64\msedgedriver.exe", edge_options)
driver = Chrome(executable_path=r"C:\Users\Sergey\Desktop\New folder\chromedriver_win32\chromedriver.exe", chrome_options=chrome_options)
driver.get("https://plus.lexis.com/practice?config=00JABiY2NmNDQyYy00YzVkLTQ1ZTEtOTlmOC1iZWY3ODJhMGU1MmMKAFBvZENhdGFsb2dvYAlCefLrCgCo7TDuPYU3")

# Login
# ---------------------------
try:
    userid = driver.find_element_by_id("userid")
    time.sleep(random.randint(2, 10))
    userid.clear()
    userid.send_keys(config.login)

    password = driver.find_element_by_id("password")
    time.sleep(random.randint(2, 10))
    password.clear()
    password.send_keys(config.password)

    # Remember me
    time.sleep(random.randint(2, 10))
    driver.find_element_by_id("chkrmflag").click()

    # Sign in button
    time.sleep(random.randint(2, 10))
    driver.find_element_by_id("signInSbmtBtn").click()
except NoSuchElementException:
    pass

# Navigation
# ---------------------------
assert "News" in driver.title

for i in config.navigation:

    driver.implicitly_wait(10)
    time.sleep(random.randint(2, 10))
    driver.find_element_by_link_text(i).click()
    assert i in driver.title

title = driver.find_element_by_id("title")
time.sleep(random.randint(2, 10))
title.clear()
title.send_keys(config.query)

time.sleep(random.randint(2, 10))
driver.find_element_by_id("date").click()
driver.find_element_by_xpath(r'//*[@id="date"]/option[5]').click()

dateFrom = driver.find_element_by_id("dateFrom")
time.sleep(random.randint(2, 10))
dateFrom.clear()
dateFrom.send_keys(config.date["from"])

dateTo = driver.find_element_by_id("dateTo")
time.sleep(random.randint(2, 10))
dateTo.clear()
dateTo.send_keys(config.date["to"])

time.sleep(random.randint(2, 10))
# driver.find_element_by_xpath(r'//*[@id="J8shk"]/div[1]/div/span/button[1]').click()
driver.find_element_by_css_selector('#J4shk > div.lexisplus-documentslist > div > span > button.lexisplus-asf-search-button.btn.icon.la-Search').click()

page = 1

def select_and_download():
    # Select all
    try:
        WebDriverWait(driver, 90).until(
            EC.visibility_of_element_located((By.XPATH, r'//*[@id="tf4k"]/ln-searchresults/div/div[3]/div[2]/div[3]/div/div[2]/div/toolbar/div/div/ul[1]/li[1]/input'))
        )
        time.sleep(random.randint(2, 10))
        checkbox = driver.find_element_by_xpath(r'//*[@id="tf4k"]/ln-searchresults/div/div[3]/div[2]/div[3]/div/div[2]/div/toolbar/div/div/ul[1]/li[1]/input')
        if checkbox.is_selected() == False:
            checkbox.click()
    except TimeoutException:
        driver.refresh()
        select_and_download()

    # Click download button
    driver.implicitly_wait(10)
    time.sleep(random.randint(2, 10))
    driver.find_element_by_css_selector("#tf4k > ln-searchresults > div > div.column.column-80-all.pageWrapperRight > div:nth-child(2) > div.results.resultsListWrapper > div > div.resultsColumn.column > div > toolbar > div > div > ul:nth-child(1) > li.expandable > ul > li.lastUsed > toolbarbutton > button").click()
    
    # Set file name
    try:
        WebDriverWait(driver, 90).until(
            EC.visibility_of_element_located((By.ID, "FileName"))
        )
        FileName = driver.find_element_by_id("FileName")
        time.sleep(random.randint(2, 10))
        FileName.clear()
        FileName.send_keys(page)
    except TimeoutException:
        driver.refresh()
        select_and_download()

    # Download
    driver.implicitly_wait(10)
    time.sleep(random.randint(2, 10))
    driver.find_element_by_css_selector("#typk > ln-delivery > lib-dialog > aside > footer > div.button-group.actions > button.button.primary.contained").click()

def go():    
    while True:
        select_and_download()
        
        # Wait for processing
        try:
            WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.ID, "delivery-popin"))
            )
            time.sleep(5)
        except TimeoutException:
            driver.refresh()
            go()
        finally:
            try:
                driver.find_element_by_css_selector("#tf4k > ln-searchresults > div > div.column.column-80-all.pageWrapperRight > div:nth-child(2) > div.results.resultsListWrapper > div > div.resultsColumn.column > div > div.paging > pagination > button:last-child").click()
            except ElementClickInterceptedException:
                print()
                print("No more pages.")
                break

            global page
            page += 1

go()

# Scroll to bottom
time.sleep(5)
driver.find_element_by_xpath('//body').send_keys(Keys.END)

time.sleep(60)
print()
print("Done!")
driver.close()