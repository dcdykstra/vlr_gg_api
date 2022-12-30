from fastapi import FastAPI
from api.match_statistics import Match_Stats_Scraper
from api.match_economy import Match_Economy_Scraper
from api.url import URL_Scraper
from schema import *

app = FastAPI(
    title="VLR.gg API",
    description="Unofficial API for VLR.gg",
    version="1.0",
    docs_url="/",
    redoc_url=None,
)

ms_s = Match_Stats_Scraper()
me_s = Match_Economy_Scraper()
url_s = URL_Scraper()


@app.get("/url/event/{region}/{event_type}/{page}", response_model=Segments_Event_URLS)
async def event_url(region: Region, event_type: Event_Type, page: int):
    return url_s.get_event_urls(region, event_type, page)


@app.get("/url/match/{event_code}", response_model=Segments_Match_URLS)
async def match_url(event_code: str):
    """
    event_code:\n
        Event pages look like:\n
        https://www.vlr.gg/event/1015/valorant-champions-2022/playoffs\n
        The event code for this page is: 1015
    """
    return url_s.get_match_urls(event_code)


@app.get("/stats/{match_code}/rounds", response_model=Segments_Round_Stats)
async def match_stats_rounds(match_code: str):
    """
    match_code:\n
        Match pages look like:\n
        https://www.vlr.gg/130685/loud-vs-optic-gaming-valorant-champions-2022-gf\n
        The match code for this page is: 130685
    """
    return ms_s.get_match_stats_round_order(match_code)


@app.get("/stats/{match_code}/players/{side}", response_model=Segments_Player_Stats)
async def match_stats_players(match_code: str, side: Side):
    """
    match_code:\n
        Match pages look like:\n
        https://www.vlr.gg/130685/loud-vs-optic-gaming-valorant-champions-2022-gf\n
        The match code for this page is: 130685\n
    """
    return ms_s.get_match_stats_players(match_code, side)


@app.get("/stats/{match_code}/economy", response_model=Segments_Economy_Stats)
async def match_stats_economy(match_code: str):
    """
    match_code:\n
        Match pages look like:\n
        https://www.vlr.gg/130685/loud-vs-optic-gaming-valorant-champions-2022-gf\n
        The match code for this page is: 130685
    """
    return me_s.get_economy_data(match_code)
