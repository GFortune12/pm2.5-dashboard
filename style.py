import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
        /* ========== 全局标题 ========== */
        h1 {
            color: #3b4a3f !important;  /* 深橄榄绿 */
            font-weight: 600;
        }

        /* ========== 侧边栏 ========== */
        section[data-testid="stSidebar"] {
            background-color: #e8e0d5;  /* 暖沙灰 */
        }

        /* ========== KPI 卡片：三个不同左边框色 ========== */
        div[data-testid="metric-container"] {
            background-color: #fdfbf7;
            border-radius: 16px;
            padding: 16px 12px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.02);
        }
        div[data-testid="metric-container"]:nth-of-type(1) {
            border-left: 6px solid #c27a5e !important;  /* 陶土红 */
        }
        div[data-testid="metric-container"]:nth-of-type(2) {
            border-left: 6px solid #4a7c59 !important;  /* 森林绿 */
        }
        div[data-testid="metric-container"]:nth-of-type(3) {
            border-left: 6px solid #d4a373 !important;  /* 金盏菊黄 */
        }

        /* ========== 按钮 ========== */
        .stButton > button {
            background-color: #6b7b5a;  /* 橄榄绿 */
            color: white;
            border-radius: 30px;
            border: none;
            padding: 8px 20px;
            font-weight: 500;
        }
        .stButton > button:hover {
            background-color: #4a5a3e;
            box-shadow: 0 4px 8px rgba(107, 123, 90, 0.3);
        }

        /* ========== 下拉框 ========== */
        div[data-baseweb="select"] > div {
            border-radius: 12px;
            border-color: #c4b8a7;
        }
        div[data-baseweb="select"] > div:focus-within {
            border-color: #6b7b5a !important;
            box-shadow: 0 0 0 2px rgba(107, 123, 90, 0.2);
        }

        /* ========== 表格表头 ========== */
        div[data-testid="stDataFrame"] thead tr th {
            background-color: #4a3f38 !important;  /* 深褐灰 */
            color: #f0ebe4 !important;
            font-weight: 500;
        }

        /* ========== 信息栏卡片 ========== */
        .info-card {
            background-color: #f6f1ea;
            border-radius: 20px;
            padding: 20px 18px;
            box-shadow: 0 6px 14px rgba(90, 70, 50, 0.05);
            border: 1px solid #d6ccc0;
        }

        /* ========== 故事引导区 ========== */
        .story-box {
            background-color: #faf7f2;
            border-radius: 20px;
            padding: 20px 24px;
            box-shadow: 0 6px 14px rgba(60, 50, 40, 0.04);
            border-left: 6px solid #5c6e4e;
        }

        /* ========== 分割线 ========== */
        hr {
            border-color: #c9bfb2;
        }
    </style>
    """, unsafe_allow_html=True)