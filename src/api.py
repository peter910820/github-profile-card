import json
import matplotlib.pyplot as plt
import numpy as np
import pygal
import requests

from collections import Counter
from requests import RequestException

class ApiGet(object):
    def __init__(self, user: str):
        self.user = user
        self.url = f"https://api.github.com/users/{user}/repos"
        self.language_data = {}
        self.magnification = 0.0

    def get_data(self) -> None:
        try:
            r = requests.get(self.url)
        except RequestException as e:
            print(e)
        data = json.loads(r.content)
        if data:
            self.language_data = Counter([ d["language"] for d in data if d["language"] is not None])
            self.language_data = dict(self.language_data)
            self.magnification = 100 / sum([value for value in self.language_data.values()])
        else:
            print("找不到使用者")

    def draw_chart_pygal(self) -> None:
        chart = pygal.Pie(inner_radius = 0.5)
        chart.title = "Github Profile"
        for key, value in self.language_data.items():
            chart.add(key, round(value * self.magnification, 1))
        chart.render_to_file(f"./img/{self.user}_profile.svg")


    def draw_chart_matplotlib(self) -> None:
        plt.style.use("Solarize_Light2")

        labels = [key for key in self.language_data.keys()]
        sizes = list(map(lambda t: t * self.magnification, self.language_data.values()))
        print(sizes)
        colors = plt.cm.viridis(np.linspace(0, 1, len(sizes)))
        # explode = (0.1, 0, 0, 0)  # Highlight a block
        plt.figure(figsize=(10, 8))
        plt.pie(sizes, labels=labels, colors=colors,
                 shadow=True, startangle=140)

        plt.axis("equal")
        plt.title("Gitgub profile", pad=20)

        plt.savefig(f"./img/{self.user}_profile.png")
        