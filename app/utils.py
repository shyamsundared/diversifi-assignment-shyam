import os
import httpx
from dotenv import load_dotenv
from fastapi import HTTPException
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

async def analyze_sentiment(text: str) -> str:
    prompt = (
        f'Classify the sentiment of the following news headline about a company as "positive", "negative", or "neutral", '
        f'based on how the news is likely to affect its stock price in the short term.\n'
        f'Headline: "{text}"\n'
        f'Respond with exactly one word: positive, negative, or neutral.'
    )
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GOOGLE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(GEMINI_URL, headers=headers, json=payload)
            resp.raise_for_status()
            # Parse the result: ["candidates"][0]["content"]["parts"][0]["text"]
            candidates = resp.json().get("candidates", [])
            if candidates:
                content = candidates[0]["content"]["parts"][0]["text"].strip().lower()
                sentiment = content.strip('. ,!').split()[0]  # get first word, remove punctuation
                if sentiment in {"positive", "negative", "neutral"}:
                    return sentiment
            
        except Exception as e:
            print(f"Gemini API error: {e}")
            return "neutral"

RAPIDAPI_KEY=os.getenv("RAPIDAPI_KEY")
async def get_news(symbol: str):
    url = "https://news-api14.p.rapidapi.com/v2/search/articles"
    params = {"query": symbol, "language": "en"}
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "news-api14.p.rapidapi.com"
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
    except httpx.HTTPError:
        raise HTTPException(status_code=503, detail="News provider unavailable. Please try again later.")

    articles = response.json().get("data", [])
    if not articles:
        raise HTTPException(status_code=404, detail="No news found for the requested stock symbol.")

    headlines = []
    for article in articles[:3]:  # Limit to 3 articles
        title = article.get("title", "")
        sentiment = await analyze_sentiment(title)
        headlines.append({"title": title, "sentiment": sentiment})

    return headlines
