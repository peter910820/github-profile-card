# import matplotlib.pyplot as plt
import json
# import numpy as np
import pygal
import requests

from collections import Counter
from pygal.style import DarkSolarizedStyle
from requests import RequestException


class ApiGet(object):
    def __init__(self, user: str):
        with open('./colors_map.json') as f:
            self.colors = json.load(f)
        self.output_colors = []
        self.user = user
        self.url = f"https://api.github.com/users/{user}/repos"
        self.language_data = {}
        self.magnification = 0.0

    def get_data(self) -> None | RequestException:
        try:
            r = requests.get(self.url)
        except RequestException as e:
            return e
        data = json.loads(r.content)
        if data:
            self.language_data = Counter(
                [d["language"] for d in data if d["language"] is not None])
            self.language_data = dict(self.language_data)
            self.magnification = 100 / \
                sum([value for value in self.language_data.values()])
        else:
            print("找不到使用者")

    def draw_chart_pygal(self) -> None:
        style = DarkSolarizedStyle(title_font_size=50)
        style.colors = tuple(self.colors[key]
                             for key in self.language_data.keys())
        chart = pygal.Pie(inner_radius=0.5, style=style)
        chart.title = "PR of Repo Languages"
        try:
            for key, value in self.language_data.items():
                chart.add(key, round(value * self.magnification, 1))
        except Exception as e:
            print(f"ERROR: {e}")
        chart.render_to_file(f"./chart/{self.user}_profile.svg")

    # a feature use matplotlib

    # def __draw_chart_matplotlib(self) -> None:
    #     plt.style.use("Solarize_Light2")

    #     labels = [key for key in self.language_data.keys()]
    #     sizes = list(map(lambda t: t * self.magnification,
    #                  self.language_data.values()))
    #     print(sizes)
    #     colors = plt.cm.viridis(np.linspace(0, 1, len(sizes)))
    #     # explode = (0.1, 0, 0, 0)  # Highlight a block
    #     plt.figure(figsize=(10, 8))
    #     plt.pie(sizes, labels=labels, colors=colors,
    #             shadow=True, startangle=140)

    #     plt.axis("equal")
    #     plt.title("Gitgub profile", pad=20)

    #     plt.savefig(f"./chart/{self.user}_profile.png")
