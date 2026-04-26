import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
        /* ========== 全局背景（清爽蓝渐变） ========== */
        body .stApp {
            background: linear-gradient(135deg, #e3f2fd 0%, #e8eaf6 50%, #e0f7fa 100%) !important;
            background-attachment: fixed !important;
        }
        body, .stMarkdown, p, span, label {
            color: #1a237e !important;
        }

        /* ========== 动态星空背景（深灰星点，浅蓝背景可见） ========== */
        body .stApp::after {
            content: "";
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            z-index: -4;
            pointer-events: none;
            background-image: 
                radial-gradient(2px 2px at 5% 10%, #666666, rgba(0,0,0,0)),
                radial-gradient(2px 2px at 10% 15%, #888888, rgba(0,0,0,0)),
                radial-gradient(2px 2px at 15% 8%, #777777, rgba(0,0,0,0)),
                radial-gradient(3px 3px at 20% 12%, #999999, rgba(0,0,0,0)),
                radial-gradient(2px 2px at 25% 20%, #666666, rgba(0,0,0,0)),
                radial-gradient(1px 1px at 30% 18%, #888888, rgba(0,0,0,0)),
                radial-gradient(2px 2px at 35% 22%, #777777, rgba(0,0,0,0)),
                radial-gradient(3px 3px at 40% 25%, #999999, rgba(0,0,0,0)),
                radial-gradient(2px 2px at 45% 28%, #666666, rgba(0,0,0,0)),
                radial-gradient(1px 1px at 50% 30%, #888888, rgba(0,0,0,0)),
                radial-gradient(2px 2px at 55% 35%, #777777, rgba(0,0,0,0)),
                radial-gradient(3px 3px at 60% 32%, #999999, rgba(0,0,0,0)),
                radial-gradient(2px 2px at 65% 38%, #666666, rgba(0,0,0,0)),
                radial-gradient(1px 1px at 70% 40%, #888888, rgba(0,0,0,0)),
                radial-gradient(2px 2px at 75% 45%, #777777, rgba(0,0,0,0)),
                radial-gradient(3px 3px at 80% 42%, #999999, rgba(0,0,0,0)),
                radial-gradient(2px 2px at 85% 48%, #666666, rgba(0,0,0,0)),
                radial-gradient(1px 1px at 90% 50%, #888888, rgba(0,0,0,0)),
                radial-gradient(2px 2px at 95% 55%, #777777, rgba(0,0,0,0));
            background-size: 400px 400px;
            animation: twinkle 80s linear infinite;
            opacity: 0.35;
        }

        @keyframes twinkle {
            0% { transform: translateY(0px); }
            50% { opacity: 0.2; }
            100% { transform: translateY(-400px); opacity: 0.35; }
        }

        /* ========== 侧边栏 ========== */
        body section[data-testid="stSidebar"] {
            background-color: rgba(255, 255, 255, 0.7) !important;
            backdrop-filter: blur(10px);
        }

        /* ========== 主内容区透明 ========== */
        .main .block-container {
            background-color: transparent !important;
        }

        /* ========== KPI 卡片 ========== */
        body div[data-testid="metric-container"] {
            background-color: #ffffff !important;
            border-radius: 16px !important;
            padding: 16px 12px !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.04) !important;
            border: none !important;
        }
        body div[data-testid="metric-container"]:nth-of-type(1) {
            border-left: 6px solid #1e88e5 !important;
        }
        body div[data-testid="metric-container"]:nth-of-type(2) {
            border-left: 6px solid #43a047 !important;
        }
        body div[data-testid="metric-container"]:nth-of-type(3) {
            border-left: 6px solid #ef6c00 !important;
        }

        /* ========== 按钮 ========== */
        body .stButton > button {
            background-color: #1e88e5 !important;
            color: white !important;
            border-radius: 30px !important;
            border: none !important;
        }
        body .stButton > button:hover {
            background-color: #1565c0 !important;
        }

        /* ========== 下拉框 ========== */
        body div[data-baseweb="select"] > div {
            border-radius: 12px !important;
            border-color: #90caf9 !important;
        }
        body div[data-baseweb="select"] > div:focus-within {
            border-color: #1e88e5 !important;
            box-shadow: 0 0 0 2px rgba(30, 136, 229, 0.2) !important;
        }

        /* ========== 表格表头 ========== */
        body div[data-testid="stDataFrame"] thead tr th {
            background-color: #1565c0 !important;
            color: white !important;
            font-weight: 500;
        }

        /* ========== 信息栏卡片 ========== */
        body .info-card {
            background-color: #ffffff !important;
            border-radius: 20px !important;
            padding: 20px 18px !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.04) !important;
            border: 1px solid #bbdefb !important;
        }

        /* ========== 故事引导区 ========== */
        body .story-box {
            background-color: #ffffff !important;
            border-radius: 20px !important;
            padding: 20px 24px !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.04) !important;
            border-left: 6px solid #1e88e5 !important;
        }

        /* ========== 分割线 ========== */
        hr {
            border-color: #bbdefb !important;
        }

        /* ========== 图表容器 ========== */
        body .stPlotlyChart {
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        }
    </style>
    """, unsafe_allow_html=True)
