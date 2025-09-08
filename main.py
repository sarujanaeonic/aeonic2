from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import requests
import json
import time

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    return webdriver.Chrome(options=chrome_options)

def login(driver, username, password):
    login_url = "https://www.freelancermap.de/login"
    driver.get(login_url)
    print("🔐 Anmeldung ...")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "login")))
    driver.find_element(By.NAME, "login").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    WebDriverWait(driver, 10).until(EC.url_changes(login_url))
    print("✅ Anmeldung erfolgreich.")

def parse_projects_from_page(driver, page, seen_links, keyword_for_url, keyword_for_field):
    url = f"https://www.freelancermap.de/projektboerse.html?query={keyword_for_url}&countries%5B%5D=1&sort=2&pagenr={page}"
    print(f"🔄 Lade Seite {page} für '{keyword_for_field}' ...")
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href*="/projekt/"]'))
        )
    except:
        print("❌ Keine Projekte gefunden.")
        return []

    items = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/projekt/"]')
    print(f"✅ {len(items)} Projekte gefunden.")
    projects = []

    for item in items:
        try:
            title = item.text.strip()
            link = item.get_attribute("href")

            if title and link and link.startswith("https://www.freelancermap.de/projekt/") and link not in seen_links:
                try:
                    container = item.find_element(By.XPATH, "./ancestor::div[contains(@class, 'project-container')]")
                    date_element = container.find_element(By.CSS_SELECTOR, "span.created-date")
                    raw_date_text = date_element.text.strip().replace("eingetragen am:", "").strip()
                    parsed_date = datetime.strptime(raw_date_text, "%d.%m.%Y / %H:%M")
                    date_text = parsed_date.strftime("%Y-%m-%d %H:%M")
                except:
                    date_text = "Unbekannt"

                projects.append({
                    "title": title,
                    "link": link,
                    "date": date_text,
                    "keywords": keyword_for_field
                })
                seen_links.add(link)
        except:
            continue

    return projects

def send_to_webhook(projects, keyword, webhook_url):
    try:
        response = requests.post(
            webhook_url,
            json=projects,
            headers={"Content-Type": "application/json"}
        )
        print(f"📡 Gesendet '{keyword}' → Status {response.status_code}")
    except Exception as e:
        print(f"❌ Fehler bei '{keyword}': {str(e)}")

def run_for_keyword(keyword_raw, webhook_url):
    keyword = keyword_raw.strip()
    if not keyword:
        return

    keyword_for_url = keyword.replace(" ", "+")
    print(f"\n🚀 Starte Suche für Keyword: {keyword}")

    driver = setup_driver()
    login(driver, USERNAME, PASSWORD)

    all_projects = []
    seen_links = set()
    MAX_PAGES = 10

    for i in range(1, MAX_PAGES + 1):
        projects = parse_projects_from_page(driver, i, seen_links, keyword_for_url, keyword)
        if not projects:
            print("⛔️ Keine neuen Projekte mehr gefunden.")
            break
        all_projects.extend(projects)
        time.sleep(1)

    driver.quit()

    if all_projects:
        send_to_webhook(all_projects, keyword, webhook_url)
    else:
        print(f"⚠️ Keine Projekte gefunden für '{keyword}'.")

# 🔐 Zugangsdaten
USERNAME = "in.alen.kairat@gmail.com"
PASSWORD = "Sommer2025++"

# 📄 Keywords lesen
with open("queries.txt", "r", encoding="utf-8") as f:
    keywords = f.readlines()

# 🌐 Webhook
webhook_url = "https://saru2025.app.n8n.cloud/webhook/dynamo-prof-prod"

# 🔁 Keywords LOOP
#for kw in keywords:
#    run_for_keyword(kw, webhook_url)

for i, kw in enumerate(keywords):
    run_for_keyword(kw, webhook_url)

    if i < len(keywords) - 1:
        print("⏳ Warte 10 Minuten bis zum nächsten Keyword ...")
        time.sleep(1800)  # 10 min
