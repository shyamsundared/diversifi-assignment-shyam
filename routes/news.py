from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta
from app.models import NewsSentiment
from app.database import get_db
from app.utils import get_news
from app.schemas import NewsSentimentRequest, NewsSentimentResponse
from app.limiter import limiter

router = APIRouter()

@router.post("/news-sentiment", response_model=NewsSentimentResponse)
@limiter.limit("5/minute")
async def news_sentiment(
    request: Request,                             # Required by SlowAPI rate limiter
    request_body: NewsSentimentRequest,
    db: AsyncSession = Depends(get_db)
):
    symbol = request_body.symbol.upper()
    now = datetime.utcnow()

    # 1. Check DB for recent sentiment (within last 10 minutes)
    res = await db.execute(
        select(NewsSentiment).where(
            (NewsSentiment.symbol == symbol) &
            (NewsSentiment.timestamp > now - timedelta(minutes=10))
        ).order_by(NewsSentiment.timestamp.desc())
    )
    db_obj = res.scalars().first()
    if db_obj:
        return NewsSentimentResponse(
            symbol=db_obj.symbol,
            timestamp=db_obj.timestamp,
            headlines=db_obj.headlines,
            overall_sentiment=getattr(db_obj, "overall_sentiment", None)  # Return if present
        )

    # 2. Fetch news + analyze sentiment
    headlines = await get_news(symbol)

    # 3. Compute overall sentiment (majority vote)
    sentiments = [h["sentiment"] for h in headlines]
    if sentiments:
        overall_sentiment = max(set(sentiments), key=sentiments.count)
    else:
        overall_sentiment = "neutral"

    # 4. Store in DB
    db_record = NewsSentiment(
        symbol=symbol,
        timestamp=now,
        headlines=headlines,
        overall_sentiment=overall_sentiment
    )
    db.add(db_record)
    await db.commit()
    await db.refresh(db_record)

    # 5. Return response
    return NewsSentimentResponse(
        symbol=symbol,
        timestamp=db_record.timestamp,
        headlines=db_record.headlines,
        overall_sentiment=db_record.overall_sentiment
    )
