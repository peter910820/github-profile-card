import json
import requests
import yaml

r = requests.get("https://raw.githubusercontent.com/github-linguist/linguist/refs/heads/main/lib/linguist/languages.yml")
data = yaml.load(r.content, Loader=yaml.Loader)
j_data = json.dumps({key: value.get("color", None) for key, value in data.items()}, indent=4)
with open("colors_map.json", "w") as f:
    f.write(j_data)
