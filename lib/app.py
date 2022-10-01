# import requests
# from bs4 import BeautifulSoup

# resp = requests.get("https://devdocs.io/")
# respText = resp.text;
# soup = BeautifulSoup(respText, 'html.parser')

# sidebar = soup.find("._sidebar")
# disabledList = soup.find("._disabled-list")

# print()

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options, executable_path=r'./chromedriver_win32/chromedriver.exe')
driver.get('https://devdocs.io')
delay = 10

try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "_intro-message")))

    source = driver.page_source
    source = source.replace("\n", "")
    soup = BeautifulSoup(source, 'html.parser')
    lists = soup.find_all('a')
    listItems = soup.find_all('a')

    print("Listing all items---------------")
    for list in lists:
        print(list.get("href"))

    print("Listing all list items--------------")
    for item in listItems:
        print(item.get("href"))

    driver.close()
except TimeoutException:
    print("Page timed out without completely loading")