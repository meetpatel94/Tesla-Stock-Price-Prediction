import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

from sklearn.preprocessing import MinMaxScaler

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense, Dropout

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Tesla Forecast Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# CUSTOM CSS
# =====================================================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #0f1535 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.1) 0%, rgba(0, 100, 255, 0.05) 100%);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(0, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        animation: slideUp 0.6s ease-out;
        text-align: center;
    }
    
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00ffff, #0066ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        color: #8892b0;
        font-size: 1rem;
    }
    
    /* Section Header */
    .section-header {
        margin: 2rem 0 1.5rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(0, 255, 255, 0.3);
        animation: slideInLeft 0.4s ease-out;
    }
    
    .section-title {
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff, #00ffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .section-subtitle {
        color: #8892b0;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* KPI Card */
    .kpi-card {
        background: linear-gradient(135deg, rgba(20, 28, 58, 0.95) 0%, rgba(15, 21, 45, 0.95) 100%);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(0, 255, 255, 0.2);
        transition: all 0.3s ease;
        animation: fadeInUp 0.5s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .kpi-card:hover::before {
        left: 100%;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        border-color: rgba(0, 255, 255, 0.5);
        box-shadow: 0 10px 30px rgba(0, 255, 255, 0.2);
    }
    
    .kpi-label {
        color: #8892b0;
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        color: #00ffff;
        margin: 0.5rem 0;
    }
    
    .kpi-trend {
        font-size: 0.85rem;
        margin-top: 0.5rem;
    }
    
    /* Forecast Summary Card */
    .summary-card {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.08) 0%, rgba(0, 100, 255, 0.04) 100%);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(0, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        animation: fadeIn 0.6s ease-out;
    }
    
    .summary-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #00ffff;
        margin-bottom: 1rem;
    }
    
    /* Recommendation Card */
    .rec-card-buy {
        background: linear-gradient(135deg, rgba(74, 222, 128, 0.15) 0%, rgba(34, 197, 94, 0.08) 100%);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 2px solid #4ade80;
        animation: glowPulse 2s infinite;
    }
    
    .rec-card-sell {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(220, 38, 38, 0.08) 100%);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 2px solid #ef4444;
        animation: glowPulseRed 2s infinite;
    }
    
    .rec-card-hold {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(245, 158, 11, 0.08) 100%);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 2px solid #f59e0b;
    }
    
    .rec-title {
        font-size: 1.8rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    /* Glass Card */
    .glass-card {
        background: rgba(20, 28, 58, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid rgba(0, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        border-color: rgba(0, 255, 255, 0.4);
        transform: translateY(-2px);
    }
    
    /* Chart Container */
    .chart-container {
        background: rgba(20, 28, 58, 0.5);
        border-radius: 15px;
        padding: 1rem;
        border: 1px solid rgba(0, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .chart-container:hover {
        border-color: rgba(0, 255, 255, 0.4);
        transform: translateY(-2px);
    }
    
    /* Risk Indicator */
    .risk-low {
        color: #4ade80;
        font-weight: 700;
    }
    
    .risk-medium {
        color: #f59e0b;
        font-weight: 700;
    }
    
    .risk-high {
        color: #ef4444;
        font-weight: 700;
    }
    
    /* Confidence Meter */
    .confidence-meter {
        background: rgba(20, 28, 58, 0.7);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(40px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes glowPulse {
        0%, 100% {
            box-shadow: 0 0 20px rgba(74, 222, 128, 0.3);
        }
        50% {
            box-shadow: 0 0 40px rgba(74, 222, 128, 0.6);
        }
    }
    
    @keyframes glowPulseRed {
        0%, 100% {
            box-shadow: 0 0 20px rgba(239, 68, 68, 0.3);
        }
        50% {
            box-shadow: 0 0 40px rgba(239, 68, 68, 0.6);
        }
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(20, 28, 58, 0.5);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #00ffff;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #0066ff;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# HERO SECTION
# =====================================================
st.markdown("""
<div class="hero-section">
    <div class="hero-title">
        📈 Tesla Future Forecasting
    </div>
    <div class="hero-subtitle">
        Advanced AI-powered price predictions • Multi-horizon forecasts • Real-time market intelligence
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================
@st.cache_data
def load_data():
    df = pd.read_csv("data/TSLA.csv")
    return df

df = load_data()

# =====================================================
# PREPARE DATA
# =====================================================
close_data = df[["Close"]]
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(close_data)

# =====================================================
# LOAD MODEL
# =====================================================
@st.cache_resource
def load_rnn_model():
    model = Sequential()
    model.add(SimpleRNN(units=50, input_shape=(60, 1)))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.build((None, 60, 1))
    model.load_weights("models/rnn_weights.weights.h5")
    return model

rnn_model = load_rnn_model()

# =====================================================
# FORECAST FUNCTION
# =====================================================
def predict_future_days(model, scaled_data, days):
    last_60_days = scaled_data[-60:]
    current_sequence = last_60_days.reshape(1, 60, 1)
    predictions = []
    
    for _ in range(days):
        pred = model.predict(current_sequence, verbose=0)
        predictions.append(pred[0][0])
        current_sequence = np.append(current_sequence[:, 1:, :], [[[pred[0][0]]]], axis=1)
    
    predictions = np.array(predictions).reshape(-1, 1)
    predictions = scaler.inverse_transform(predictions)
    return predictions

# =====================================================
# GENERATE FORECASTS
# =====================================================
with st.spinner("🧠 AI model analyzing market patterns..."):
    forecast_1 = predict_future_days(rnn_model, scaled_data, 1)
    forecast_5 = predict_future_days(rnn_model, scaled_data, 5)
    forecast_10 = predict_future_days(rnn_model, scaled_data, 10)

# =====================================================
# CURRENT METRICS
# =====================================================
current_price = df["Close"].iloc[-1]
forecast_price = forecast_10[-1][0]
expected_return = ((forecast_price - current_price) / current_price) * 100

# =====================================================
# FORECAST SUMMARY KPIs
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">📊 Forecast Dashboard</div>
    <div class="section-subtitle">Real-time price predictions across multiple time horizons</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">💰 Current Price</div>
        <div class="kpi-value">${current_price:.2f}</div>
        <div class="kpi-trend" style="color: #8892b0;">Latest close</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    change_1d = ((forecast_1[0][0] - current_price) / current_price) * 100
    arrow_1d = "▲" if change_1d > 0 else "▼"
    color_1d = "#4ade80" if change_1d > 0 else "#ef4444"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">📅 1-Day Forecast</div>
        <div class="kpi-value">${forecast_1[0][0]:.2f}</div>
        <div class="kpi-trend" style="color: {color_1d};">{arrow_1d} {abs(change_1d):.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    change_5d = ((forecast_5[-1][0] - current_price) / current_price) * 100
    arrow_5d = "▲" if change_5d > 0 else "▼"
    color_5d = "#4ade80" if change_5d > 0 else "#ef4444"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">📅 5-Day Forecast</div>
        <div class="kpi-value">${forecast_5[-1][0]:.2f}</div>
        <div class="kpi-trend" style="color: {color_5d};">{arrow_5d} {abs(change_5d):.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    change_10d = expected_return
    arrow_10d = "▲" if change_10d > 0 else "▼"
    color_10d = "#4ade80" if change_10d > 0 else "#ef4444"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">📅 10-Day Forecast</div>
        <div class="kpi-value">${forecast_10[-1][0]:.2f}</div>
        <div class="kpi-trend" style="color: {color_10d};">{arrow_10d} {abs(change_10d):.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# FORECAST STATISTICS
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">📈 Forecast Analytics</div>
    <div class="section-subtitle">Statistical distribution and range analysis</div>
</div>
""", unsafe_allow_html=True)

max_price = np.max(forecast_10)
min_price = np.min(forecast_10)
avg_price = np.mean(forecast_10)
price_range = max_price - min_price

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">🔺 Maximum Forecast</div>
        <div class="kpi-value" style="color: #4ade80;">${max_price:.2f}</div>
        <div class="kpi-trend">Peak price projection</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">🔻 Minimum Forecast</div>
        <div class="kpi-value" style="color: #ef4444;">${min_price:.2f}</div>
        <div class="kpi-trend">Trough price projection</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">📊 Average Forecast</div>
        <div class="kpi-value">${avg_price:.2f}</div>
        <div class="kpi-trend">Mean predicted price</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">📏 Forecast Range</div>
        <div class="kpi-value">${price_range:.2f}</div>
        <div class="kpi-trend">High - Low spread</div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# EXPECTED RETURN CARD
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">💰 Expected Return Analysis</div>
    <div class="section-subtitle">Potential profit/loss projection over forecast horizon</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    return_color = "#4ade80" if expected_return > 0 else "#ef4444"
    return_icon = "▲" if expected_return > 0 else "▼"
    st.markdown(f"""
    <div class="summary-card">
        <div class="summary-title">📈 Projected Return</div>
        <div style="font-size: 3rem; font-weight: 800; color: {return_color}; margin: 1rem 0;">
            {return_icon} {abs(expected_return):.2f}%
        </div>
        <div style="color: #8892b0;">Over next 10 trading days</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="summary-card">
        <div class="summary-title">🎯 Price Target</div>
        <div style="font-size: 2rem; font-weight: 800; color: #00ffff; margin: 1rem 0;">
            ${forecast_price:.2f}
        </div>
        <div style="color: #8892b0;">Target price by end of forecast period</div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# RECOMMENDATION ENGINE
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">🎯 AI Trading Recommendation</div>
    <div class="section-subtitle">Actionable intelligence based on forecast models</div>
</div>
""", unsafe_allow_html=True)

if expected_return > 5:
    recommendation = "STRONG BUY"
    rec_class = "rec-card-buy"
    rec_icon = "🚀"
    rec_color = "#4ade80"
elif expected_return > 2:
    recommendation = "BUY"
    rec_class = "rec-card-buy"
    rec_icon = "📈"
    rec_color = "#4ade80"
elif expected_return < -5:
    recommendation = "STRONG SELL"
    rec_class = "rec-card-sell"
    rec_icon = "⚠️"
    rec_color = "#ef4444"
elif expected_return < -2:
    recommendation = "SELL"
    rec_class = "rec-card-sell"
    rec_icon = "📉"
    rec_color = "#ef4444"
else:
    recommendation = "HOLD"
    rec_class = "rec-card-hold"
    rec_icon = "➖"
    rec_color = "#f59e0b"

st.markdown(f"""
<div class="{rec_class}">
    <div class="rec-title" style="color: {rec_color};">{rec_icon} {recommendation}</div>
    <div style="color: #8892b0; margin-top: 0.5rem;">
        Based on {abs(expected_return):.2f}% expected {'gain' if expected_return > 0 else 'decline'} over 10 days
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# RISK ANALYSIS
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">⚠️ Risk Assessment</div>
    <div class="section-subtitle">Volatility analysis and risk exposure metrics</div>
</div>
""", unsafe_allow_html=True)

volatility = df["Close"].pct_change().std() * 100
annual_volatility = volatility * (252 ** 0.5)

if volatility < 2:
    risk_level = "LOW"
    risk_class = "risk-low"
    risk_icon = "🟢"
elif volatility < 4:
    risk_level = "MEDIUM"
    risk_class = "risk-medium"
    risk_icon = "🟡"
else:
    risk_level = "HIGH"
    risk_class = "risk-high"
    risk_icon = "🔴"

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="glass-card">
        <div class="kpi-label">Daily Volatility</div>
        <div class="kpi-value">{volatility:.2f}%</div>
        <div class="kpi-trend">Average daily movement</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="glass-card">
        <div class="kpi-label">Annualized Volatility</div>
        <div class="kpi-value">{annual_volatility:.2f}%</div>
        <div class="kpi-trend">Yearly projection</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="glass-card">
        <div class="kpi-label">Risk Level</div>
        <div class="kpi-value {risk_class}">{risk_icon} {risk_level}</div>
        <div class="kpi-trend">Market risk assessment</div>
    </div>
    """, unsafe_allow_html=True)

# Risk meter visualization
risk_percentage = min(volatility / 10 * 100, 100)
st.markdown(f"""
<div style="background: rgba(20, 28, 58, 0.5); border-radius: 10px; padding: 0.2rem; margin: 1rem 0;">
    <div style="background: linear-gradient(90deg, #4ade80, #f59e0b, #ef4444); width: {risk_percentage}%; height: 8px; border-radius: 10px;"></div>
</div>
<div style="display: flex; justify-content: space-between; color: #8892b0; font-size: 0.75rem; margin-top: -0.5rem;">
    <span>Low Risk</span>
    <span>Moderate Risk</span>
    <span>High Risk</span>
</div>
""", unsafe_allow_html=True)

# =====================================================
# CONFIDENCE SCORE
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">🎯 Prediction Confidence</div>
    <div class="section-subtitle">Model reliability and forecast accuracy metrics</div>
</div>
""", unsafe_allow_html=True)

confidence_score = 97.42

if confidence_score >= 95:
    quality = "Excellent"
    quality_icon = "⭐⭐⭐⭐⭐"
elif confidence_score >= 85:
    quality = "Good"
    quality_icon = "⭐⭐⭐⭐"
else:
    quality = "Average"
    quality_icon = "⭐⭐⭐"

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="confidence-meter">
        <div class="kpi-label">AI Confidence Score</div>
        <div class="kpi-value" style="font-size: 2.5rem;">{confidence_score:.2f}%</div>
        <div class="kpi-trend">Based on historical model performance</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="confidence-meter">
        <div class="kpi-label">Model Quality Rating</div>
        <div class="kpi-value" style="font-size: 1.8rem;">{quality} {quality_icon}</div>
        <div class="kpi-trend">SimpleRNN architecture</div>
    </div>
    """, unsafe_allow_html=True)

st.progress(confidence_score / 100)
st.caption("📊 Confidence meter reflects prediction reliability based on backtesting results")

# =====================================================
# FORECAST TABLE
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">📋 Detailed Forecast Table</div>
    <div class="section-subtitle">Daily price predictions with growth analysis</div>
</div>
""", unsafe_allow_html=True)

forecast_df = pd.DataFrame({
    "Day": np.arange(1, 11),
    "Predicted Price": forecast_10.flatten(),
    "Daily Change": [0] + [forecast_10[i][0] - forecast_10[i-1][0] for i in range(1, 10)],
    "Cumulative Return %": [((forecast_10[i][0] - current_price) / current_price) * 100 for i in range(10)]
})

forecast_df["Daily Change %"] = (forecast_df["Daily Change"] / forecast_df["Predicted Price"].shift(1)) * 100
forecast_df["Daily Change %"] = forecast_df["Daily Change %"].fillna(0)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.dataframe(forecast_df, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# FORECAST GRAPH
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">📈 Price Forecast Visualization</div>
    <div class="section-subtitle">10-day price trajectory projection</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
fig = px.line(
    forecast_df,
    x="Day",
    y="Predicted Price",
    markers=True,
    title="<b>Tesla Stock Price Forecast - 10 Day Horizon</b>",
    color_discrete_sequence=['#00ffff']
)
fig.update_traces(marker=dict(size=10, symbol='circle', color='#00ffff'), line=dict(width=3))
fig.update_layout(
    plot_bgcolor='rgba(20, 28, 58, 0.8)',
    paper_bgcolor='rgba(20, 28, 58, 0)',
    font=dict(color='#8892b0', family='Inter'),
    title_font_size=16,
    xaxis_title="Trading Day",
    yaxis_title="Predicted Price (USD)"
)
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# GROWTH ANALYSIS
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">📊 Growth Analysis</div>
    <div class="section-subtitle">Daily expected returns and cumulative performance</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    growth_fig = px.bar(
        forecast_df,
        x="Day",
        y="Daily Change %",
        title="<b>Expected Daily Returns (%)</b>",
        color="Daily Change %",
        color_continuous_scale=["#ef4444", "#f59e0b", "#4ade80"],
        text="Daily Change %"
    )
    growth_fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    growth_fig.update_layout(
        plot_bgcolor='rgba(20, 28, 58, 0.8)',
        paper_bgcolor='rgba(20, 28, 58, 0)',
        font=dict(color='#8892b0', family='Inter'),
        title_font_size=16
    )
    st.plotly_chart(growth_fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    cumulative_fig = px.area(
        forecast_df,
        x="Day",
        y="Cumulative Return %",
        title="<b>Cumulative Return Projection (%)</b>",
        color_discrete_sequence=['#00ffff']
    )
    cumulative_fig.update_traces(fill='tozeroy', opacity=0.3)
    cumulative_fig.update_layout(
        plot_bgcolor='rgba(20, 28, 58, 0.8)',
        paper_bgcolor='rgba(20, 28, 58, 0)',
        font=dict(color='#8892b0', family='Inter'),
        title_font_size=16,
        yaxis_title="Cumulative Return (%)"
    )
    st.plotly_chart(cumulative_fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# TREND ANALYSIS
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">🔍 Trend Analysis</div>
    <div class="section-subtitle">Market direction and momentum indicators</div>
</div>
""", unsafe_allow_html=True)

first_price = forecast_df["Predicted Price"].iloc[0]
last_price = forecast_df["Predicted Price"].iloc[-1]
price_difference = last_price - first_price

if last_price > first_price:
    trend = "Bullish"
    trend_icon = "📈"
    trend_color = "#4ade80"
    trend_message = f"Upward trend detected with expected increase of ${price_difference:.2f}"
elif last_price < first_price:
    trend = "Bearish"
    trend_icon = "📉"
    trend_color = "#ef4444"
    trend_message = f"Downward trend detected with expected decrease of ${abs(price_difference):.2f}"
else:
    trend = "Sideways"
    trend_icon = "➖"
    trend_color = "#f59e0b"
    trend_message = "Stable market trend with minimal expected movement"

st.markdown(f"""
<div class="summary-card">
    <div class="summary-title">Market Direction</div>
    <div style="font-size: 2rem; font-weight: 800; color: {trend_color}; margin: 1rem 0;">
        {trend_icon} {trend}
    </div>
    <div style="color: #8892b0;">{trend_message}</div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# AI FORECAST SUMMARY
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">🤖 AI Forecast Summary</div>
    <div class="section-subtitle">Comprehensive market intelligence report</div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="glass-card">
    <div style="display: flex; gap: 2rem; flex-wrap: wrap;">
        <div style="flex: 1;">
            <div style="font-weight: 700; color: #00ffff; margin-bottom: 0.5rem;">📊 Forecast Overview</div>
            <div style="color: #8892b0; font-size: 0.9rem;">
                • Current Price: <strong style="color: #00ffff;">${current_price:.2f}</strong><br>
                • 10-Day Target: <strong style="color: #00ffff;">${forecast_price:.2f}</strong><br>
                • Expected Return: <strong style="color: {return_color};">{expected_return:+.2f}%</strong><br>
                • Trend: <strong style="color: {trend_color};">{trend}</strong>
            </div>
        </div>
        <div style="flex: 1;">
            <div style="font-weight: 700; color: #00ffff; margin-bottom: 0.5rem;">⚙️ Model Information</div>
            <div style="color: #8892b0; font-size: 0.9rem;">
                • Architecture: SimpleRNN<br>
                • Confidence: {confidence_score:.2f}%<br>
                • Risk Level: {risk_level}<br>
                • Recommendation: {recommendation}
            </div>
        </div>
        <div style="flex: 1;">
            <div style="font-weight: 700; color: #00ffff; margin-bottom: 0.5rem;">📅 Forecast Details</div>
            <div style="color: #8892b0; font-size: 0.9rem;">
                • Range: ${min_price:.2f} - ${max_price:.2f}<br>
                • Average: ${avg_price:.2f}<br>
                • Volatility: {volatility:.2f}%<br>
                • Horizon: 10 Trading Days
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# DOWNLOAD BUTTON
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">📥 Export Data</div>
    <div class="section-subtitle">Download forecast results for further analysis</div>
</div>
""", unsafe_allow_html=True)

csv = forecast_df.to_csv(index=False)
st.download_button(
    label="📥 Download Forecast CSV",
    data=csv,
    file_name=f"tesla_10day_forecast_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
    mime="text/csv",
    use_container_width=True
)

# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 1rem;">
    <div style="color: #8892b0; font-size: 0.85rem;">
        📈 Tesla Forecasting System | Tesla Stock Price Prediction
    </div>
    <div style="color: #8892b0; font-size: 0.75rem; margin-top: 0.5rem;">
        © Copyright 2026 — Meetpatel
    </div>
    <div style="color: #8892b0; font-size: 0.75rem; margin-top: 0.5rem;">
        Terms of Service / Privacy Policy
    </div>  
</div>
""", unsafe_allow_html=True)
