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

def parse_projects_from_page(page):
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
            if title and link and link.startswith("https://www.freelancermap.de/projekt/"):
                projects.append({"title": title, "link": link})
        except:
            continue
    return projects

all_projects = []
MAX_PAGES = 5

for i in range(1, MAX_PAGES + 1):
    projects = parse_projects_from_page(i)
    if not projects:
        print("⛔️ Keine weiteren Projekte gefunden.")
        break
    all_projects.extend(projects)
    time.sleep(1)

driver.quit()

with open("freelancermap_projects.json", "w", encoding="utf-8") as f:
    json.dump(all_projects, f, ensure_ascii=False, indent=2)

print(f"✅ Insgesamt {len(all_projects)} Projekte gespeichert.")
