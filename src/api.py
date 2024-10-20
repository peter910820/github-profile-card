import json
import requests
from requests import RequestException

class ApiGet(object):
    def __init__(self, name: str):
        self.url = f"https://api.github.com/users/{name}/repos"

    def get_data(self):
        try:
            r = requests.get(self.url)
        except RequestException as e:
            print(e)
        data = json.loads(r.content)
        if data:
            return [ d["language"] for d in data ]

        else:
            print('找不到使用者')