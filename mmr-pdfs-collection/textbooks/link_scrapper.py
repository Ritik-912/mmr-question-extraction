from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import random
import pandas as pd

geckodriver_path = "C:/Users/ritik/Downloads/geckodriver-v0.34.0-win32/geckodriver.exe"
firefox_path = "C:/Program Files/Mozilla Firefox/firefox.exe"

def initialize_driver():
    firefox_profile = webdriver.FirefoxProfile()
    firefox_options = Options()
    firefox_options.profile = firefox_profile
    firefox_options.binary_location = firefox_path
    firefox_options.add_argument("--disable-blink-features=AutomationControlled")
    firefox_options.add_argument("--incognito")
    useragentarray = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/535.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/532.36",
        "Mozilla/4.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/533.36",
        "Mozilla/2.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/532.36",
        "Mozilla/3.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/532.36"
    ]
    firefox_options.set_preference("general.useragent.override", random.choice(useragentarray))
    driver = webdriver.Firefox(service=FirefoxService(executable_path=geckodriver_path), options=firefox_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def scroll_to_load_all(driver, num):
    iterations = num // 20
    while iterations > 0:
        driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight)", driver.find_element(By.TAG_NAME, 'main'))
        time.sleep(1)
        iterations -= 1

driver = initialize_driver()
driver.get("https://ndl.iitkgp.ac.in/se_browse/resourceType?resourceType%5B%5D=010000%2F010100&accessRights%5B%5D=open&type%5B%5D=text&subjectClass%5B%5D=03000000&subjectClass%5B%5D=03000000%2F03010000&subjectClass%5B%5D=03000000%2F03020000&subjectClass%5B%5D=03000000%2F03030000&subjectClass%5B%5D=03000000%2F03040000&subjectClass%5B%5D=03000000%2F03050000&subjectClass%5B%5D=03000000%2F03060000&subjectClass%5B%5D=03000000%2F03080000")
driver.maximize_window()
driver.implicitly_wait(10)
number_of_pdfs = int(driver.find_element(By.ID, "result-msg").text.split()[0].replace(",", ""))
print(f"Number of PDFs: {number_of_pdfs}")
scroll_to_load_all(driver, number_of_pdfs)
cards = driver.find_elements(By.CLASS_NAME, "card")
print(f"Number of resources found: {len(cards)}")
links = [card.find_element(By.TAG_NAME, 'a').get_attribute('href') for card in cards]
driver.quit()
pd.DataFrame(links, columns=["url"]).to_csv("scrapped_url.csv", index=False)