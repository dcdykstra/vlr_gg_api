import requests
import time
import pandas as pd
import re
import os
import json
from selectolax.parser import HTMLParser

# MORE GENERAL
# https://scrapfly.io/blog/how-to-turn-web-scrapers-into-data-apis/
# https://www.vlr.gg/vct
# https://fastapi.tiangolo.com/deployment/deta/


class VLR_Scraper():
    def __init__(self) -> None:
        pass

    def get_html(self, url):
        resp = requests.get(url)
        self.url = url
        html, status_code = resp.text, resp.status_code
        return HTMLParser(html), status_code

    # input from this type of page https://www.vlr.gg/events/
    # event_type options are "completed" or "upcoming"

    # codes are
    """
    all
    north-america
    europe
    brazil
    asia-pacific
    korea
    japan
    latin-america
    oceania
    mena
    game-changers
    collegiate
    """

    def get_event_urls(self, code, event_type="completed"):
        url = "https://www.vlr.gg/events/" + code
        html, status = self.get_html(url)
        events = html.css_first("div.events-container")

        container = events.css_first(
            f"div.wf-label.mod-large.mod-{event_type}").parent

        event_urls = ["https://www.vlr.gg" + i.attributes.get(
            "href") for i in container.css("a.wf-card.mod-flex.event-item")]

        segments = {"status": status, "urls": event_urls}
        data = {"data": segments}

        if status != 200:
            raise Exception(f"Response Code: {status}")
        return data

    # input is an event url
    def get_match_urls(self, code):
        url = "https://www.vlr.gg/event/" + code
        html, status = self.get_html(url)
        subnav_links = [i.attributes.get("href")
                        for i in html.css("a.wf-subnav-item")]
        match_urls = []
        for i in subnav_links:
            page, status = self.get_html("https://www.vlr.gg" + i)
            a_href = [str(i.attributes.get("href")) for i in page.css("a")]
            filt = re.compile('^\/\d+\/\S+')
            match_urls += list(
                set(["https://www.vlr.gg" + link for link in a_href if filt.match(link)]))

        segments = {"status": status, "urls": match_urls}
        data = {"data": segments}

        if status != 200:
            raise Exception(f"Response Code: {status}")
        return data

    def get_match_stats_header(self, code):
        url = "https://www.vlr.gg/" + code
        html, status = self.get_html(url)
        match_stats = []
        container = html.css_first("div.vm-stats-container")
        games = container.css("div.vm-stats-game:not([data-game-id=all])")

        # Match pages may have data for more than one map
        for game in games:
            map_stats = {}
            header_data = game.css_first("div.vm-stats-game-header")

            # Map Name
            map_name = (header_data.css_first("div.map")
                        .css_first("span")
                        .text().replace("PICK", "").strip())

            # Winning Team
            winner = (header_data.css_first("div.score.mod-win")
                      .parent
                      .css_first("div.team-name")
                      .text().strip())

            # Team Names
            team_data = header_data.css("div.team")
            team1 = (team_data[0].css_first("div.team-name")
                     .text().strip())
            team2 = (team_data[1].css_first("div.team-name")
                     .text().strip())

            # Team Side Scores
            team1_ct_score = team_data[0].css_first(
                "span.mod-ct").text()
            team2_ct_score = team_data[1].css_first(
                "span.mod-ct").text()

            team1_t_score = team_data[0].css_first("span.mod-t").text()
            team2_t_score = team_data[1].css_first("span.mod-t").text()

            # Starting Sides
            team1_starting_side = (team_data[0].css_first("span")
                                   .attributes
                                   .get("class")
                                   .strip("mod-")
                                   + " side")
            team2_starting_side = (team_data[1].css_first("span")
                                   .attributes
                                   .get("class")
                                   .strip("mod-")
                                   + " side")

            map_stats = {
                "url": self.url,
                "map": map_name,
                "winner": winner,
                "team1": team1,
                "team2": team2,
                "team1_ct_score": int(team1_ct_score),
                "team2_ct_score": int(team2_ct_score),
                "team1_t_score": int(team1_t_score),
                "team2_t_score": int(team2_t_score),
                "team1_starting_side": team1_starting_side,
                "team2_starting_side": team2_starting_side,
            }
            match_stats.append(map_stats)
        segments = {"status": status, "segments": match_stats}
        data = {"data": segments}

        if status != 200:
            raise Exception(f"Response Code: {status}")
        return data

    def round_order_helper(self, node):
        if node.css_first("div.rnd-num") == None:
            pass

        else:
            rnd_num = ("Round " + node.css_first("div.rnd-num").text().strip())
            try:
                rnd_winner = node.css_first(
                    "div.rnd-sq.mod-win").attributes.get("class").strip("rnd-sq mod-win mod-")
                return rnd_num, rnd_winner
            except AttributeError as err:
                return rnd_num, None

    def get_match_stats_round_order(self, code):
        url = "https://www.vlr.gg/" + code
        html, status = self.get_html(url)
        match_stats = []
        container = html.css_first("div.vm-stats-container")
        games = container.css("div.vm-stats-game:not([data-game-id=all])")

        # Match pages may have data for more than one map
        for game in games:
            tup_list = []
            header_data = game.css_first("div.vm-stats-game-header")

            tup_list.append(("link", self.url))

            # Map Name
            map_name = (header_data.css_first("div.map")
                        .css_first("span")
                        .text().replace("PICK", "").strip())
            tup_list.append(("map", map_name))

            # Round Win Order
            vlr_rounds = game.css_first("div.vlr-rounds")
            round_order_data = vlr_rounds.css("div.vlr-rounds-row-col")[1:]

            rnd_tup = [self.round_order_helper(
                i) for i in round_order_data if self.round_order_helper(i) is not None]
            tup_list = tup_list + rnd_tup
            match_stats.append(dict(tup_list))

        segments = {"status": status, "segments": match_stats}
        data = {"data": segments}

        if status != 200:
            raise Exception(f"Response Code: {status}")
        return data

    # side options are "both", "t", "ct"
    def get_match_stats_players(self, code, side="both"):
        url = "https://www.vlr.gg/" + code
        html, status = self.get_html(url)
        match_stats = []
        container = html.css_first("div.vm-stats-container")
        games = container.css("div.vm-stats-game:not([data-game-id=all])")

        # Match pages may have data for more than one map
        for game in games:
            map_stats = {}
            header_data = game.css_first("div.vm-stats-game-header")

            # Map Name
            map_name = (header_data.css_first("div.map")
                        .css_first("span")
                        .text().replace("PICK", "").strip())

            # Team Names
            team_data = header_data.css("div.team")
            team1 = (team_data[0].css_first("div.team-name")
                     .text().strip())
            team2 = (team_data[1].css_first("div.team-name")
                     .text().strip())

            # Starting Sides
            team1_starting_side = (team_data[0].css_first("span")
                                   .attributes
                                   .get("class")
                                   .strip("mod-")
                                   + " side")
            team2_starting_side = (team_data[1].css_first("span")
                                   .attributes
                                   .get("class")
                                   .strip("mod-")
                                   + " side")

            map_stats = {
                "url": self.url,
                "map": map_name,
                "team1": team1,
                "team2": team2,
                "team1_starting_side": team1_starting_side,
                "team2_starting_side": team2_starting_side,
            }

            tables = game.css("table.wf-table-inset")

            # Get table header
            thead = tables[0].css_first("thead")
            th = [i.attributes.get("title") for i in thead.css("th")]
            th[0] = "Player"
            th[-1] = "First Kills - Deaths"

            # Two tables per match page
            for team_num, v in enumerate(tables):
                tbody = v.css_first("tbody")
                tr = tbody.css("tr")

                # Get the player match statistics
                stats = [[node.text().strip() for node in stat]
                         for stat in [row.css(f"span.side.mod-{side}") for row in tr]]

                # Get the player names and agents
                pl_ag = [[row.css_first("a > div").text().strip(),
                          row.css_first("span > img").attributes.get("title")] for row in tr]

                # Recreate the table
                table = [v+stats[i] for i, v in enumerate(pl_ag)]

                team_statistics = []
                for player in table:
                    d = {}
                    for i, v in enumerate(player):
                        # Trying to coerce strings to numerics
                        try:
                            value = float(v)
                        except ValueError:
                            value = v

                        d[th[i]] = value
                    team_statistics.append(d)
                map_stats.update(
                    {f"team{team_num+1}_statistics": team_statistics})

            match_stats.append(map_stats)

        segments = {"status": status, "segments": match_stats}
        data = {"data": segments}

        if status != 200:
            raise Exception(f"Response Code: {status}")
        return data

    def save_json(self, json_data, name):
        json_object = json.dumps(json_data, indent=4)
        cwd = os.getcwd()
        with open(f"{cwd}\\data\\{name}.json", "w") as outfile:
            outfile.write(json_object)


if __name__ == "__main__":
    vlr = VLR_Scraper()
    url = "https://www.vlr.gg/event/1015/valorant-champions-2022"

    df = vlr.get_match_urls(url)
    vlr.save_json(df, "out")
