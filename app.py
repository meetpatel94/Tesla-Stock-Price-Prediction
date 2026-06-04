import streamlit as st

# =====================================================
# CUSTOM CSS FOR APP NAVIGATION
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
    
    /* Sidebar Navigation Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15, 21, 53, 0.98) 0%, rgba(10, 14, 39, 0.98) 100%);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(0, 255, 255, 0.2);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #8892b0;
    }
    
    /* Navigation Menu Items */
    .st-emotion-cache-1v0mbdj {
        background: transparent;
    }
    
    /* Custom Sidebar Header */
    .sidebar-header {
        text-align: center;
        padding: 1.5rem 1rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid rgba(0, 255, 255, 0.2);
    }
    
    .sidebar-logo {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    .sidebar-title {
        font-size: 1.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00ffff, #0066ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.25rem;
    }
    
    .sidebar-subtitle {
        font-size: 0.7rem;
        color: #8892b0;
    }
    
    /* Navigation Item Hover Effect */
    .st-emotion-cache-1v0mbdj:hover {
        background: rgba(0, 255, 255, 0.1);
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    /* Active Navigation Item */
    .st-emotion-cache-1v0mbdj:active {
        background: rgba(0, 255, 255, 0.2);
    }
    
    /* Footer in Sidebar */
    .sidebar-footer {
        position: fixed;
        bottom: 1rem;
        left: 1rem;
        right: 1rem;
        text-align: center;
        padding: 1rem;
        border-top: 1px solid rgba(0, 255, 255, 0.1);
        font-size: 0.7rem;
        color: #6b7280;
    }
    
    /* Main Content Area */
    .main-header {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Welcome Card */
    .welcome-card {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.1) 0%, rgba(0, 100, 255, 0.05) 100%);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(0, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        text-align: center;
        animation: slideUp 0.6s ease-out;
    }
    
    .welcome-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00ffff, #0066ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .welcome-subtitle {
        color: #8892b0;
        font-size: 1.1rem;
    }
    
    /* Feature Cards */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: rgba(20, 28, 58, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(0, 255, 255, 0.2);
        transition: all 0.3s ease;
        animation: fadeInUp 0.5s ease-out;
        text-align: center;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        border-color: rgba(0, 255, 255, 0.4);
        box-shadow: 0 10px 30px rgba(0, 255, 255, 0.2);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #00ffff;
        margin-bottom: 0.5rem;
    }
    
    .feature-description {
        color: #8892b0;
        font-size: 0.85rem;
        line-height: 1.5;
    }
    
    /* Stats Container */
    .stats-container {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.05) 0%, rgba(0, 100, 255, 0.02) 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(0, 255, 255, 0.1);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 800;
        color: #00ffff;
    }
    
    .stat-label {
        color: #8892b0;
        font-size: 0.85rem;
    }
    
    /* Quick Links */
    .quick-links {
        display: flex;
        gap: 1rem;
        justify-content: center;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    
    .quick-link {
        background: rgba(0, 255, 255, 0.1);
        border-radius: 10px;
        padding: 0.5rem 1rem;
        color: #00ffff;
        text-decoration: none;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .quick-link:hover {
        background: rgba(0, 255, 255, 0.2);
        transform: translateY(-2px);
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
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.7;
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
# PAGE DEFINITIONS
# =====================================================

dashboard = st.Page(
    "pages/dashboard.py",
    title="Market Dashboard",
    icon="📊",
    default=True
)

eda = st.Page(
    "pages/eda.py",
    title="Exploratory Analysis",
    icon="📈"
)

comparison = st.Page(
    "pages/model_comparison.py",
    title="Model Comparison",
    icon="🤖"
)

prediction = st.Page(
    "pages/prediction.py",
    title="AI Prediction",
    icon="🔮"
)

forecasting = st.Page(
    "pages/Forecasting.py",
    title="Future Forecasting",
    icon="📉"
)

about = st.Page(
    "pages/About_Project.py",
    title="Project Info",
    icon="📘"
)

# =====================================================
# SIDEBAR CUSTOM CONTENT
# =====================================================

# Add custom sidebar header

# Navigation
pg = st.navigation([
    dashboard,
    eda,
    comparison,
    prediction,
    forecasting,
    about
])

# Add sidebar footer
st.markdown("""
<div class="sidebar-footer">
    
</div>
""", unsafe_allow_html=True)

# =====================================================
# MAIN CONTENT AREA (for initial load)
# =====================================================

# Run the selected page
pg.run()

# =====================================================
# HIDE STREAMLIT BRANDING
# =====================================================
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
# header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
