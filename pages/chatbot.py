import streamlit as st
import pandas as pd
import random
from difflib import get_close_matches

# =====================================================
# PAGE TITLE
# =====================================================

st.title("🤖 Tesla AI Chatbot")

st.markdown("""
Welcome to the Tesla AI Assistant.
Ask questions about Tesla stock prediction,
forecasting, models and project details.
""")

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        "data/TSLA.csv"
    )

    return df

df = load_data()

# =====================================================
# FEATURE CARDS
# =====================================================

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.info("📊 Dataset")

with col2:
    st.info("🤖 Models")

with col3:
    st.info("📈 Forecast")

with col4:
    st.info("💰 Insights")

with col5:
    st.info("🔮 Predictin")

# =====================================================
# DATASET OVERVIEW
# =====================================================

st.subheader("📊 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Rows",
        df.shape[0]
    )

with col2:

    st.metric(
        "Columns",
        df.shape[1]
    )

with col3:

    st.metric(
        "Highest Close",
        f"${df['Close'].max():.2f}"
    )

with col4:

    st.metric(
        "Latest Close",
        f"${df['Close'].iloc[-1]:.2f}"
    )

# =====================================================
# NEW CHAT
# =====================================================

col1, col2 = st.columns([5,1])

with col2:

    if st.button(
        "🧹 New Chat",
        use_container_width=True
    ):

        st.session_state.messages = [

            {
                "role": "assistant",

                "content": """
👋 Hello!

I am your Tesla AI Assistant.

Ask me anything about:

📊 Tesla Dataset

🤖 Model Performance

📈 Forecasting

💰 Stock Insights

🔮 Future Predictions
"""
            }

        ]

        st.rerun()

# =====================================================
# KNOWLEDGE BASE
# =====================================================

knowledge_base = {

    "best model":
    "best_model",

    "which model":
    "best_model",

    "highest accuracy":
    "best_model",

    "top model":
    "best_model",

    "dataset":
    "dataset",

    "data":
    "dataset",

    "tesla dataset":
    "dataset",

    "forecast":
    "forecast",

    "forecasting":
    "forecast",

    "prediction":
    "forecast",

    "future price":
    "forecast",

    "future stock":
    "forecast",

    "rnn":
    "rnn",

    "simple rnn":
    "rnn",

    "lstm":
    "lstm",

    "highest price":
    "highest_price",

    "max price":
    "highest_price",

    "lowest price":
    "lowest_price",

    "minimum price":
    "lowest_price",

    "close price":
    "close_price",

    "latest close":
    "close_price",

    "latest price":
    "close_price",

    "buy":
    "buy",

    "sell":
    "buy",

    "investment":
    "buy",

    "project":
    "project",

    "about project":
    "project",

    "rmse":
    "rmse",

    "mae":
    "mae",

    "r2":
    "r2",

    "r²":
    "r2",

    "deep learning":
    "deep_learning"
}

# =====================================================
# INITIAL CHAT MESSAGE
# =====================================================

if "messages" not in st.session_state:

    st.session_state.messages = [

        {
            "role": "assistant",

            "content": """
👋 Hello!

I am your Tesla AI Assistant.

Ask me anything about:

📊 Tesla Dataset

🤖 Model Performance

📈 Forecasting

💰 Stock Insights

🔮 Future Predictions
"""
        }

    ]

# =====================================================
# CHAT HISTORY
# =====================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

# =====================================================
# RANDOM QUESTIONS
# =====================================================

all_questions = [

    "Which model is best?",
    "Tell me about the dataset",
    "What is forecasting?",
    "What is RNN?",
    "What is LSTM?",
    "Highest Tesla price",
    "Lowest Tesla price",
    "Tell me about the project",
    "What is RMSE?",
    "What is MAE?",
    "What is R² Score?",
    "Latest Tesla closing price",
    "Why is SimpleRNN best?",
    "How many rows are in dataset?",
    "What is Deep Learning?"
]

if "random_questions" not in st.session_state:

    st.session_state.random_questions = random.sample(
        all_questions,
        8
    )
# =====================================================
# SUGGESTED QUESTIONS
# =====================================================

st.markdown("---")

st.subheader("💡 Suggested Questions")

col1, col2 = st.columns(2)

clicked_question = None

for i, q in enumerate(
    st.session_state.random_questions
):

    if i % 2 == 0:

        with col1:

            if st.button(
                q,
                key=f"q_{i}",
                use_container_width=True
            ):

                clicked_question = q

    else:

        with col2:

            if st.button(
                q,
                key=f"q_{i}",
                use_container_width=True
            ):

                clicked_question = q

if st.button(
    "🔄 Refresh Questions",
    use_container_width=True
):

    st.session_state.random_questions = random.sample(
        all_questions,
        8
    )

    st.rerun()

# =====================================================
# CHAT INPUT
# =====================================================

user_input = st.chat_input(
    "Ask anything about Tesla stock..."
)

prompt = None

if clicked_question:

    prompt = clicked_question

elif user_input:

    prompt = user_input

