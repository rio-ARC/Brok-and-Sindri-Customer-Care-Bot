# Deployment Guide (Render)

Deploying the Huldra Brothers Support Bot to Render is simple.

## Prerequisites
- A [Render](https://render.com) account.
- The GitHub repository connected to your Render account.
- Your API Keys (`GROQ_API_KEY` and `TAVILY_API_KEY`).

## Step-by-Step Instructions

1. **New Web Service**
   - Go to your Render Dashboard.
   - Click **New +** and select **Web Service**.
   - Select the repository: `rio-ARC/Brok-and-Sindri-Customer-Care-Bot`.

2. **Configuration**
   - **Name:** `huldra-support-bot` (or similar)
   - **Region:** Choose the one closest to you.
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port 10000`

3. **Environment Variables**
   - Scroll down to the **Environment Variables** section.
   - Click **Add Environment Variable** for each key:
     - `GROQ_API_KEY`: Paste your key from `.env`.
     - `TAVILY_API_KEY`: Paste your key from `.env`.
     - `PYTHON_VERSION`: `3.11.0` (Optional, but good for stability).

4. **Deploy**
   - Click **Create Web Service**.
   - Render will start building. Watch the logs.
   - Once it says "Live", your bot is ready!

## Verifying Deployment
Your API URL will be something like `https://huldra-support-bot.onrender.com`.

- **Health Check:** Visit `https://huldra-support-bot.onrender.com/` in your browser. You should see the JSON status message.
- **Chat:** Send a POST request to `https://huldra-support-bot.onrender.com/chat`.
