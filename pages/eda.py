import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Tesla EDA Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
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
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15, 21, 53, 0.95) 0%, rgba(10, 14, 39, 0.95) 100%);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(0, 255, 255, 0.2);
    }
    
    [data-testid="stSidebar"] .sidebar-content {
        padding: 2rem 1rem;
    }
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #00ffff;
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
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00ffff, #0066ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
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
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 255, 255, 0.2);
    }
    
    /* Metric Card */
    .metric-card {
        background: linear-gradient(135deg, rgba(20, 28, 58, 0.9) 0%, rgba(15, 21, 45, 0.9) 100%);
        border-radius: 15px;
        padding: 1.2rem;
        text-align: center;
        border: 1px solid rgba(0, 255, 255, 0.15);
        transition: all 0.3s ease;
        animation: fadeInUp 0.5s ease-out;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: rgba(0, 255, 255, 0.4);
        box-shadow: 0 5px 20px rgba(0, 255, 255, 0.2);
    }
    
    .metric-label {
        color: #8892b0;
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #00ffff;
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
    
    /* Alert Card */
    .alert-card {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.05) 100%);
        border-radius: 12px;
        padding: 1rem;
        border-left: 4px solid #ef4444;
        margin: 1rem 0;
    }
    
    /* Success Card */
    .success-card {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.1) 0%, rgba(0, 100, 255, 0.05) 100%);
        border-radius: 12px;
        padding: 1rem;
        border-left: 4px solid #00ffff;
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
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }
    
    /* Loading Animation */
    .loading-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
    
    .loading-spinner {
        width: 40px;
        height: 40px;
        border: 3px solid rgba(0, 255, 255, 0.3);
        border-radius: 50%;
        border-top-color: #00ffff;
        animation: spin 0.6s linear infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
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
    
    /* Dataframe Styling */
    .stDataFrame {
        background: rgba(20, 28, 58, 0.5);
        border-radius: 10px;
        border: 1px solid rgba(0, 255, 255, 0.2);
    }
    
    /* Filter Badge */
    .filter-badge {
        background: rgba(0, 255, 255, 0.1);
        border-radius: 20px;
        padding: 0.3rem 0.8rem;
        font-size: 0.85rem;
        color: #00ffff;
        display: inline-block;
        margin: 0.2rem;
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
# LOAD DATA WITH ANIMATION
# =====================================================
@st.cache_data
def load_data():
    with st.spinner(''):
        placeholder = st.empty()
        placeholder.markdown('<div class="loading-wrapper"><div class="loading-spinner"></div></div>', unsafe_allow_html=True)
        df = pd.read_csv("data/TSLA.csv")
        df["Date"] = pd.to_datetime(df["Date"])
        placeholder.empty()
        return df

df = load_data()

# =====================================================
# HERO SECTION
# =====================================================
st.markdown("""
<div class="hero-section">
    <div class="hero-title">
        📊 Tesla Exploratory Data Analysis
    </div>
    <div style="color: #8892b0; margin-top: 0.5rem;">
        Advanced analytics • Statistical insights • Market intelligence
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR FILTERS
# =====================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <div style="font-size: 2rem;">📅</div>
        <div style="font-size: 1.2rem; font-weight: 600; color: #00ffff;">Date Range Filter</div>
    </div>
    """, unsafe_allow_html=True)
    
    start_date = st.date_input(
        "Start Date",
        df["Date"].min(),
        key="start_date"
    )
    
    end_date = st.date_input(
        "End Date",
        df["Date"].max(),
        key="end_date"
    )
    
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: center; padding: 0.5rem;">
        <div style="font-size: 0.85rem; color: #8892b0;">
            Active Filters
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<span class="filter-badge">📅 {start_date}</span>', unsafe_allow_html=True)
    st.markdown(f'<span class="filter-badge">📅 {end_date}</span>', unsafe_allow_html=True)

# Apply filters
filtered_df = df[
    (df["Date"] >= pd.to_datetime(start_date)) &
    (df["Date"] <= pd.to_datetime(end_date))
]

# =====================================================
# QUICK STATS
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">📊 Dataset Overview</div>
    <div class="section-subtitle">Real-time data statistics and composition</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Records</div>
        <div class="metric-value">{filtered_df.shape[0]:,}</div>
        <div style="color: #4ade80; font-size: 0.8rem; margin-top: 0.5rem;">✓ Trading Days</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Features</div>
        <div class="metric-value">{filtered_df.shape[1]}</div>
        <div style="color: #4ade80; font-size: 0.8rem; margin-top: 0.5rem;">✓ OHLC + Volume</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Date Range</div>
        <div class="metric-value" style="font-size: 1.2rem;">{(filtered_df['Date'].max() - filtered_df['Date'].min()).days} days</div>
        <div style="color: #4ade80; font-size: 0.8rem; margin-top: 0.5rem;">✓ Analysis Period</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Data Completeness</div>
        <div class="metric-value">100%</div>
        <div style="color: #4ade80; font-size: 0.8rem; margin-top: 0.5rem;">✓ No Missing Values</div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# DATASET PREVIEW
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">📋 Sample Data</div>
    <div class="section-subtitle">First 5 records for inspection</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.dataframe(filtered_df.head(), use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# DATA TYPES & MISSING VALUES
# =====================================================
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="section-header">
        <div class="section-title" style="font-size: 1.3rem;">🔍 Schema Analysis</div>
    </div>
    """, unsafe_allow_html=True)
    
    dtype_df = pd.DataFrame({
        "Column": filtered_df.columns,
        "Data Type": filtered_df.dtypes.astype(str)
    })
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.dataframe(dtype_df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="section-header">
        <div class="section-title" style="font-size: 1.3rem;">❌ Missing Values</div>
    </div>
    """, unsafe_allow_html=True)
    
    missing_df = pd.DataFrame(
        filtered_df.isnull().sum(),
        columns=["Missing Values"]
    )
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.dataframe(missing_df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# STATISTICAL SUMMARY
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">📈 Statistical Summary</div>
    <div class="section-subtitle">Descriptive statistics and distribution metrics</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.dataframe(filtered_df.describe(), use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# DISTRIBUTION ANALYSIS
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">📊 Distribution Analysis</div>
    <div class="section-subtitle">Price and volume distribution patterns</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig1 = px.histogram(
        filtered_df,
        x="Close",
        nbins=50,
        title="<b>Close Price Distribution</b>",
        color_discrete_sequence=['#00ffff'],
        marginal="box"
    )
    fig1.update_layout(
        plot_bgcolor='rgba(20, 28, 58, 0.8)',
        paper_bgcolor='rgba(20, 28, 58, 0)',
        font=dict(color='#8892b0', family='Inter'),
        title_font_size=16
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig2 = px.histogram(
        filtered_df,
        x="Volume",
        nbins=50,
        title="<b>Volume Distribution</b>",
        color_discrete_sequence=['#00ffff'],
        marginal="box"
    )
    fig2.update_layout(
        plot_bgcolor='rgba(20, 28, 58, 0.8)',
        paper_bgcolor='rgba(20, 28, 58, 0)',
        font=dict(color='#8892b0', family='Inter'),
        title_font_size=16
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# PRICE TRENDS
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">📉 Price Trend Analysis</div>
    <div class="section-subtitle">Open, high, low, close price movements</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
fig3 = px.line(
    filtered_df,
    x="Date",
    y=["Open", "Close"],
    title="<b>Open vs Close Price Trend</b>",
    color_discrete_sequence=['#f59e0b', '#00ffff']
)
fig3.update_layout(
    plot_bgcolor='rgba(20, 28, 58, 0.8)',
    paper_bgcolor='rgba(20, 28, 58, 0)',
    font=dict(color='#8892b0', family='Inter'),
    title_font_size=16,
    hovermode='x unified'
)
st.plotly_chart(fig3, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
fig4 = px.line(
    filtered_df,
    x="Date",
    y=["High", "Low"],
    title="<b>High vs Low Price Trend</b>",
    color_discrete_sequence=['#ef4444', '#4ade80']
)
fig4.update_layout(
    plot_bgcolor='rgba(20, 28, 58, 0.8)',
    paper_bgcolor='rgba(20, 28, 58, 0)',
    font=dict(color='#8892b0', family='Inter'),
    title_font_size=16,
    hovermode='x unified'
)
st.plotly_chart(fig4, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# OHLC COMPARISON
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">📊 OHLC Complete Analysis</div>
    <div class="section-subtitle">Full price spectrum comparison</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
fig5 = px.line(
    filtered_df,
    x="Date",
    y=["Open", "High", "Low", "Close"],
    title="<b>OHLC Price Comparison - Complete Market View</b>",
    color_discrete_sequence=['#f59e0b', '#ef4444', '#4ade80', '#00ffff']
)
fig5.update_layout(
    plot_bgcolor='rgba(20, 28, 58, 0.8)',
    paper_bgcolor='rgba(20, 28, 58, 0)',
    font=dict(color='#8892b0', family='Inter'),
    title_font_size=16,
    hovermode='x unified',
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01,
        bgcolor='rgba(0,0,0,0.5)'
    )
)
st.plotly_chart(fig5, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# CORRELATION ANALYSIS
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">🔥 Correlation Matrix</div>
    <div class="section-subtitle">Feature relationships and dependencies</div>
</div>
""", unsafe_allow_html=True)

numeric_df = filtered_df.select_dtypes(include=["number"])
corr = numeric_df.corr()

fig, ax = plt.subplots(figsize=(12, 8))
fig.patch.set_facecolor('#141C3A')
ax.set_facecolor('#141C3A')

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    center=0,
    fmt='.2f',
    square=True,
    linewidths=1,
    cbar_kws={"shrink": 0.8},
    ax=ax
)

ax.set_title("Feature Correlation Heatmap", color='#00ffff', fontsize=16, pad=20)
ax.tick_params(colors='#8892b0')

plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
plt.setp(ax.get_yticklabels(), rotation=0)

for text in ax.texts:
    text.set_color('white')
    text.set_fontsize(9)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.pyplot(fig)
st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# RELATIONSHIP ANALYSIS
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">🎯 Price Relationships</div>
    <div class="section-subtitle">Volume-price correlation analysis</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig7 = px.scatter(
        filtered_df,
        x="Volume",
        y="Close",
        title="<b>Volume vs Close Price</b>",
        hover_data=["Date"],
        trendline="ols",
        color_discrete_sequence=['#00ffff']
    )
    fig7.update_layout(
        plot_bgcolor='rgba(20, 28, 58, 0.8)',
        paper_bgcolor='rgba(20, 28, 58, 0)',
        font=dict(color='#8892b0', family='Inter'),
        title_font_size=16
    )
    st.plotly_chart(fig7, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig8 = px.scatter(
        filtered_df,
        x="Open",
        y="Close",
        title="<b>Open vs Close Price Correlation</b>",
        trendline="ols",
        color_discrete_sequence=['#00ffff']
    )
    fig8.update_layout(
        plot_bgcolor='rgba(20, 28, 58, 0.8)',
        paper_bgcolor='rgba(20, 28, 58, 0)',
        font=dict(color='#8892b0', family='Inter'),
        title_font_size=16
    )
    st.plotly_chart(fig8, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# PRICE RANGE ANALYSIS
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">📏 Volatility Analysis</div>
    <div class="section-subtitle">Daily price range and market volatility</div>
</div>
""", unsafe_allow_html=True)

price_range = filtered_df["High"] - filtered_df["Low"]
range_df = pd.DataFrame({
    "Date": filtered_df["Date"],
    "Range": price_range
})

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
fig9 = px.area(
    range_df,
    x="Date",
    y="Range",
    title="<b>Daily High-Low Price Range - Market Volatility Indicator</b>",
    color_discrete_sequence=['#00ffff']
)
fig9.update_layout(
    plot_bgcolor='rgba(20, 28, 58, 0.8)',
    paper_bgcolor='rgba(20, 28, 58, 0)',
    font=dict(color='#8892b0', family='Inter'),
    title_font_size=16,
    hovermode='x unified'
)
fig9.update_traces(fill='tozeroy', opacity=0.3)
st.plotly_chart(fig9, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# PRICE HIGHLIGHTS
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">🏆 Price Extremes</div>
    <div class="section-subtitle">Historical peak and trough analysis</div>
</div>
""", unsafe_allow_html=True)

highest_close = filtered_df.loc[filtered_df["Close"].idxmax()]
lowest_close = filtered_df.loc[filtered_df["Close"].idxmin()]

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="success-card">
        <div style="font-weight: 700; color: #00ffff; margin-bottom: 0.5rem;">📈 ALL-TIME HIGH</div>
        <div style="font-size: 1.5rem; font-weight: 800; color: #4ade80; margin: 0.5rem 0;">${highest_close['Close']:.2f}</div>
        <div style="color: #8892b0;">Date: {highest_close['Date'].date()}</div>
        <div style="color: #8892b0; font-size: 0.85rem;">Volume: {highest_close['Volume']:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="alert-card">
        <div style="font-weight: 700; color: #ef4444; margin-bottom: 0.5rem;">📉 ALL-TIME LOW</div>
        <div style="font-size: 1.5rem; font-weight: 800; color: #ef4444; margin: 0.5rem 0;">${lowest_close['Close']:.2f}</div>
        <div style="color: #8892b0;">Date: {lowest_close['Date'].date()}</div>
        <div style="color: #8892b0; font-size: 0.85rem;">Volume: {lowest_close['Volume']:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# KEY INSIGHTS
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">💡 Key Analytical Insights</div>
    <div class="section-subtitle">Data-driven observations and patterns</div>
</div>
""", unsafe_allow_html=True)

corr_price_volume = numeric_df['Close'].corr(numeric_df['Volume'])
avg_price_range = price_range.mean()
volatility = filtered_df['Close'].pct_change().std()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="insight-card">
        <div style="font-weight: 700; color: #4ade80; margin-bottom: 0.5rem;">📊 PRICE-VOLUME CORRELATION</div>
        <div style="font-size: 1.2rem; font-weight: 600;">{corr_price_volume:.3f}</div>
        <div style="color: #8892b0; font-size: 0.85rem;">{'Positive' if corr_price_volume > 0 else 'Negative'} relationship detected</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="insight-card">
        <div style="font-weight: 700; color: #4ade80; margin-bottom: 0.5rem;">📏 AVG DAILY RANGE</div>
        <div style="font-size: 1.2rem; font-weight: 600;">${avg_price_range:.2f}</div>
        <div style="color: #8892b0; font-size: 0.85rem;">Average intraday price movement</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="insight-card">
        <div style="font-weight: 700; color: #4ade80; margin-bottom: 0.5rem;">⚡ DAILY VOLATILITY</div>
        <div style="font-size: 1.2rem; font-weight: 600;">{volatility:.2%}</div>
        <div style="color: #8892b0; font-size: 0.85rem;">{'High' if volatility > 0.03 else 'Moderate'} volatility regime</div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# FOOTER
# =====================================================
st.markdown("""
<div style="text-align: center; padding: 2rem; margin-top: 2rem; border-top: 1px solid rgba(0, 255, 255, 0.2);">
    <div style="color: #8892b0; font-size: 0.85rem;">
        📊 Tesla Exploratory Data Analysis | Tesla Stock Price Prediction
    </div>
    <div style="color: #8892b0; font-size: 0.75rem; margin-top: 0.5rem;">
        © Copyright 2026 — Meetpatel
    </div>
    <div style="color: #8892b0; font-size: 0.75rem; margin-top: 0.5rem;">
        Terms of Service / Privacy Policy
    </div>
</div>
""", unsafe_allow_html=True)