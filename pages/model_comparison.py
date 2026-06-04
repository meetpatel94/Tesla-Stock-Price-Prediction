import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Model Comparison Dashboard",
    page_icon="🤖",
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
    
    /* Winner Card */
    .winner-card {
        background: linear-gradient(135deg, rgba(74, 222, 128, 0.15) 0%, rgba(34, 197, 94, 0.05) 100%);
        border-radius: 20px;
        padding: 2rem;
        border: 2px solid #4ade80;
        backdrop-filter: blur(10px);
        animation: glowPulse 2s infinite, fadeInUp 0.6s ease-out;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .winner-badge {
        display: inline-block;
        background: linear-gradient(135deg, #4ade80, #22c55e);
        border-radius: 50px;
        padding: 0.5rem 1.5rem;
        font-size: 0.9rem;
        font-weight: 700;
        color: white;
        margin-bottom: 1rem;
    }
    
    .winner-title {
        font-size: 2rem;
        font-weight: 800;
        color: #4ade80;
        margin: 1rem 0;
    }
    
    .winner-reason {
        color: #8892b0;
        font-size: 1rem;
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
        box-shadow: 0 10px 30px rgba(0, 255, 255, 0.2);
    }
    
    .metric-label {
        color: #8892b0;
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #00ffff;
    }
    
    /* Model Card */
    .model-card {
        background: rgba(20, 28, 58, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(0, 255, 255, 0.2);
        transition: all 0.3s ease;
        animation: fadeIn 0.6s ease-out;
        height: 100%;
    }
    
    .model-card:hover {
        transform: translateY(-5px);
        border-color: rgba(0, 255, 255, 0.4);
        box-shadow: 0 10px 30px rgba(0, 255, 255, 0.15);
    }
    
    .model-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #00ffff;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .model-badge {
        display: inline-block;
        background: rgba(0, 255, 255, 0.2);
        border-radius: 20px;
        padding: 0.2rem 0.8rem;
        font-size: 0.75rem;
        color: #00ffff;
        margin-bottom: 1rem;
    }
    
    /* Performance Indicator */
    .perf-indicator {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .perf-label {
        color: #8892b0;
        font-size: 0.9rem;
    }
    
    .perf-value {
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    .perf-badge {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-left: 0.5rem;
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
    
    /* Insight Card */
    .insight-card {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.1) 0%, rgba(0, 100, 255, 0.05) 100%);
        border-radius: 12px;
        padding: 1rem;
        border-left: 4px solid #00ffff;
        margin: 1rem 0;
        animation: fadeInRight 0.5s ease-out;
    }
    
    /* Info Card */
    .info-card {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(245, 158, 11, 0.05) 100%);
        border-radius: 12px;
        padding: 1rem;
        border-left: 4px solid #f59e0b;
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
    
    /* Loading Animation */
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Dataframe Styling */
    .stDataFrame {
        background: rgba(20, 28, 58, 0.5);
        border-radius: 10px;
        border: 1px solid rgba(0, 255, 255, 0.2);
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
        🤖 Model Comparison Dashboard
    </div>
    <div class="hero-subtitle">
        Deep Learning Performance Analysis | RNN vs LSTM for Stock Price Prediction
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# MODEL RESULTS DATA
# =====================================================
results_df = pd.DataFrame({
    "Model": ["SimpleRNN", "LSTM"],
    "RMSE": [11.69, 14.91],
    "MAE": [7.90, 10.56],
    "R2 Score": [0.9742, 0.9581]
})

# Calculate improvements
rmse_improvement = ((results_df["RMSE"][1] - results_df["RMSE"][0]) / results_df["RMSE"][1]) * 100
mae_improvement = ((results_df["MAE"][1] - results_df["MAE"][0]) / results_df["MAE"][1]) * 100
r2_improvement = ((results_df["R2 Score"][0] - results_df["R2 Score"][1]) / results_df["R2 Score"][1]) * 100

# =====================================================
# WINNER SECTION
# =====================================================
st.markdown("""
<div class="winner-card">
    <div class="winner-badge">
        🏆 BETTER MODEL
    </div>
    <div class="winner-title">
        SimpleRNN
    </div>
    <div class="winner-reason">
        Superior performance across all metrics • Lowest error rates • Highest prediction accuracy
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# MODEL COMPARISON CARDS
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">📊 Model Performance Metrics</div>
    <div class="section-subtitle">Detailed comparison of evaluation metrics</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="model-card">
        <div style="text-align: center;">
            <div class="model-title">🔄 SimpleRNN</div>
            <div class="model-badge">Recommended Model</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="perf-indicator">
            <span class="perf-label">📉 RMSE</span>
            <span class="perf-value" style="color: #4ade80;">{results_df["RMSE"][0]:.2f}</span>
        </div>
        <div class="perf-indicator">
            <span class="perf-label">📊 MAE</span>
            <span class="perf-value" style="color: #4ade80;">{results_df["MAE"][0]:.2f}</span>
        </div>
        <div class="perf-indicator">
            <span class="perf-label">📈 R² Score</span>
            <span class="perf-value" style="color: #4ade80;">{results_df["R2 Score"][0]:.4f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="model-card">
        <div style="text-align: center;">
            <div class="model-title">🧠 LSTM</div>
            <div class="model-badge">Comparison Model</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="perf-indicator">
            <span class="perf-label">📉 RMSE</span>
            <span class="perf-value" style="color: #ef4444;">{results_df["RMSE"][1]:.2f}</span>
        </div>
        <div class="perf-indicator">
            <span class="perf-label">📊 MAE</span>
            <span class="perf-value" style="color: #ef4444;">{results_df["MAE"][1]:.2f}</span>
        </div>
        <div class="perf-indicator">
            <span class="perf-label">📈 R² Score</span>
            <span class="perf-value" style="color: #f59e0b;">{results_df["R2 Score"][1]:.4f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# PERFORMANCE METRICS TABLE
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">📋 Metrics Dashboard</div>
    <div class="section-subtitle">Tabular view of all performance indicators</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.dataframe(results_df, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# RMSE COMPARISON
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">📉 Root Mean Square Error (RMSE)</div>
    <div class="section-subtitle">Lower values indicate better prediction accuracy</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
fig_rmse = px.bar(
    results_df,
    x="Model",
    y="RMSE",
    text="RMSE",
    title="<b>RMSE Comparison - SimpleRNN vs LSTM</b>",
    color="Model",
    color_discrete_map={"SimpleRNN": "#4ade80", "LSTM": "#ef4444"}
)
fig_rmse.update_traces(textposition='outside', texttemplate='%{text:.2f}')
fig_rmse.update_layout(
    plot_bgcolor='rgba(20, 28, 58, 0.8)',
    paper_bgcolor='rgba(20, 28, 58, 0)',
    font=dict(color='#8892b0', family='Inter'),
    title_font_size=16,
    showlegend=False,
    yaxis_title="RMSE Value"
)
st.plotly_chart(fig_rmse, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# MAE COMPARISON
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">📊 Mean Absolute Error (MAE)</div>
    <div class="section-subtitle">Average prediction error magnitude</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
fig_mae = px.bar(
    results_df,
    x="Model",
    y="MAE",
    text="MAE",
    title="<b>MAE Comparison - Error Analysis</b>",
    color="Model",
    color_discrete_map={"SimpleRNN": "#4ade80", "LSTM": "#ef4444"}
)
fig_mae.update_traces(textposition='outside', texttemplate='%{text:.2f}')
fig_mae.update_layout(
    plot_bgcolor='rgba(20, 28, 58, 0.8)',
    paper_bgcolor='rgba(20, 28, 58, 0)',
    font=dict(color='#8892b0', family='Inter'),
    title_font_size=16,
    showlegend=False,
    yaxis_title="MAE Value"
)
st.plotly_chart(fig_mae, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# R² COMPARISON
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">📈 R² Score (Coefficient of Determination)</div>
    <div class="section-subtitle">Higher values indicate better fit</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
fig_r2 = px.bar(
    results_df,
    x="Model",
    y="R2 Score",
    text="R2 Score",
    title="<b>R² Score Comparison - Model Fit Analysis</b>",
    color="Model",
    color_discrete_map={"SimpleRNN": "#4ade80", "LSTM": "#f59e0b"}
)
fig_r2.update_traces(textposition='outside', texttemplate='%{text:.4f}')
fig_r2.update_layout(
    plot_bgcolor='rgba(20, 28, 58, 0.8)',
    paper_bgcolor='rgba(20, 28, 58, 0)',
    font=dict(color='#8892b0', family='Inter'),
    title_font_size=16,
    showlegend=False,
    yaxis_title="R² Score",
    yaxis_range=[0.95, 1.0]
)
st.plotly_chart(fig_r2, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# OVERALL COMPARISON
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">🎯 Comprehensive Model Analysis</div>
    <div class="section-subtitle">Side-by-side comparison of all metrics</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
comparison_long = pd.melt(
    results_df,
    id_vars=["Model"],
    value_vars=["RMSE", "MAE", "R2 Score"],
    var_name="Metric",
    value_name="Value"
)

fig_all = px.bar(
    comparison_long,
    x="Model",
    y="Value",
    color="Metric",
    barmode="group",
    title="<b>Overall Model Performance Comparison</b>",
    color_discrete_map={"RMSE": "#ef4444", "MAE": "#f59e0b", "R2 Score": "#4ade80"}
)
fig_all.update_layout(
    plot_bgcolor='rgba(20, 28, 58, 0.8)',
    paper_bgcolor='rgba(20, 28, 58, 0)',
    font=dict(color='#8892b0', family='Inter'),
    title_font_size=16,
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01,
        bgcolor='rgba(0,0,0,0.5)'
    )
)
st.plotly_chart(fig_all, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# KEY INSIGHTS
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">💡 Analytical Insights</div>
    <div class="section-subtitle">Key observations and performance analysis</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="insight-card">
        <div style="font-weight: 700; color: #00ffff; margin-bottom: 0.5rem;">🎯 RMSE IMPROVEMENT</div>
        <div style="font-size: 1.5rem; font-weight: 800; color: #4ade80;">{rmse_improvement:.1f}%</div>
        <div style="color: #8892b0; font-size: 0.85rem;">Better prediction accuracy</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="insight-card">
        <div style="font-weight: 700; color: #00ffff; margin-bottom: 0.5rem;">📊 MAE IMPROVEMENT</div>
        <div style="font-size: 1.5rem; font-weight: 800; color: #4ade80;">{mae_improvement:.1f}%</div>
        <div style="color: #8892b0; font-size: 0.85rem;">Lower absolute error</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="insight-card">
        <div style="font-weight: 700; color: #00ffff; margin-bottom: 0.5rem;">📈 R² IMPROVEMENT</div>
        <div style="font-size: 1.5rem; font-weight: 800; color: #4ade80;">{r2_improvement:.1f}%</div>
        <div style="color: #8892b0; font-size: 0.85rem;">Better model fit</div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# RECOMMENDATION SECTION
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">📖 Final Recommendation</div>
    <div class="section-subtitle">Model selection rationale and deployment guidance</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="winner-card" style="border: 2px solid #00ffff; background: linear-gradient(135deg, rgba(0, 255, 255, 0.1) 0%, rgba(0, 100, 255, 0.05) 100%);">
        <div style="font-size: 3rem; margin-bottom: 1rem;">✅</div>
        <div style="font-size: 1.5rem; font-weight: 800; color: #00ffff; margin-bottom: 1rem;">Selected Model: SimpleRNN</div>
        <div style="color: #8892b0; text-align: left; margin-top: 1rem;">
            • 27.6% lower RMSE than LSTM<br>
            • 33.7% lower MAE than LSTM<br>
            • 1.7% higher R² score<br>
            • Faster training time<br>
            • More stable predictions
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <div style="font-weight: 700; color: #f59e0b; margin-bottom: 0.5rem;">🎯 DEPLOYMENT INSIGHTS</div>
        <div style="color: #ffffff; margin: 0.5rem 0;">
            SimpleRNN demonstrates superior performance for Tesla stock prediction due to:
        </div>
        <div style="color: #8892b0; font-size: 0.9rem; margin-top: 0.5rem;">
            • Better generalization on time series data<br>
            • Lower risk of overfitting<br>
            • More consistent error distribution<br>
            • Optimal complexity for this dataset
        </div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# MODEL ARCHITECTURE NOTE
# =====================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">⚙️ Model Architecture</div>
    <div class="section-subtitle">Technical specifications and configuration</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1rem 0;">
    <div class="glass-card">
        <div style="font-weight: 700; color: #00ffff; margin-bottom: 1rem;">🔄 SimpleRNN Configuration</div>
        <div style="color: #8892b0;">• Simple recurrent architecture</div>
        <div style="color: #8892b0;">• 50 hidden units</div>
        <div style="color: #8892b0;">• Adam optimizer</div>
        <div style="color: #8892b0;">• Mean squared error loss</div>
        <div style="color: #8892b0;">• 100 training epochs</div>
    </div>
    <div class="glass-card">
        <div style="font-weight: 700; color: #f59e0b; margin-bottom: 1rem;">🧠 LSTM Configuration</div>
        <div style="color: #8892b0;">• Long Short-Term Memory</div>
        <div style="color: #8892b0;">• 50 LSTM units</div>
        <div style="color: #8892b0;">• Adam optimizer</div>
        <div style="color: #8892b0;">• Mean squared error loss</div>
        <div style="color: #8892b0;">• 100 training epochs</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# FOOTER
# =====================================================
st.markdown(f"""
<div style="text-align: center; padding: 2rem; margin-top: 2rem; border-top: 1px solid rgba(0, 255, 255, 0.2);">
    <div style="color: #8892b0; font-size: 0.85rem;">
        🤖 Model Comparison Dashboard | Tesla Stock Price Prediction
    </div>
    <div style="color: #8892b0; font-size: 0.75rem; margin-top: 0.5rem;">
        © Copyright 2026 — Meetpatel
    </div>
    <div style="color: #8892b0; font-size: 0.75rem; margin-top: 0.5rem;">
        Terms of Service / Privacy Policy
    </div>
</div>
""", unsafe_allow_html=True)
