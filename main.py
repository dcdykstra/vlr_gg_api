from fastapi import FastAPI
from loguru import logger as log
from api.scrape import VLR_Scraper
from schema import Segments_Player_Stats, Segments_Round_Stats, Segments_Event_URLS, Segments_Match_URLS

app = FastAPI(
    title="VLR.gg API",
    description="Unofficial API for VLR.gg",
    version="1.0",
    docs_url="/",
    redoc_url=None,
)
vlr = VLR_Scraper()


@app.get("/url/event/{region}/{event_type}", response_model=Segments_Event_URLS)
async def event_url(region: str, event_type: str):
    """
    region:\n
        all\n
        north-america\n
        europe\n
        brazil\n
        asia-pacific\n
        korea\n
        japan\n
        latin-america\n
        oceania\n
        mena\n
        game-changers\n
        collegiate
    event_type:\n
        completed\n
        upcoming
    """
    return vlr.get_event_urls(region, event_type)


@app.get("/url/match/{event_code}", response_model=Segments_Match_URLS)
async def match_url(event_code: str):
    """
    event_code:\n
        Event pages look like:\n
        https://www.vlr.gg/event/1015/valorant-champions-2022/playoffs\n
        The event code for this page is: 1015
    """
    return vlr.get_match_urls(event_code)


@app.get("/stats/{match_code}/rounds", response_model=Segments_Round_Stats)
async def match_stats_rounds(match_code: str):
    """
    match_code:\n
        Match pages look like:\n
        https://www.vlr.gg/130685/loud-vs-optic-gaming-valorant-champions-2022-gf\n
        The match code for this page is: 130685
    """
    return vlr.get_match_stats_round_order(match_code)


@app.get("/stats/{match_code}/{side}", response_model=Segments_Player_Stats)
async def match_stats_players(match_code: str, side: str):
    """
    match_code:\n
        Match pages look like:\n
        https://www.vlr.gg/130685/loud-vs-optic-gaming-valorant-champions-2022-gf\n
        The match code for this page is: 130685\n
    side:\n
        both\n
        t\n
        ct\n
    """
    return vlr.get_match_stats_players(match_code, side)