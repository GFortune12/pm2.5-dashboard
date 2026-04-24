import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
        /* ========== 全局星空背景与基础设定 ========== */
        /* 页面基底：深邃夜空 */
        .stApp {
            background: linear-gradient(135deg, #0b1b3d 0%, #1a2f4a 50%, #0d1e33 100%);
            background-attachment: fixed;
        }

        /* 让主内容区透明，为的是能透出基底 */
        .main .block-container {
            background-color: transparent !important;
        }

        /* ========== 动态星空效果 (伪元素) ========== */
        /* 背景容器 */
        .stApp::before {
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -5;
            background: transparent;
            pointer-events: none;
        }

        /* 星星层 - 使用重复的径向渐变和动画模拟星空 */
        .stApp::after {
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
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
            z-index: -4;
            pointer-events: none;
            animation: twinkle 80s linear infinite;
            opacity: 0.7;
        }

        @keyframes twinkle {
            0% { transform: translateY(0px); }
            50% { opacity: 0.5; }
            100% { transform: translateY(-400px); opacity: 0.7; }
        }

        /* ========== 通用卡片与容器美化 ========== */
        /* 沿用大地色系的半透明效果，增加“毛玻璃”质感 */
        .stButton > button, div[data-baseweb="select"] > div, .stTextInput > div > div > input {
            border-radius: 12px !important;
        }

        .stPlotlyChart {
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        /* ========== 侧边栏 ========== */
        section[data-testid="stSidebar"] {
            background-color: rgba(26, 47, 74, 0.85);
            backdrop-filter: blur(10px);
        }

        /* ========== 适配夜空主题的标题与文字 ========== */
        h1, h2, h3, h4 {
            color: #e2e8f0 !important;
            font-weight: 600;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }
        
        label, .stMarkdown, .stCaption {
            color: #e2e8f0 !important;
        }

        /* ========== 分割线 ========== */
        hr {
            border-color: rgba(255,255,255,0.2);
            margin: 2rem 0;
        }

        /* ========== 信息栏与故事框 ========== */
        .info-card, .story-box {
            background-color: rgba(20, 40, 65, 0.8);
            backdrop-filter: blur(8px);
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 6px 14px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.15);
        }
    </style>
    """, unsafe_allow_html=True)