# =====================================================
# PROCESS USER MESSAGE
# =====================================================

if prompt:

    st.session_state.messages.append({

        "role": "user",

        "content": prompt

    })

    question = prompt.lower().strip()

    matched_intent = None

    # =====================================================
    # DIRECT MATCH
    # =====================================================

    for keyword, intent in knowledge_base.items():

        if keyword in question:

            matched_intent = intent

            break

    # =====================================================
    # FUZZY MATCH
    # =====================================================

    if matched_intent is None:

        matches = get_close_matches(

            question,

            knowledge_base.keys(),

            n=1,

            cutoff=0.4

        )

        if matches:

            matched_intent = knowledge_base[
                matches[0]
            ]

    # =====================================================
    # RESPONSE ENGINE
    # =====================================================

    if matched_intent == "best_model":

        answer = f"""
🏆 Best Model

SimpleRNN

Performance:

• R² Score : 97.42%

• RMSE : 11.69

• MAE : 7.90

SimpleRNN achieved the best
overall prediction accuracy.
"""

    elif matched_intent == "dataset":

        answer = f"""
📊 Tesla Dataset

Rows:
{df.shape[0]}

Columns:
{df.shape[1]}

Features:

• Date

• Open

• High

• Low

• Close

• Adj Close

• Volume

Target:

• Close Price
"""

    elif matched_intent == "rnn":

        answer = """
🤖 SimpleRNN

SimpleRNN is a Recurrent Neural Network.

It learns stock price patterns
from historical Tesla data and
predicts future prices.
"""

    elif matched_intent == "lstm":

        answer = """
🧠 LSTM

LSTM stands for
Long Short-Term Memory.

Advantages:

• Better memory

• Time-series forecasting

• Learns long-term patterns

Used for stock prediction tasks.
"""

    elif matched_intent == "forecast":

        answer = """
📈 Forecasting Module

Forecasts Available:

• 1 Day

• 5 Days

• 10 Days

Model Used:

SimpleRNN

Input:

Last 60 trading days

Output:

Future Tesla prices
"""

    elif matched_intent == "highest_price":

        highest_price = df["Close"].max()

        highest_date = df.loc[
            df["Close"].idxmax(),
            "Date"
        ]

        answer = f"""
📈 Highest Tesla Closing Price

Price:

${highest_price:.2f}

Date:

{highest_date}
"""

    elif matched_intent == "lowest_price":

        lowest_price = df["Close"].min()

        lowest_date = df.loc[
            df["Close"].idxmin(),
            "Date"
        ]

        answer = f"""
📉 Lowest Tesla Closing Price

Price:

${lowest_price:.2f}

Date:

{lowest_date}
"""

    elif matched_intent == "close_price":

        latest_price = df["Close"].iloc[-1]

        answer = f"""
💰 Latest Tesla Closing Price

${latest_price:.2f}
"""
    elif matched_intent == "rmse":

        answer = """
📉 RMSE

RMSE stands for

Root Mean Square Error

Purpose:

Measures prediction error.

Lower RMSE means
better model performance.

SimpleRNN RMSE:

11.69
"""

    elif matched_intent == "mae":

        answer = """
📊 MAE

MAE stands for

Mean Absolute Error

Purpose:

Measures average prediction error.

Lower MAE means
higher prediction accuracy.

SimpleRNN MAE:

7.90
"""

    elif matched_intent == "r2":

        answer = """
🎯 R² Score

R² measures how well
the model explains the data.

Range:

0 to 1

Higher is better.

SimpleRNN R² Score:

97.42%
"""

    elif matched_intent == "deep_learning":

        answer = """
🧠 Deep Learning

Deep Learning is a subset
of Machine Learning.

It uses Neural Networks
with multiple layers.

Models used in this project:

• SimpleRNN

• LSTM

These models learn historical
Tesla stock patterns and generate
future predictions.
"""

    elif matched_intent == "buy":

        answer = """
💡 Investment Guidance

This project provides analytical
forecasting only.

Before investing consider:

• Forecast Trend

• Market Conditions

• Risk Analysis

• Company Fundamentals

AI predictions should not be the
only factor in investment decisions.
"""

    elif matched_intent == "project":

        answer = """
📘 Tesla Stock Price Prediction

Project Modules:

📊 Dashboard

📈 EDA

🤖 Model Comparison

🔮 Prediction

📉 Forecasting

🤖 AI Assistant

Technologies:

• Python

• Streamlit

• TensorFlow

• Keras

• Scikit-Learn

• Plotly

• Pandas
"""

    else:

        answer = f"""
🤔 I couldn't fully understand:

"{prompt}"

Try asking:

• Which model is best?

• Tell me about the dataset

• What is forecasting?

• What is RNN?

• What is LSTM?

• What is RMSE?

• What is MAE?

• What is R² Score?

• Highest Tesla price

• Lowest Tesla price

• Tell me about the project
"""

    # =====================================================
    # SAVE RESPONSE
    # =====================================================

    st.session_state.messages.append({

        "role": "assistant",

        "content": answer

    })

    st.rerun()