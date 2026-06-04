import streamlit as st
from datetime import datetime

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="About - Tesla AI Stock Predictor",
    page_icon="📘",
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
    
    /* Glass Card */
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
        transform: translateY(-2px);
    }
    
    /* Info Card */
    .info-card {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.08) 0%, rgba(0, 100, 255, 0.04) 100%);
        border-radius: 12px;
        padding: 1rem;
        border-left: 4px solid #00ffff;
        margin: 1rem 0;
        animation: fadeInRight 0.5s ease-out;
    }
    
    /* Success Card */
    .success-card {
        background: linear-gradient(135deg, rgba(74, 222, 128, 0.1) 0%, rgba(34, 197, 94, 0.05) 100%);
        border-radius: 12px;
        padding: 1rem;
        border-left: 4px solid #4ade80;
    }
    
    /* Winner Card */
    .winner-card {
        background: linear-gradient(135deg, rgba(74, 222, 128, 0.15) 0%, rgba(34, 197, 94, 0.08) 100%);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 2px solid #4ade80;
        animation: glowPulse 2s infinite;
    }
    
    /* Feature Grid */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .feature-item {
        background: rgba(20, 28, 58, 0.7);
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .feature-item:hover {
        transform: translateY(-3px);
        background: rgba(0, 255, 255, 0.1);
    }
    
    /* Table Styling */
    .custom-table {
        background: rgba(20, 28, 58, 0.5);
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid rgba(0, 255, 255, 0.2);
    }
    
    /* Workflow Step */
    .workflow-step {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0.5rem;
        margin: 0.5rem 0;
    }
    
    .step-number {
        background: linear-gradient(135deg, #00ffff, #0066ff);
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        color: white;
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
        📘 Tesla AI Stock Predictor
    </div>
    <div class="hero-subtitle">
        Advanced Deep Learning Platform for Financial Market Forecasting
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# PROJECT HIGHLIGHTS
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">🚀 Project Highlights</div>
    <div class="section-subtitle">Key metrics and achievements</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-label">🤖 Deep Learning Models</div>
        <div class="kpi-value">2</div>
        <div class="kpi-trend">SimpleRNN + LSTM</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-label">📅 Forecast Horizon</div>
        <div class="kpi-value">10 Days</div>
        <div class="kpi-trend">Multi-period predictions</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-label">📊 Best R² Score</div>
        <div class="kpi-value">97.42%</div>
        <div class="kpi-trend">SimpleRNN Performance</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-label">🖥 Dashboard Modules</div>
        <div class="kpi-value">6</div>
        <div class="kpi-trend">Complete analytics suite</div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# PROJECT OVERVIEW
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">📖 Project Overview</div>
    <div class="section-subtitle">Understanding the mission and scope</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="glass-card">
        <div style="color: #8892b0; line-height: 1.8;">
            Tesla is one of the most actively traded stocks in the global financial market, 
            making it an ideal candidate for time-series forecasting research.
            <br><br>
            The objective of this project is to analyze historical Tesla stock data and 
            predict future stock prices using advanced Deep Learning techniques including 
            SimpleRNN and LSTM architectures.
            <br><br>
            This application provides an interactive dashboard that supports comprehensive 
            stock analysis, multi-horizon forecasting, model comparison, and decision-support 
            analytics for financial market participants.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <div style="font-weight: 700; color: #00ffff; margin-bottom: 0.5rem;">🎯 Core Mission</div>
        <div style="color: #8892b0; font-size: 0.9rem;">
            Democratize access to AI-powered financial forecasting and provide actionable 
            market intelligence through deep learning technology.
        </div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# OBJECTIVE & PROBLEM STATEMENT
# =====================================================
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="section-header">
        <div class="section-title" style="font-size: 1.3rem;">🎯 Project Objective</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card">
        <div style="color: #8892b0; line-height: 1.8;">
            The primary objective of this project is to predict future Tesla stock prices 
            using Deep Learning models such as SimpleRNN and LSTM.
            <br><br>
            The system analyzes historical stock market data and forecasts future price trends 
            to support financial analysis and investment decision-making processes.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="section-header">
        <div class="section-title" style="font-size: 1.3rem;">❓ Problem Statement</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card">
        <div style="color: #8892b0; line-height: 1.8;">
            Stock prices are highly volatile and influenced by multiple factors including 
            market sentiment, economic indicators, and company performance.
            <br><br>
            Traditional statistical approaches often struggle to capture sequential dependencies 
            present in time-series stock market data. This project uses Deep Learning to 
            learn historical patterns and generate accurate future forecasts.
        </div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# DATASET INFORMATION
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">📊 Dataset Information</div>
    <div class="section-subtitle">Tesla historical stock data (TSLA)</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="glass-card">
        <div style="font-weight: 700; color: #00ffff; margin-bottom: 1rem;">📁 Dataset Overview</div>
        <div style="color: #8892b0;">
            <strong>Dataset:</strong> Tesla Historical Stock Dataset (TSLA)<br>
            <strong>Source:</strong> Historical market data<br>
            <strong>Target Variable:</strong> Close Price<br>
            <strong>Data Points:</strong> Complete trading history
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card">
        <div style="font-weight: 700; color: #00ffff; margin-bottom: 1rem;">📋 Features</div>
        <div style="color: #8892b0;">
            • Date - Trading Date<br>
            • Open - Opening Price<br>
            • High - Highest Price<br>
            • Low - Lowest Price<br>
            • Close - Closing Price<br>
            • Adj Close - Adjusted Close Price<br>
            • Volume - Trading Volume
        </div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# PROJECT WORKFLOW
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">🔄 Project Workflow</div>
    <div class="section-subtitle">End-to-end machine learning pipeline</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="glass-card">
    <div class="workflow-step">
        <div class="step-number">1</div>
        <div style="flex: 1; color: #8892b0;">Data Collection - Historical TSLA stock data acquisition</div>
    </div>
    <div class="workflow-step">
        <div class="step-number">2</div>
        <div style="flex: 1; color: #8892b0;">Data Cleaning & Preprocessing - Handling missing values and scaling</div>
    </div>
    <div class="workflow-step">
        <div class="step-number">3</div>
        <div style="flex: 1; color: #8892b0;">Exploratory Data Analysis - Pattern discovery and visualization</div>
    </div>
    <div class="workflow-step">
        <div class="step-number">4</div>
        <div style="flex: 1; color: #8892b0;">Deep Learning Model Training - SimpleRNN & LSTM architectures</div>
    </div>
    <div class="workflow-step">
        <div class="step-number">5</div>
        <div style="flex: 1; color: #8892b0;">Model Evaluation - Performance metrics comparison</div>
    </div>
    <div class="workflow-step">
        <div class="step-number">6</div>
        <div style="flex: 1; color: #8892b0;">Future Forecasting - Multi-horizon price predictions</div>
    </div>
    <div class="workflow-step">
        <div class="step-number">7</div>
        <div style="flex: 1; color: #8892b0;">Decision Support - Trading signals and risk analysis</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# TECHNOLOGIES USED
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">🛠 Technologies Used</div>
    <div class="section-subtitle">Modern tech stack for AI-driven analytics</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="glass-card">
        <div style="font-weight: 700; color: #00ffff; margin-bottom: 0.5rem;">🐍 Core Languages</div>
        <div style="color: #8892b0;">
            • Python 3.8+<br>
            • SQL (data handling)
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card">
        <div style="font-weight: 700; color: #00ffff; margin-bottom: 0.5rem;">🧠 Deep Learning</div>
        <div style="color: #8892b0;">
            • TensorFlow<br>
            • Keras<br>
            • Scikit-Learn
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="glass-card">
        <div style="font-weight: 700; color: #00ffff; margin-bottom: 0.5rem;">📊 Data Processing</div>
        <div style="color: #8892b0;">
            • Pandas<br>
            • NumPy<br>
            • MinMaxScaler
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="glass-card">
        <div style="font-weight: 700; color: #00ffff; margin-bottom: 0.5rem;">🎨 Visualization</div>
        <div style="color: #8892b0;">
            • Streamlit<br>
            • Plotly<br>
            • Matplotlib<br>
            • Seaborn
        </div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# DASHBOARD MODULES
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">🖥 Dashboard Modules</div>
    <div class="section-subtitle">Comprehensive analytics platform</div>
</div>
""", unsafe_allow_html=True)

modules = [
    ("📊 Dashboard", "Real-time stock metrics and KPI monitoring"),
    ("📈 EDA", "Exploratory data analysis and visualization"),
    ("🤖 Model Comparison", "RNN vs LSTM performance evaluation"),
    ("🔮 Prediction", "Interactive stock price forecasting"),
    ("📉 Forecasting", "Multi-horizon future predictions"),
    ("📘 About", "Project documentation and information")
]

cols = st.columns(3)
for idx, (module, desc) in enumerate(modules):
    with cols[idx % 3]:
        st.markdown(f"""
        <div class="feature-item">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{module}</div>
            <div style="color: #8892b0; font-size: 0.85rem;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# =====================================================
# MODEL PERFORMANCE
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">📈 Model Performance</div>
    <div class="section-subtitle">SimpleRNN vs LSTM comparative analysis</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])

with col1:
    performance_data = {
        "Model": ["SimpleRNN", "LSTM"],
        "RMSE": [11.69, 14.91],
        "MAE": [7.90, 10.56],
        "R² Score": [0.9742, 0.9581]
    }
    
    st.markdown('<div class="custom-table">', unsafe_allow_html=True)
    st.table(performance_data)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="winner-card">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🏆</div>
        <div style="font-size: 1.2rem; font-weight: 700; color: #4ade80;">Best Model</div>
        <div style="font-size: 1.5rem; font-weight: 800; color: #00ffff; margin: 0.5rem 0;">SimpleRNN</div>
        <div style="color: #8892b0; font-size: 0.85rem;">
            ✓ Lowest RMSE (11.69)<br>
            ✓ Lowest MAE (7.90)<br>
            ✓ Highest R² (97.42%)
        </div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# PERFORMANCE SUMMARY
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">📊 Performance Summary</div>
    <div class="section-subtitle">Key evaluation metrics</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-label">Root Mean Square Error</div>
        <div class="kpi-value">11.69</div>
        <div class="kpi-trend">SimpleRNN Performance</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-label">Mean Absolute Error</div>
        <div class="kpi-value">7.90</div>
        <div class="kpi-trend">Prediction accuracy</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-label">R² Score</div>
        <div class="kpi-value">97.42%</div>
        <div class="kpi-trend">Model fit quality</div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# BUSINESS APPLICATIONS
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">💼 Business Applications</div>
    <div class="section-subtitle">Real-world use cases and value propositions</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="glass-card">
        <div style="font-weight: 700; color: #00ffff; margin-bottom: 1rem;">📈 Financial Forecasting</div>
        <div style="color: #8892b0;">
            • Future stock trend estimation<br>
            • Investment planning support<br>
            • Market movement prediction
        </div>
    </div>
    <br>
    <div class="glass-card">
        <div style="font-weight: 700; color: #00ffff; margin-bottom: 1rem;">⚠️ Risk Management</div>
        <div style="color: #8892b0;">
            • Portfolio monitoring<br>
            • Volatility assessment<br>
            • Risk evaluation support
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card">
        <div style="font-weight: 700; color: #00ffff; margin-bottom: 1rem;">🎯 Trading Strategy</div>
        <div style="color: #8892b0;">
            • Buy/Sell decision support<br>
            • Forecast-based analysis<br>
            • Trend identification
        </div>
    </div>
    <br>
    <div class="glass-card">
        <div style="font-weight: 700; color: #00ffff; margin-bottom: 1rem;">🔬 Research & Analytics</div>
        <div style="color: #8892b0;">
            • Deep Learning experimentation<br>
            • Time-series forecasting<br>
            • Financial data analysis
        </div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# KEY FEATURES
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">⭐ Key Features</div>
    <div class="section-subtitle">Comprehensive analytics capabilities</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="glass-card">
        <div style="font-weight: 700; color: #4ade80; margin-bottom: 0.5rem;">📊 Data Analysis</div>
        <div style="color: #8892b0; font-size: 0.85rem;">
            • Dataset Exploration<br>
            • Statistical Analysis<br>
            • Correlation Analysis<br>
            • Price Trend Analysis
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card">
        <div style="font-weight: 700; color: #4ade80; margin-bottom: 0.5rem;">🧠 Deep Learning</div>
        <div style="color: #8892b0; font-size: 0.85rem;">
            • SimpleRNN Model<br>
            • LSTM Model<br>
            • Model Evaluation<br>
            • Model Comparison
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="glass-card">
        <div style="font-weight: 700; color: #4ade80; margin-bottom: 0.5rem;">🔮 Forecasting</div>
        <div style="color: #8892b0; font-size: 0.85rem;">
            • 1, 5, 10-Day Forecasts<br>
            • Trend Analysis<br>
            • Risk Assessment<br>
            • Trading Recommendations
        </div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 1rem;">
    <div style="color: #8892b0; font-size: 0.85rem;">
        📘 Tesla AI Stock Predictor | Tesla Stock Price Prediction
    </div>
   <div style="color: #8892b0; font-size: 0.75rem; margin-top: 0.5rem;">
        © Copyright 2026 — Meetpatel
    </div>
    <div style="color: #8892b0; font-size: 0.75rem; margin-top: 0.5rem;">
        Terms of Service / Privacy Policy
    </div>
</div>
""", unsafe_allow_html=True)
