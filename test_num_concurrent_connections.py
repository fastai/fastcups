from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from time import sleep

options = Options()
options.headless = True
driver = webdriver.Chrome('./chromedriver', options=options)
while True:
    driver.execute_script('''window.open("http://localhost:5000","_blank");''')
    # driver.get('http://localhost:5000')

sleep(1)

for handle in driver.window_handles:
    driver.switch_to.window(window_name=handle)
    driver.close()
