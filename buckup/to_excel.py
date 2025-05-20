import pandas as pd
import json

with open("freelancermap_projects.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

df.to_excel("freelancermap_projects.xlsx", index=False)

print("✅ Daten wurden in freelancermap_projects.xlsx gespeichert")
