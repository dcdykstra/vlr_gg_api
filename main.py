import uvicorn

from fastapi import FastAPI, Request
from loguru import logger as log
from api.scrape import VLR_Scraper

app = FastAPI(
    title="vlrgg api",
    description="bruh",
    # version="1.0.5",
    docs_url="/",
    redoc_url=None,
)
vlr = VLR_Scraper()


@app.get("/url/event/{region}/{event_type}")
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


@app.get("/url/match/{event_code}")
async def match_url(event_code: str):
    """
    event_code:\n
        Event pages look like:\n
        https://www.vlr.gg/event/1015/valorant-champions-2022/playoffs\n
        The event code for this page is: 1015
    """
    return vlr.get_match_urls(event_code)


@app.get("/stats/header/{match_code}")
async def match_stats_header(match_code: str):
    """
    match_code:\n
        Match pages look like:\n
        https://www.vlr.gg/130685/loud-vs-optic-gaming-valorant-champions-2022-gf\n
        The match code for this page is: 130685
    """
    return vlr.get_match_stats_header(match_code)


@app.get("/stats/rounds/{match_code}")
async def match_stats_rounds(match_code: str):
    """
    match_code:\n
        Match pages look like:\n
        https://www.vlr.gg/130685/loud-vs-optic-gaming-valorant-champions-2022-gf\n
        The match code for this page is: 130685
    """
    return vlr.get_match_stats_round_order(match_code)


@app.get("/stats/players/{match_code}/{side}")
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


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=3001)
