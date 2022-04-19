'''
This is a very basic script for testing the number of concurrent connections that can be open / load testing.

Requires selenium, the Chrome browser and a matching chromedriver binary to be available.
'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from multiprocessing import Process
from time import sleep

CHROMEDIRVER_PATH = './chromedriver'

def run():
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(CHROMEDIRVER_PATH, options=options)
    for i in range(200):
        driver.execute_script('''window.open("http://localhost:5000","_blank");''')

    sleep(10)

    for handle in driver.window_handles:
        driver.switch_to.window(window_name=handle)
        driver.close()

for i in range(6):
    p = Process(target=run)
    p.start()
