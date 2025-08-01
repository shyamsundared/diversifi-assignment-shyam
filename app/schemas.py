from pydantic import BaseModel
from typing import List
from datetime import datetime

class HeadlineSentiment(BaseModel):
    title: str
    sentiment: str

class NewsSentimentResponse(BaseModel):
    symbol: str
    timestamp: datetime
    headlines: List[HeadlineSentiment]
    overall_sentiment: str | None = None
class NewsSentimentRequest(BaseModel):
    symbol: str