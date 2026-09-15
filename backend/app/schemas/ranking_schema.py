from pydantic import BaseModel

class RankingEntry(BaseModel):
    nickname: str
    puntos_total: int

class RankingResponse(BaseModel):
    ranking: list[RankingEntry]
    total: int