# AI Investment Bot

A data-driven investment assistant that analyzes US stocks, generates **BUY/HOLD/SELL** signals, and provides an **AI chatbot** for natural language Q&A.

## Live Demo
[Click here to view the live app](https://avernlll-investment-bot.streamlit.app/)

## Features
- **Signal Engine**: Combines technical indicators (RSI, 50-day SMA) and fundamentals (P/E, Profit Margin) to generate actionable recommendations.
- **AI Chatbot**: Ask questions like *"Which stock performed best in the last 30 days?"* (Powered by DeepSeek API).
- **Interactive Dashboard**: View price charts, fundamentals, and statistics in real-time.

## Tech Stack
- **Frontend/UI**: Streamlit
- **Data**: Pandas, NumPy, yfinance (Yahoo Finance API)
- **AI**: DeepSeek API (OpenAI-compatible)
- **Visualization**: Matplotlib, Plotly
- **Deployment**: Streamlit Cloud
## Run Locally
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Avernlll/investment-bot.git
   cd investment-bot
2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
4. **Set up your API keys**:
   ```bash
   DEEPSEEK_API_KEY=your-key-here
5. **Run the app**:
   ```bash
   streamlit run app.py
## Author
Avernlll - https://github.com/Avernlll
