import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Tesla Stockkkk Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
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
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00ffff, #0066ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        color: #8892b0;
        font-size: 1.1rem;
    }
    
    /* KPI Card Styles */
    .kpi-card {
        background: linear-gradient(135deg, rgba(20, 28, 58, 0.9) 0%, rgba(15, 21, 45, 0.9) 100%);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(0, 255, 255, 0.15);
        backdrop-filter: blur(10px);
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
        border-color: rgba(0, 255, 255, 0.4);
        box-shadow: 0 10px 30px rgba(0, 255, 255, 0.2);
    }
    
    .kpi-label {
        color: #8892b0;
        font-size: 0.9rem;
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
        color: #4ade80;
    }
    
    /* Glassmorphism Card */
    .glass-card {
        background: rgba(20, 28, 58, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(0, 255, 255, 0.2);
        transition: all 0.3s ease;
        animation: fadeIn 0.6s ease-out;
    }
    
    .glass-card:hover {
        border-color: rgba(0, 255, 255, 0.4);
        box-shadow: 0 5px 20px rgba(0, 255, 255, 0.1);
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
    
    /* Insight Card */
    .insight-card {
        background: linear-gradient(135deg, rgba(74, 222, 128, 0.1) 0%, rgba(34, 197, 94, 0.05) 100%);
        border-radius: 12px;
        padding: 1rem;
        border-left: 4px solid #4ade80;
        margin: 1rem 0;
        animation: fadeInRight 0.5s ease-out;
    }
    
    /* Recommendation Card */
    .rec-card {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.1) 0%, rgba(0, 100, 255, 0.05) 100%);
        border-radius: 12px;
        padding: 1rem;
        border-right: 4px solid #00ffff;
        margin: 1rem 0;
        animation: fadeInLeft 0.5s ease-out;
    }
    
    /* Risk Card */
    .risk-card {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.05) 100%);
        border-radius: 12px;
        padding: 1rem;
        border-left: 4px solid #ef4444;
        margin: 1rem 0;
        animation: fadeInRight 0.5s ease-out;
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
    
    @keyframes fadeInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes fadeInRight {
        from {
            opacity: 0;
            transform: translateX(20px);
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
    
    @keyframes glowPulse {
        0%, 100% {
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
        }
        50% {
            box-shadow: 0 0 30px rgba(0, 255, 255, 0.4);
        }
    }
    
    /* Loading Animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 2px solid rgba(0, 255, 255, 0.3);
        border-radius: 50%;
        border-top-color: #00ffff;
        animation: spin 0.6s linear infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Metric Container */
    .metric-container {
        background: rgba(20, 28, 58, 0.5);
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    /* Dataframe Styling */
    .stDataFrame {
        background: rgba(20, 28, 58, 0.5);
        border-radius: 10px;
        border: 1px solid rgba(0, 255, 255, 0.2);
    }
    
    /* Plotly Chart Styling */
    .stPlotlyChart {
        background: rgba(20, 28, 58, 0.5);
        border-radius: 15px;
        padding: 0.5rem;
        border: 1px solid rgba(0, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .stPlotlyChart:hover {
        border-color: rgba(0, 255, 255, 0.4);
        transform: translateY(-2px);
    }
    
    /* Custom Button Hover */
    div.stButton > button {
        background: linear-gradient(135deg, #00ffff, #0066ff);
        color: white;
        border: none;
        transition: transform 0.3s ease;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 255, 255, 0.3);
    }
    
    /* Scrollbar Styling */
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

# --------------------------------------------------
# LOAD DATA WITH LOADING ANIMATION
# --------------------------------------------------
@st.cache_data
def load_data():
    with st.spinner(''):
        placeholder = st.empty()
        placeholder.markdown('<div class="loading-spinner"></div> Loading Tesla stock data...', unsafe_allow_html=True)
        df = pd.read_csv("data/TSLA.csv")
        df["Date"] = pd.to_datetime(df["Date"])
        placeholder.empty()
        return df

df = load_data()

# --------------------------------------------------
# DATA PREPARATION
# --------------------------------------------------
latest_close = df["Close"].iloc[-1]
highest_close = df["Close"].max()
lowest_close = df["Close"].min()
avg_volume = df["Volume"].mean()

# Calculate price change
price_change = latest_close - df["Close"].iloc[-2]
price_change_pct = (price_change / df["Close"].iloc[-2]) * 100

# Moving Averages
df["MA50"] = df["Close"].rolling(50).mean()
df["MA200"] = df["Close"].rolling(200).mean()

# Current price vs moving averages
vs_ma50 = ((latest_close - df["MA50"].iloc[-1]) / df["MA50"].iloc[-1]) * 100
vs_ma200 = ((latest_close - df["MA200"].iloc[-1]) / df["MA200"].iloc[-1]) * 100

# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------
st.markdown("""
<div class="hero-section">
    <div class="hero-title">
        🚀 Tesla Stock Dashboard
    </div>
    <div class="hero-subtitle">
        Real-time market analytics & trading insights | Premium Financial Intelligence Platform
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# KPI CARDS SECTION
# --------------------------------------------------
st.markdown("""
<div class="section-header">
    <div class="section-title">📊 Market Overview</div>
    <div class="section-subtitle">Key performance indicators and real-time metrics</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    trend_icon = "📈" if price_change > 0 else "📉"
    trend_color = "#4ade80" if price_change > 0 else "#ef4444"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Latest Close Price</div>
        <div class="kpi-value">${latest_close:.2f}</div>
        <div class="kpi-trend">{trend_icon} {price_change:+.2f} ({price_change_pct:+.2f}%)</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">52-Week High</div>
        <div class="kpi-value">${highest_close:.2f}</div>
        <div class="kpi-trend">📊 All-time peak</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">52-Week Low</div>
        <div class="kpi-value">${lowest_close:.2f}</div>
        <div class="kpi-trend">📊 Support level</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Average Daily Volume</div>
        <div class="kpi-value">{avg_volume:,.0f}</div>
        <div class="kpi-trend">📊 Liquidity indicator</div>
    </div>
    """, unsafe_allow_html=True)

# Additional metrics row
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="glass-card">
        <div class="kpi-label">vs 50-Day MA</div>
        <div class="kpi-value" style="color: {'#4ade80' if vs_ma50 > 0 else '#ef4444'}">{vs_ma50:+.2f}%</div>
        <div class="kpi-trend">Moving average comparison</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="glass-card">
        <div class="kpi-label">vs 200-Day MA</div>
        <div class="kpi-value" style="color: {'#4ade80' if vs_ma200 > 0 else '#ef4444'}">{vs_ma200:+.2f}%</div>
        <div class="kpi-trend">Moving average comparison</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="glass-card">
        <div class="kpi-label">Trading Session</div>
        <div class="kpi-value" style="font-size: 1.5rem">{datetime.now().strftime('%Y-%m-%d')}</div>
        <div class="kpi-trend">Last updated: {datetime.now().strftime('%H:%M:%S')}</div>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# DATASET OVERVIEW
# --------------------------------------------------
st.markdown("""
<div class="section-header">
    <div class="section-title">📋 Dataset Information</div>
    <div class="section-subtitle">Raw data structure and sample records</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="glass-card">
        <div class="kpi-label">Total Records</div>
        <div class="kpi-value" style="font-size: 1.8rem">{df.shape[0]:,}</div>
        <div class="kpi-trend">Trading days</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="glass-card">
        <div class="kpi-label">Total Features</div>
        <div class="kpi-value" style="font-size: 1.8rem">{df.shape[1]}</div>
        <div class="kpi-trend">OHLC + Volume + MAs</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="metric-container">', unsafe_allow_html=True)
st.dataframe(df.head(), use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# CLOSING PRICE CHART
# --------------------------------------------------
st.markdown("""
<div class="section-header">
    <div class="section-title">📈 Price Action Analysis</div>
    <div class="section-subtitle">Tesla closing price trend over time</div>
</div>
""", unsafe_allow_html=True)

fig1 = px.line(
    df,
    x="Date",
    y="Close",
    title="<b>Tesla Closing Price Evolution</b>"
)

fig1.update_layout(
    xaxis_title="Date",
    yaxis_title="Close Price (USD)",
    title_font_size=16,
    plot_bgcolor='rgba(20, 28, 58, 0.8)',
    paper_bgcolor='rgba(20, 28, 58, 0)',
    font=dict(color='#8892b0', family='Inter'),
    hovermode='x unified',
    showlegend=True
)

fig1.update_traces(line=dict(color='#00ffff', width=2))

st.plotly_chart(fig1, use_container_width=True)

# --------------------------------------------------
# MOVING AVERAGES
# --------------------------------------------------
st.markdown("""
<div class="section-header">
    <div class="section-title">📊 Technical Indicators</div>
    <div class="section-subtitle">Moving average crossover analysis</div>
</div>
""", unsafe_allow_html=True)

fig2 = go.Figure()

fig2.add_trace(
    go.Scatter(
        x=df["Date"],
        y=df["Close"],
        name="Close Price",
        line=dict(color='#00ffff', width=2)
    )
)

fig2.add_trace(
    go.Scatter(
        x=df["Date"],
        y=df["MA50"],
        name="50-Day MA",
        line=dict(color='#f59e0b', width=2, dash='dash')
    )
)

fig2.add_trace(
    go.Scatter(
        x=df["Date"],
        y=df["MA200"],
        name="200-Day MA",
        line=dict(color='#ef4444', width=2, dash='dash')
    )
)

fig2.update_layout(
    title="<b>Moving Average Comparison - Golden Cross Analysis</b>",
    xaxis_title="Date",
    yaxis_title="Price (USD)",
    title_font_size=16,
    plot_bgcolor='rgba(20, 28, 58, 0.8)',
    paper_bgcolor='rgba(20, 28, 58, 0)',
    font=dict(color='#8892b0', family='Inter'),
    hovermode='x unified',
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01,
        bgcolor='rgba(0,0,0,0.5)'
    )
)

st.plotly_chart(fig2, use_container_width=True)

# --------------------------------------------------
# VOLUME CHART
# --------------------------------------------------
st.markdown("""
<div class="section-header">
    <div class="section-title">📦 Volume Analysis</div>
    <div class="section-subtitle">Trading volume and liquidity metrics</div>
</div>
""", unsafe_allow_html=True)

fig3 = px.bar(
    df,
    x="Date",
    y="Volume",
    title="<b>Tesla Daily Trading Volume</b>",
    color_discrete_sequence=['#00ffff']
)

fig3.update_layout(
    xaxis_title="Date",
    yaxis_title="Volume (Shares)",
    title_font_size=16,
    plot_bgcolor='rgba(20, 28, 58, 0.8)',
    paper_bgcolor='rgba(20, 28, 58, 0)',
    font=dict(color='#8892b0', family='Inter'),
    hovermode='x unified'
)

fig3.update_traces(opacity=0.8, marker_line_width=0)

st.plotly_chart(fig3, use_container_width=True)

# --------------------------------------------------
# INSIGHTS & RECOMMENDATIONS
# --------------------------------------------------
st.markdown("""
<div class="section-header">
    <div class="section-title">💡 Market Intelligence</div>
    <div class="section-subtitle">AI-powered insights and trading recommendations</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="insight-card">
        <div style="font-weight: 700; color: #4ade80; margin-bottom: 0.5rem;">📈 BULLISH SIGNALS</div>
        <div style="color: #ffffff;">• Price is {'above' if vs_ma50 > 0 else 'below'} 50-day MA by {abs(vs_ma50):.2f}%</div>
        <div style="color: #ffffff;">• Current trend shows {'positive' if price_change > 0 else 'negative'} momentum</div>
        <div style="color: #ffffff;">• {'Strong' if avg_volume > df["Volume"].median() else 'Moderate'} trading volume detected</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="rec-card">
        <div style="font-weight: 700; color: #00ffff; margin-bottom: 0.5rem;">🎯 TRADING RECOMMENDATION</div>
        <div style="color: #ffffff;">• Strategy: {'BUY on dips' if vs_ma50 > 0 else 'ACCUMULATE at support'}</div>
        <div style="color: #ffffff;">• Risk Level: {'MEDIUM' if abs(vs_ma50) < 15 else 'HIGH'}</div>
        <div style="color: #ffffff;">• Target: Consider {'long-term' if vs_ma200 > 0 else 'short-term'} position</div>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# RISK ASSESSMENT
# --------------------------------------------------
st.markdown("""
<div class="section-header">
    <div class="section-title">⚠️ Risk Analysis</div>
    <div class="section-subtitle">Volatility assessment and risk metrics</div>
</div>
""", unsafe_allow_html=True)

volatility = df["Close"].pct_change().std() * (252 ** 0.5)  # Annualized volatility
daily_volatility = df["Close"].pct_change().std()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="risk-card">
        <div class="kpi-label">Annualized Volatility</div>
        <div class="kpi-value" style="font-size: 1.5rem; color: {'#ef4444' if volatility > 0.4 else '#f59e0b'}">{volatility:.2%}</div>
        <div class="kpi-trend">{'HIGH' if volatility > 0.4 else 'MODERATE'} risk level</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="risk-card">
        <div class="kpi-label">Daily Volatility</div>
        <div class="kpi-value" style="font-size: 1.5rem">{daily_volatility:.2%}</div>
        <div class="kpi-trend">Expected daily movement</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    max_drawdown = ((df["Close"].cummax() - df["Close"]) / df["Close"].cummax()).max()
    st.markdown(f"""
    <div class="risk-card">
        <div class="kpi-label">Max Drawdown</div>
        <div class="kpi-value" style="font-size: 1.5rem; color: '#ef4444'">{max_drawdown:.2%}</div>
        <div class="kpi-trend">Historical peak-to-trough decline</div>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# RECENT DATA
# --------------------------------------------------
st.markdown("""
<div class="section-header">
    <div class="section-title">🕒 Recent Transactions</div>
    <div class="section-subtitle">Latest 10 trading records</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="metric-container">', unsafe_allow_html=True)
st.dataframe(df.tail(10), use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("""
<div style="text-align: center; padding: 2rem; margin-top: 2rem; border-top: 1px solid rgba(0, 255, 255, 0.2);">
    <div style="color: #8892b0; font-size: 0.85rem;">
        📊 Tesla Stock Dashboard | Tesla Stock Price Prediction
    </div>
    <div style="color: #8892b0; font-size: 0.75rem; margin-top: 0.5rem;">
        © Copyright 2026 — Meetpatel
    </div>
    <div style="color: #8892b0; font-size: 0.75rem; margin-top: 0.5rem;">
        Terms of Service / Privacy Policy
    </div>
</div>
""", unsafe_allow_html=True)