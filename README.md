# News Sentiment Analysis API

A FastAPI backend service that fetches news headlines for stocks/tickers and provides sentiment classification for each headline as well as an overall sentiment summary. The project uses AI-powered models to determine sentiment and stores results in a PostgreSQL database (e.g., Neon).

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

text

### 2. Create and activate a Python virtual environment

**Windows**:
python -m venv venv
.\venv\Scripts\activate

text

**macOS/Linux**:
python3 -m venv venv
source venv/bin/activate

text

### 3. Install dependencies

pip install -r requirements.txt

text

### 4. Configure environment variables

Copy the example environment file and update it with your own keys:

cp .env.example .env

text

Edit the `.env` file to set your environment-specific values, for example:
postrgres database URL(This is for neon db)
DATABASE_URL=postgresql+asyncpg://<username>:<password>@<host>:<port>/<database>?ssl=require

# Your Google Gemini API key for sentiment analysis
GOOGLE_API_KEY=your_google_gemini_api_key

# API key for your news source (e.g., RapidAPI)
RAPIDAPI_KEY=your_rapidapi_key
text

> **Note:** Never commit your real API keys or secrets to public repos.

---

### 5. Run locally

uvicorn app.main:app --reload

text

Your API will be running at `http://localhost:8000`

Access the interactive Swagger UI at:  
`http://localhost:8000/docs`

---

### 6. Run with Docker

Build the Docker image:

docker build -t news-sentiment-api .

text

Run a container with environment variables:

docker run -p 8000:8000 --env-file .env news-sentiment-api

text

---

## 📰 News Source & Sentiment Analysis

### News

- The app fetches news headlines using a reliable financial news API (such as RapidAPI or other aggregators).
- Headlines are fetched based on the stock ticker symbols provided to the API.

### Sentiment Analysis

- Sentiment is categorized as **positive**, **negative**, or **neutral**.
- The sentiment is intended to reflect how news may impact stock prices shortly after publication.

---

## 🤖 AI Tools Used

### Google Gemini API (Google AI)

- Utilizes Google Gemini’s Large Language Models (LLMs) to classify sentiment.
- Headlines are analyzed with prompts like:

  > *Classify the sentiment of the following news headline about a company as "positive", "negative", or "neutral" based on how the news affects its stock price.*

- Uses asynchronous HTTP calls (`httpx.AsyncClient`) to communicate with the Gemini REST API.
- Handles API errors gracefully by defaulting to `"neutral"` sentiment if needed.

### Alternatives Supported or Extensible

- Hugging Face Transformers models (e.g. `distilbert-base-uncased-finetuned-sst-2-english`)
- Local sentiment analyzers such as VADER for testing or smaller workloads
- Easily adaptable to other AI providers like Anthropic Claude, Cohere, or IBM Watson with minor changes

---

## 📚 Code Highlights

- Fully asynchronous design for efficient API calls and database operations
- Modular code separation between news fetching, sentiment analysis, and database handling
- Includes a Dockerfile for containerized deployment
- Environment variables managed with `.env` for security and flexibility

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for:

- Support for additional news APIs or data sources
- Integration with new AI/sentiment providers
- Performance enhancements and caching strategies
- Improved documentation or tests

---

## 🛡️ Security & Privacy

- All API keys and secrets are loaded securely from environment variables
- No sensitive information is logged or exposed by this service
- Designed to be deployed securely within your infrastructure or behind authentication layers

---
