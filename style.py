import streamlit as st

# 空气质量行业标准色
COLORS = {
    '优': '#00e400',
    '良': '#ffff00',
    '轻度污染': '#ff7e00',
    '中度污染': '#ff0000',
    '重度污染': '#99004c',
    '严重污染': '#7e0023',
    'primary': '#0f172a',      # 深色背景
    'secondary': '#1e293b',    # 卡片/侧边栏背景
    'accent': '#38bdf8',       # 天蓝霓虹
    'background': '#0f172a',   # 整体背景
    'card_bg': '#1e293b',      # 卡片背景
    'text': '#e2e8f0',         # 浅色文字
    'border': '#334155',
    'warning': '#fbbf24',
    'danger': '#ef4444',
    'success': '#10b981'
}

def apply_custom_styles():
    st.markdown(f"""
    <style>
        /* ========== CSS 变量 ========== */
        :root {{
            --primary: {COLORS['primary']};
            --secondary: {COLORS['secondary']};
            --accent: {COLORS['accent']};
            --bg: {COLORS['background']};
            --card: {COLORS['card_bg']};
            --text: {COLORS['text']};
            --border: {COLORS['border']};
        }}

        /* ========== 全局背景与文字 ========== */
        body, .main, .stApp {{
            background-color: var(--bg);
            color: var(--text);
        }}

        /* ========== 侧边栏 ========== */
        section[data-testid="stSidebar"] {{
            background-color: #1e293b;
            border-right: 1px solid #334155;
        }}

        /* ========== 标题 ========== */
        h1, h2, h3, h4 {{
            color: #f1f5f9 !important;
            font-weight: 600;
        }}

        /* ========== KPI 卡片 ========== */
        div[data-testid="metric-container"] {{
            background: linear-gradient(145deg, #1e293b, #0f172a);
            border: 1px solid #38bdf8;
            border-radius: 20px;
            padding: 20px 16px;
            color: #e2e8f0;
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.15);
            transition: all 0.3s ease;
        }}
        div[data-testid="metric-container"]:hover {{
            box-shadow: 0 0 25px rgba(56, 189, 248, 0.4);
            transform: translateY(-4px);
        }}
        div[data-testid="metric-container"] * {{
            color: #e2e8f0 !important;
        }}

        /* ========== 按钮 ========== */
        .stButton > button {{
            background-color: #38bdf8;
            color: #0f172a;
            border-radius: 30px;
            border: none;
            padding: 8px 20px;
            font-weight: 600;
            transition: all 0.2s ease;
        }}
        .stButton > button:hover {{
            background-color: #7dd3fc;
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.5);
            transform: translateY(-2px);
        }}

        /* ========== 下拉框 ========== */
        div[data-baseweb="select"] > div {{
            border-radius: 12px;
            border-color: #475569;
            background-color: #1e293b;
        }}
        div[data-baseweb="select"] > div:focus-within {{
            border-color: #38bdf8 !important;
            box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.3);
        }}

        /* ========== 表格 ========== */
        div[data-testid="stDataFrame"] thead tr th {{
            background-color: #38bdf8 !important;
            color: #0f172a !important;
            font-weight: 600;
        }}
        div[data-testid="stDataFrame"] tbody tr td {{
            background-color: #1e293b;
            color: #e2e8f0;
        }}

        /* ========== 卡片通用 ========== */
        .info-card, .story-box {{
            background-color: #1e293b;
            border: 1px solid #334155;
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
        }}
        .info-card:hover, .story-box:hover {{
            border-color: #38bdf8;
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.2);
        }}

        /* ========== 分割线 ========== */
        hr {{
            border-color: #334155;
        }}

        /* ========== Plotly 图表容器 ========== */
        .stPlotlyChart {{
            border-radius: 16px;
            background-color: #1e293b;
            padding: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}
    </style>
    """, unsafe_allow_html=True)
