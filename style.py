import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
        /* ========== 全局背景（大地暖色系） ========== */
        body .stApp {
            background: linear-gradient(135deg, #f5efe8 0%, #faf7f2 50%, #f0ebe4 100%) !important;
            background-attachment: fixed !important;
        }
        body, .stMarkdown, p, span, label {
            color: #4a3f38 !important;
        }

        /* ========== 动态星空背景（浅色版，白色星点） ========== */
        body .stApp::after {
            content: "";
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            z-index: -4;
            pointer-events: none;
            background-image: 
                radial-gradient(2px 2px at 5% 10%, #ffffff, rgba(0,0,0,0)),
                radial-gradient(2px 2px at 10% 15%, #ffffff, rgba(0,0,0,0)),
                radial-gradient(2px 2px at 15% 8%, #f0f0f0, rgba(0,0,0,0)),
                radial-gradient(3px 3px at 20% 12%, #ffffff, rgba(0,0,0,0)),
                radial-gradient(2px 2px at 25% 20%, #f0f0f0, rgba(0,0,0,0)),
                radial-gradient(1px 1px at 30% 18%, #ffffff, rgba(0,0,0,0)),
                radial-gradient(2px 2px at 35% 22%, #f0f0f0, rgba(0,0,0,0)),
                radial-gradient(3px 3px at 40% 25%, #ffffff, rgba(0,0,0,0)),
                radial-gradient(2px 2px at 45% 28%, #f0f0f0, rgba(0,0,0,0)),
                radial-gradient(1px 1px at 50% 30%, #ffffff, rgba(0,0,0,0)),
                radial-gradient(2px 2px at 55% 35%, #f0f0f0, rgba(0,0,0,0)),
                radial-gradient(3px 3px at 60% 32%, #ffffff, rgba(0,0,0,0)),
                radial-gradient(2px 2px at 65% 38%, #f0f0f0, rgba(0,0,0,0)),
                radial-gradient(1px 1px at 70% 40%, #ffffff, rgba(0,0,0,0)),
                radial-gradient(2px 2px at 75% 45%, #f0f0f0, rgba(0,0,0,0)),
                radial-gradient(3px 3px at 80% 42%, #ffffff, rgba(0,0,0,0)),
                radial-gradient(2px 2px at 85% 48%, #f0f0f0, rgba(0,0,0,0)),
                radial-gradient(1px 1px at 90% 50%, #ffffff, rgba(0,0,0,0)),
                radial-gradient(2px 2px at 95% 55%, #f0f0f0, rgba(0,0,0,0));
            background-size: 400px 400px;
            animation: twinkle 80s linear infinite;
            opacity: 0.3;
        }

        @keyframes twinkle {
            0% { transform: translateY(0px); }
            50% { opacity: 0.15; }
            100% { transform: translateY(-400px); opacity: 0.3; }
        }

        /* ========== 侧边栏 ========== */
        body section[data-testid="stSidebar"] {
            background-color: rgba(232, 224, 213, 0.85) !important;
            backdrop-filter: blur(8px);
        }

        /* ========== 主内容区透明 ========== */
        .main .block-container {
            background-color: transparent !important;
        }

        /* ========== KPI 卡片：大地色边框 ========== */
        body div[data-testid="metric-container"] {
            background-color: #fdfbf7 !important;
            border-radius: 16px !important;
            padding: 16px 12px !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.04) !important;
        }
        body div[data-testid="metric-container"]:nth-of-type(1) {
            border-left: 6px solid #c27a5e !important;
        }
        body div[data-testid="metric-container"]:nth-of-type(2) {
            border-left: 6px solid #4a7c59 !important;
        }
        body div[data-testid="metric-container"]:nth-of-type(3) {
            border-left: 6px solid #d4a373 !important;
        }

        /* ========== 按钮 ========== */
        body .stButton > button {
            background-color: #6b7b5a !important;
            color: white !important;
            border-radius: 30px !important;
            border: none !important;
        }

        /* ========== 下拉框 ========== */
        body div[data-baseweb="select"] > div {
            border-radius: 12px !important;
            border-color: #c4b8a7 !important;
        }
        body div[data-baseweb="select"] > div:focus-within {
            border-color: #6b7b5a !important;
            box-shadow: 0 0 0 2px rgba(107, 123, 90, 0.2) !important;
        }

        /* ========== 表格表头 ========== */
        body div[data-testid="stDataFrame"] thead tr th {
            background-color: #4a3f38 !important;
            color: #f0ebe4 !important;
            font-weight: 500;
        }

        /* ========== 信息栏卡片 ========== */
        body .info-card {
            background-color: #f6f1ea !important;
            border-radius: 20px !important;
            padding: 20px 18px !important;
            box-shadow: 0 6px 14px rgba(90, 70, 50, 0.05) !important;
            border: 1px solid #d6ccc0 !important;
        }

        /* ========== 故事引导区 ========== */
        body .story-box {
            background-color: #faf7f2 !important;
            border-radius: 20px !important;
            padding: 20px 24px !important;
            box-shadow: 0 6px 14px rgba(60, 50, 40, 0.04) !important;
            border-left: 6px solid #5c6e4e !important;
        }

        /* ========== 分割线 ========== */
        hr {
            border-color: #c9bfb2 !important;
        }

        /* ========== 图表容器 ========== */
        body .stPlotlyChart {
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        }
    </style>
    """, unsafe_allow_html=True)
