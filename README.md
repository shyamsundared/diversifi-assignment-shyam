# News Sentiment Analysis API

A FastAPI backend service that fetches news headlines for stocks/tickers and provides sentiment classification for each headline as well as an overall sentiment summary. The project uses AI-powered models to determine sentiment and stores results in a PostgreSQL database (Neon).

---

## 🚀 Features

- Fetches latest financial news headlines for stock symbols
- Performs sentiment analysis: positive, negative, or neutral
- Stores historical sentiment data in a PostgreSQL database
- Fully asynchronous using FastAPI and async HTTP requests
- Dockerized for easy deployment

---

## 📝 Setup Instructions

### 1. Clone the repository

git clone https://github.com/shyamsundared/diversifi-assignment-shyam.git

cd diversifi-assignment-shyam



### 2. Create and activate a Python virtual environment

**Windows**:
python -m venv venv
.\venv\Scripts\activate



**macOS/Linux**:
python3 -m venv venv
source venv/bin/activate



### 3. Install dependencies

pip install -r requirements.txt



### 4. Configure environment variables
copy .env.example and put in the your keys 
create .env file with these keys


postrgres database URL(This is for neon db)
while copying from connection string , make sure to remove the part after ssl=require.
DATABASE_URL=postgresql+asyncpg://<username>:<password>@<host>:<port>/<database>?ssl=require
GOOGLE_API_KEY=your_google_gemini_api_key
RAPIDAPI_KEY=your_rapidapi_key




---

### 5. Run locally

uvicorn app.main:app --reload



Your API will be running at `http://localhost:8000`

Access the interactive Swagger UI at:  
`http://localhost:8000/docs`

---

### 6. Run with Docker

Build the Docker image:

docker build -t news-sentiment-api .



Run a container with environment variables:

docker run -p 8000:8000 --env-file .env news-sentiment-api



---

## Sentiment Analysis

### News

-I used rapiAPI to fetch news

### Sentiment Analysis
- I used gemini api as it was free.

---

##  AI Tools Used

### Google Gemini API (Google AI)

- Utilizes Google Gemini’s Large Language Models (LLMs) to classify sentiment.
- Headlines are analyzed with prompts like:

  > *Classify the sentiment of the following news headline about a company as "positive", "negative", or "neutral" based on how the news affects its stock price.*

- Uses asynchronous HTTP calls (`httpx.AsyncClient`) to communicate with the Gemini REST API.
.



---
# How I used AI tools
I used perplexity to help me create boiler plate code for the schemas, for importing modules which were 
making the code cleaner, took help for debugging with tricky syntax but maintained a scalable design by 
separating the code into modules like database, logic,pydantic schema, routes .
I also added a rate limiter for the POST request at 5 requests/min to make it more scalable.
swagger ui was pretty helpful in debugging, I didnt need to use postman, I could hit the endpoint from /docs


## code details

- Fully asynchronous design for efficient API calls and database operations
- Modular code separation between news fetching, sentiment analysis, and database handling
- Includes a Dockerfile for containerized deployment
- Environment variables managed with `.env` for security and flexibility
- I have added rate limiter at 5 requests. Hitting the post end point 5 times, should return 429 error saying too many requests

---



## 🛡️ Security & Privacy

- All API keys and secrets are loaded securely from environment variables
- No sensitive information is logged or exposed by this service
- Designed to be deployed securely within your infrastructure or behind authentication layers

---
