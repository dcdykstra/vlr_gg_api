import requests
import re
from selectolax.parser import HTMLParser


class URL_Scraper():
    def __init__(self) -> None:
        pass

    def get_html(self, url):
        resp = requests.get(url)
        self.url = url
        html, status_code = resp.text, resp.status_code
        return HTMLParser(html), status_code

    # input from this type of page https://www.vlr.gg/events/
    def get_event_urls(self, region, event_type, page):
        url = f"https://www.vlr.gg/events/{region}/?page={page}"
        html, status = self.get_html(url)
        events = html.css_first("div.events-container")

        container = events.css_first(
            f"div.wf-label.mod-large.mod-{event_type}").parent

        event_urls = ["https://www.vlr.gg" + i.attributes.get(
            "href") for i in container.css("a.wf-card.mod-flex.event-item")]

        segments = {"status": status, "urls": event_urls}

        if status != 200:
            raise Exception(f"Response Code: {status}")
        return segments

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

        if status != 200:
            raise Exception(f"Response Code: {status}")
        return segments
