# import matplotlib.pyplot as plt
import json
# import numpy as np
import pygal
import requests


from collections import Counter
from loguru import logger
from typing import Counter as CounterType
from pygal.style import DarkSolarizedStyle
# from requests import RequestException

from typing import Dict, List, Any


class ApiGet(object):
    def __init__(self, user: str):
        with open('./colors_map.json') as f:
            self.colors: Dict[str, str] = json.load(f)
        self.user: str = user
        self.url: str = f"https://api.github.com/users/{user}/repos"
        self.language_data: CounterType[str] = Counter()
        self.magnification: float = 0.0
        # self.output_colors = []

    def generate_chart(self) -> None:
        """
        generate user svg file entry point
        """

        try:
            r = requests.get(self.url)
            data = json.loads(r.content)
            self.language_data = Counter(
                [d["language"] for d in data if d["language"] is not None])
            self.magnification = 100 / \
                sum(value for value in self.language_data.values())
            self.__draw_chart_pygal()
            return None
        except Exception as e:
            logger.error(e)
            raise

    def __draw_chart_pygal(self) -> None:
        """
        internal function

        use to generate pygal svg file
        """

        style = DarkSolarizedStyle(title_font_size=50)
        style.colors = tuple(self.colors[key]  # type: ignore
                             for key in self.language_data.keys())
        chart = pygal.Pie(inner_radius=0.5, style=style)
        chart.title = "PR of Repo Languages"
        try:
            for key, value in self.language_data.items():
                chart.add(key, round(value * self.magnification, 1))
        except Exception as e:
            logger.error(e)
            raise
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
