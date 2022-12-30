from pydantic import BaseModel, Field
from typing import List, Optional


class Player_Statistics(BaseModel):
    Player: str
    Agent: str
    Rating: int = Field(description="VLR Rating")
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
    r1: str = Field(description="Winning Side", alias="Round 1")
    r2: str = Field(description="Winning Side", alias="Round 2")
    r3: str = Field(description="Winning Side", alias="Round 3")
    r4: str = Field(description="Winning Side", alias="Round 4")
    r5: str = Field(description="Winning Side", alias="Round 5")
    r6: str = Field(description="Winning Side", alias="Round 6")
    r7: str = Field(description="Winning Side", alias="Round 7")
    r8: str = Field(description="Winning Side", alias="Round 8")
    r9: str = Field(description="Winning Side", alias="Round 9")
    r10: str = Field(description="Winning Side", alias="Round 10")
    r11: str = Field(description="Winning Side", alias="Round 11")
    r12: str = Field(description="Winning Side", alias="Round 12")
    r13: str = Field(description="Winning Side", alias="Round 13")
    r14: Optional[str] = Field(description="Winning Side", alias="Round 14")
    r15: Optional[str] = Field(description="Winning Side", alias="Round 15")
    r16: Optional[str] = Field(description="Winning Side", alias="Round 16")
    r17: Optional[str] = Field(description="Winning Side", alias="Round 17")
    r18: Optional[str] = Field(description="Winning Side", alias="Round 18")
    r19: Optional[str] = Field(description="Winning Side", alias="Round 19")
    r20: Optional[str] = Field(description="Winning Side", alias="Round 20")
    r21: Optional[str] = Field(description="Winning Side", alias="Round 21")
    r22: Optional[str] = Field(description="Winning Side", alias="Round 22")
    r23: Optional[str] = Field(description="Winning Side", alias="Round 23")
    r24: Optional[str] = Field(description="Winning Side", alias="Round 24")

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
