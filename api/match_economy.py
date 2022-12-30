import requests
import re
from selectolax.parser import HTMLParser


class Match_Economy_Scraper():
    def __init__(self) -> None:
        pass

    def get_html(self, url):
        resp = requests.get(url)
        self.url = url
        html, status_code = resp.text, resp.status_code
        return HTMLParser(html), status_code

    def get_economy_data(self, code):
        url = "https://www.vlr.gg/" + code + "/?tab=economy"
        html, status = self.get_html(url)
        match_stats = []
        container = html.css_first("div.vm-stats-container")
        games = container.css("div.vm-stats-game:not([data-game-id=all])")

        # Team Names
        teams = games[0].css("div.team")
        team1_name = teams[0].text().strip()
        team2_name = teams[1].text().strip()

        # Map Tabs
        map_tabs = html.css(f"div.vm-stats-gamesnav-item.js-map-switch")
        game_ids = [node.attributes.get("data-game-id")
                    for node in map_tabs]
        map_dict = dict(zip(game_ids, map_tabs))

        for game in games:
            map_stats = {}
            tables = game.css("table.wf-table-inset.mod-econ")
            if not tables:
                break

            game_id = game.attributes.get("data-game-id")

            # Map Name
            map_name_node = map_dict.get(game_id)
            map_name = map_name_node.css_first("div > div").text().strip()
            map_name = re.search("[a-zA-Z]+", map_name).group(0)

            # Economy Tables
            table = tables[1]
            points = table.css("td > div.rnd-sq ")

            spending = [point.text().strip() for point in points]

            # These are lists of each teams respective "$$$" for each round
            team1_spending = spending[::2]
            team2_spending = spending[1::2]

            team1_spending_dict = {}
            team2_spending_dict = {}
            for i, v in enumerate(team1_spending):
                team1_spending_dict.update({f"Round {i+1}": v})
                team2_spending_dict.update({f"Round {i+1}": team2_spending[i]})

            map_stats = {
                "url": self.url,
                "map": map_name,
                "team1": team1_name,
                "team2": team2_name,
                "team1_spending": team1_spending_dict,
                "team2_spending": team2_spending_dict
            }
            match_stats.append(map_stats)
        segments = {"status": status, "segments": match_stats}

        if status != 200:
            raise Exception(f"Response Code: {status}")
        return segments
