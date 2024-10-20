import json
import matplotlib.pyplot as plt
import numpy as np
import requests

from collections import Counter
from requests import RequestException

class ApiGet(object):
    def __init__(self, user: str):
        self.user = user
        self.url = f"https://api.github.com/users/{user}/repos"
        self.language_data = None

    def get_data(self) -> None:
        try:
            r = requests.get(self.url)
        except RequestException as e:
            print(e)
        data = json.loads(r.content)
        if data:
            self.language_data = Counter([ d["language"] for d in data if d["language"] is not None])
            self.language_data = dict(self.language_data)
        else:
            print("找不到使用者")

    def draw_chart(self):
        plt.style.use("Solarize_Light2")

        labels = [key for key in self.language_data.keys()]
        tmp = sum([value for value in self.language_data.values()])
        magnification = 100 / tmp
        sizes = list(map(lambda t: t * magnification, self.language_data.values()))
        print(sizes)
        colors = plt.cm.viridis(np.linspace(0, 1, len(sizes)))
        # explode = (0.1, 0, 0, 0)  # 突出某個區塊（例如 Apple）
        plt.figure(figsize=(10, 8))
        plt.pie(sizes, labels=labels, colors=colors,
                autopct="%1.1f%%", shadow=True, startangle=140)

        plt.axis("equal")
        plt.title("Gitgub profile", pad=20)

        plt.savefig(f"./img/{self.user} profile.png")