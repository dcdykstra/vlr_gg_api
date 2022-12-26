import uvicorn

from fastapi import FastAPI, Request
from loguru import logger as log
from scrape_v2 import VLR_Scraper

app = FastAPI()
vlr = VLR_Scraper()
# attach route to our API app


@app.get("/stats/header/{url}")
async def match_stats_header(url: str):
    return vlr.get_match_stats_header(url)


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=3001)
