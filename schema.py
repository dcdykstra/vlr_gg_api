from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class Event_Type(str, Enum):
    COMPLETED = "completed"
    UPCOMING = "upcoming"


class Region(str, Enum):
    ALL = "all"
    NA = "north-america"
    EU = "europe"
    BR = "brazil"
    APAC = "asia-pacific"
    KR = "korea"
    JP = "japan"
    LATAM = "latin-america"
    OCE = "oceania"
    MENA = "mena"
    GC = "game-changers"
    COLL = "collegiate"


class Side(str, Enum):
    BOTH = "both"
    CT = "ct"
    T = "t"


class Player_Statistics(BaseModel):
    Player: str
    Agent: str
    Rating: Optional[int] = Field(description="VLR Rating")
    ACS: int = Field(alias="Average Combat Score")
    Kills: int
    Deaths: int
    Assists: int
    KD: int = Field(alias="Kills - Deaths")
    KAST: str = Field(alias="Kill, Assist, Trade, Survive %")
    ADR: int = Field(alias="Average Damage per Round")
    HS: str = Field(alias="Headshot %")
    FK: int = Field(alias="First Kills")
    FD: int = Field(alias="First Deaths")
    FKFD: int = Field(alias="First Kills - First Deaths")


class Match_Statistics(BaseModel):
    url: str = Field(description="URL for the match")
    map: str = Field(description="Map for the respective match")
    winner: str = Field(description="Winning team")
    team1: str = Field(description="Team 1 Full Name")
    team2: str = Field(description="Team 2 Full Name")
    team1_ct_score: int = Field(
        description="Total rounds team 1 won on ct side")
    team2_ct_score: int = Field(
        description="Total rounds team 2 won on ct side")
    team1_t_score: int = Field(description="Total rounds team 1 won on t side")
    team2_t_score: int = Field(description="Total rounds team 2 won on t side")
    team1_starting_side: str = Field(description="Side team 1 started on")
    team2_starting_side: str = Field(description="Side team 2 started on")
    team1_statistics: List[Player_Statistics]
    team2_statistics: List[Player_Statistics]


class Round_Statistics(BaseModel):
    url: str = Field(description="URL for the match")
    map: str = Field(description="Map for the respective match")
    winner: str = Field(description="Winning team")
    team1: str = Field(description="Team 1 Full Name")
    team2: str = Field(description="Team 2 Full Name")
    team1_ct_score: int = Field(
        description="Total rounds team 1 won on ct side")
    team2_ct_score: int = Field(
        description="Total rounds team 2 won on ct side")
    team1_t_score: int = Field(description="Total rounds team 1 won on t side")
    team2_t_score: int = Field(description="Total rounds team 2 won on t side")
    team1_starting_side: str = Field(description="Side team 1 started on")
    team2_starting_side: str = Field(description="Side team 2 started on")
    round_order_data: dict


class Economy_Statistics(BaseModel):
    url: str = Field(description="URL for the match")
    map: str = Field(description="Map for the respective match")
    team1: str = Field(description="Team 1 Short Name")
    team2: str = Field(description="Team 2 Short Name")
    team1_spending: dict
    team2_spending: dict


class Segments_Match_URLS(BaseModel):
    status: int
    urls: list = Field(description="List of Valorant match URLS")


class Segments_Event_URLS(BaseModel):
    status: int
    urls: list = Field(description="List of Valorant event URLS")


class Segments_Player_Stats(BaseModel):
    status: int
    segments: List[Match_Statistics]


class Segments_Round_Stats(BaseModel):
    status: int
    segments: List[Round_Statistics]


class Segments_Economy_Stats(BaseModel):
    status: int
    segments: List[Economy_Statistics]
