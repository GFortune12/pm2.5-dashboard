import streamlit as st

# 空气质量行业标准色
COLORS = {
    '优': '#00e400',
    '良': '#ffff00',
    '轻度污染': '#ff7e00',
    '中度污染': '#ff0000',
    '重度污染': '#99004c',
    '严重污染': '#7e0023',
    'primary': '#2c3e50',
    'secondary': '#34495e',
    'accent': '#1abc9c',
    'background': '#f5f6fa',
    'card_bg': '#ffffff',
    'text': '#2c3e50',
    'border': '#e0e0e0',
    'warning': '#f39c12',
    'danger': '#e74c3c',
    'success': '#27ae60'
}

def apply_custom_styles():
    st.markdown(f"""
    <style>
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

        /* ========== 全局标题 ========== */
        h1 {{
            color: #3b4a3f !important;
            font-weight: 600;
        }}

        /* ========== 侧边栏 ========== */
        section[data-testid="stSidebar"] {{
            background-color: #e8e0d5;
        }}

        /* ========== KPI 卡片：渐变背景 + 悬停动效 ========== */
        div[data-testid="metric-container"] {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            padding: 20px 16px;
            color: white;
            box-shadow: 0 10px 25px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            border: none !important;
        }}
        div[data-testid="metric-container"]:hover {{
            transform: translateY(-6px);
            box-shadow: 0 20px 35px rgba(0,0,0,0.15);
        }}
        div[data-testid="metric-container"] * {{
            color: white !important;
        }}

        /* ========== 按钮 ========== */
        .stButton > button {{
            background-color: #6b7b5a;
            color: white;
            border-radius: 30px;
            border: none;
            padding: 8px 20px;
            font-weight: 500;
            transition: all 0.2s ease;
        }}
        .stButton > button:hover {{
            background-color: #4a5a3e;
            box-shadow: 0 4px 8px rgba(107, 123, 90, 0.3);
            transform: translateY(-2px);
        }}

        /* ========== 下拉框 ========== */
        div[data-baseweb="select"] > div {{
            border-radius: 12px;
            border-color: #c4b8a7;
        }}
        div[data-baseweb="select"] > div:focus-within {{
            border-color: #6b7b5a !important;
            box-shadow: 0 0 0 2px rgba(107, 123, 90, 0.2);
        }}

        /* ========== 表格表头 ========== */
        div[data-testid="stDataFrame"] thead tr th {{
            background-color: #4a3f38 !important;
            color: #f0ebe4 !important;
            font-weight: 500;
        }}

        /* ========== 信息栏卡片 ========== */
        .info-card {{
            background-color: #f6f1ea;
            border-radius: 20px;
            padding: 20px 18px;
            box-shadow: 0 6px 14px rgba(90, 70, 50, 0.05);
            border: 1px solid #d6ccc0;
            transition: all 0.3s ease;
        }}
        .info-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 12px 22px rgba(90, 70, 50, 0.1);
        }}

        /* ========== 故事引导区 ========== */
        .story-box {{
            background-color: #faf7f2;
            border-radius: 20px;
            padding: 20px 24px;
            box-shadow: 0 6px 14px rgba(60, 50, 40, 0.04);
            border-left: 6px solid #5c6e4e;
            transition: all 0.3s ease;
        }}
        .story-box:hover {{
            box-shadow: 0 10px 20px rgba(60, 50, 40, 0.08);
        }}

        /* ========== 分割线 ========== */
        hr {{
            border-color: #c9bfb2;
        }}

        /* ========== Plotly 图表容器美化 ========== */
        .stPlotlyChart {{
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        }}
    </style>
    """, unsafe_allow_html=True)
