from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)

def login(username, password):
    login_url = "https://www.freelancermap.de/login"
    driver.get(login_url)
    print("🔐 Anmeldung ...")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "login")) 
    )

    driver.find_element(By.NAME, "login").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    WebDriverWait(driver, 10).until(
        EC.url_changes(login_url)
    )
    print("✅ Anmeldung erfolgreich.")

def parse_projects_from_page(page, seen_links):
    url = f"https://www.freelancermap.de/projektboerse.html?query=sap+bw&countries%5B%5D=1&sort=2&pagenr={page}"
    print(f"🔄 Seite wird geladen {page}...")
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
            if (
                title and link and
                link.startswith("https://www.freelancermap.de/projekt/") and
                link not in seen_links
            ):
                projects.append({"title": title, "link": link})
                seen_links.add(link)
        except:
            continue
    return projects


USERNAME = "in.alen.kairat@gmail.com"
PASSWORD = "Sommer2025++"

login(USERNAME, PASSWORD)

all_projects = []
seen_links = set()
MAX_PAGES = 10

for i in range(1, MAX_PAGES + 1):
    projects = parse_projects_from_page(i, seen_links)
    if not projects:
        print("⛔️ Keine neuen Projekte mehr gefunden. Stoppen.")
        break
    all_projects.extend(projects)
    time.sleep(1)

driver.quit()

with open("freelancermap_projects.json", "w", encoding="utf-8") as f:
    json.dump(all_projects, f, ensure_ascii=False, indent=2)

print(f"✅ Einzigartige Projekte gespeichert: {len(all_projects)}.")
