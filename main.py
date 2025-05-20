from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import json
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)

try:
    driver.get("https://www.freelancermap.de/login")

    wait = WebDriverWait(driver, 10)
    login_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))

    print("Найден текст на кнопке:", login_button.text)

finally:
    driver.quit()

