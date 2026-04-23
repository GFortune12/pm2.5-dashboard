import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(page_title="趋势分析", layout="wide")
import sys
sys.path.append('../')  # 确保能找到 style 模块（因为 pages 在子目录）
from style import apply_custom_styles
apply_custom_styles()

if 'df_main' not in st.session_state:
    st.error("请先返回主页加载数据！")
    st.stop()

df_main = st.session_state['df_main']

# 侧边栏
st.sidebar.header("分析选项")
analysis_type = st.sidebar.radio(
    "选择分析维度",
    ["年度趋势与预测", "季节性规律", "城市对比"]
)
# 污染物切换（与主页同步）
pollutant_options = ['PM2.5', 'PM10', 'So2', 'No2', 'O3']
current_pollutant = st.session_state.get('pollutant', 'PM2.5')
default_index = pollutant_options.index(current_pollutant) if current_pollutant in pollutant_options else 0
pollutant = st.sidebar.selectbox(
    "选择污染物",
    pollutant_options,
    index=default_index,
    key="pollutant_selector_deep"
)
st.title(f"📈 {pollutant}趋势分析与预测")
# 更新全局状态
st.session_state['pollutant'] = pollutant

# ---------- 1. 年度趋势与预测 ----------
if analysis_type == "年度趋势与预测":
    st.header(f"{pollutant}年度趋势与预测（2013-2026）")

    national = df_main.groupby('年份')[pollutant].mean().reset_index()

    X = national['年份'].values.reshape(-1, 1)
    y = national[pollutant].values
    model = LinearRegression()
    model.fit(X, y)

    future_years = np.array([2023, 2024, 2025, 2026]).reshape(-1, 1)
    future_pred = model.predict(future_years)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=national['年份'], y=national[pollutant],
                             mode='lines+markers', name='历史数据',
                             line=dict(color='#2e7d32', width=3)))
    fig.add_trace(go.Scatter(x=future_years.flatten(), y=future_pred,
                             mode='lines+markers', name='预测趋势',
                             line=dict(color='#ff8c00', width=3, dash='dash')))
    fig.update_layout(yaxis_title=f"{pollutant} (μg/m³)", xaxis_title="年份",
                      title=f"全国{pollutant}年度趋势及线性预测")
    st.plotly_chart(fig, use_container_width=True)

    val_2013 = national[national['年份'] == 2013][pollutant].values[0]
    val_2022 = national[national['年份'] == 2022][pollutant].values[0]
    decline = (val_2013 - val_2022) / val_2013 * 100

    # ========== 预测依据展示（优化版） ==========
    with st.expander("📐 点击查看预测模型依据"):
        if pollutant == 'O3':
            trend_desc = "O₃近年呈波动上升态势，线性模型仅作示意，实际趋势需谨慎解读"
        elif pollutant in ['PM2.5', 'PM10', 'So2', 'No2']:
            trend_desc = f"{pollutant}整体呈下降趋势，但2022年出现反弹"
        else:
            trend_desc = f"{pollutant}变化趋势"

        slope = model.coef_[0]
        if slope < 0:
            direction = "下降"
        else:
            direction = "上升"

        st.markdown(f"""
        **模型说明**：基于2013-2022年全国年均 **{pollutant}** 浓度，采用线性回归拟合趋势并外推至2026年。

        **数据趋势**：{trend_desc}。  
        **拟合优度 (R²)**：{model.score(X, y):.3f}  
        **速率**：每年 **{direction}** 约 **{abs(slope):.2f}** μg/m³  
        **预测值（2026年）**：约 **{future_pred[-1]:.1f}** μg/m³

        **⚠️ 局限说明**：
        - 线性模型假设变化速率恒定，无法捕捉政策突变或非线性转折。
        - 未纳入未来能源结构、经济形势、气候异常等外部变量。
        - 长期预测存在较大不确定性，仅供趋势参考。

        **数据来源**：全国城市空气质量历史数据集（2013‑2022）。
        """)

    # ==================== 政策与事件卡片 ====================
    st.markdown("---")
    st.subheader("📜 治理历程与关键事件")

    events = [
        {"year": "2013年", "icon": "🟢", "title": "大气十条出台",
         "desc": "国务院发布《大气污染防治行动计划》，开启全面治霾。"},
        {"year": "2018年", "icon": "🟠", "title": "蓝天保卫战三年行动",
         "desc": "划定“2+26”重点区域，强化联防联控。"},
        {"year": "2020年", "icon": "🔵", "title": "疫情临时性改善",
         "desc": "封控导致交通和工业骤减，PM2.5短暂大幅下降。"},
        {"year": "2022年", "icon": "🔴", "title": "后疫情反弹",
         "desc": "经济恢复叠加沙尘天气，华北PM2.5回升明显。"}
    ]

    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)

    with row1_col1:
        ev = events[0]
        st.markdown(f"""
        <div style="background:#ffffff; border-radius:16px; padding:18px; box-shadow:0 4px 12px rgba(0,0,0,0.04); border-left:6px solid #2e7d32; margin-bottom:20px;">
            <h4 style="margin-top:0; color:#1b5e20;">{ev['icon']} {ev['year']}  {ev['title']}</h4>
            <p style="margin-bottom:0;">{ev['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
    with row1_col2:
        ev = events[1]
        st.markdown(f"""
        <div style="background:#ffffff; border-radius:16px; padding:18px; box-shadow:0 4px 12px rgba(0,0,0,0.04); border-left:6px solid #2e7d32; margin-bottom:20px;">
            <h4 style="margin-top:0; color:#1b5e20;">{ev['icon']} {ev['year']}  {ev['title']}</h4>
            <p style="margin-bottom:0;">{ev['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

    with row2_col1:
        ev = events[2]
        st.markdown(f"""
        <div style="background:#ffffff; border-radius:16px; padding:18px; box-shadow:0 4px 12px rgba(0,0,0,0.04); border-left:6px solid #2e7d32; margin-bottom:20px;">
            <h4 style="margin-top:0; color:#1b5e20;">{ev['icon']} {ev['year']}  {ev['title']}</h4>
            <p style="margin-bottom:0;">{ev['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
    with row2_col2:
        ev = events[3]
        st.markdown(f"""
        <div style="background:#ffffff; border-radius:16px; padding:18px; box-shadow:0 4px 12px rgba(0,0,0,0.04); border-left:6px solid #2e7d32; margin-bottom:20px;">
            <h4 style="margin-top:0; color:#1b5e20;">{ev['icon']} {ev['year']}  {ev['title']}</h4>
            <p style="margin-bottom:0;">{ev['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

    # ==================== 趋势解读 ====================
    st.markdown("---")
    st.subheader("📊 趋势解读")

    if pollutant == 'PM2.5':
        reason_2013 = "《大气污染防治行动计划》实施，大规模推进燃煤锅炉淘汰和工业提标改造"
        reason_2018 = "《打赢蓝天保卫战三年行动计划》接续发力，清洁取暖成效显著"
        reason_2022 = "疫情后工业恢复、沙尘天气增多、部分区域管控力度有所松懈"
    elif pollutant == 'O3':
        reason_2013 = "前体物（NOx和VOCs）排放仍处于高位，O₃生成潜势大"
        reason_2018 = "部分区域推行VOCs与NOx协同减排，但O₃浓度仍呈波动上升态势"
        reason_2022 = "高温强辐射天气频发，光化学反应加剧，叠加前体物排放未根本削减"
    elif pollutant in ['PM10', 'So2', 'No2']:
        reason_2013 = "工业排放和燃煤是主要来源，《大气十条》实施后排放量大幅削减"
        reason_2018 = "超低排放改造和散煤治理持续推进，浓度持续下降"
        reason_2022 = "部分重工业城市出现反弹，与生产活动恢复有关"
    else:
        reason_2013 = "排放控制措施逐步落实"
        reason_2018 = "污染防治攻坚战深入"
        reason_2022 = "经济活动回升带来短期波动"

    st.markdown(f"""
    <div style="background-color:#f0f2f6; padding:20px; border-radius:10px;">
    <h4>十年变化，2022年出现波动</h4>
    <ul>
        <li><b>2013-2017年（快速下降期）</b>：{pollutant}从{val_2013:.1f} μg/m³显著下降。主要得益于{reason_2013}。</li>
        <li><b>2018-2021年（持续改善期）</b>：浓度继续走低。{reason_2018}。</li>
        <li><b>2022年（反弹期）</b>：浓度回升至{val_2022:.1f} μg/m³。可能原因：{reason_2022}。</li>
    </ul>
    <p><b>预测显示</b>：若当前下降趋势延续，2026年全国{pollutant}年均浓度有望降至 <b>{future_pred[-1]:.1f} μg/m³</b>，但需警惕反弹风险。</p>
    </div>
    """, unsafe_allow_html=True)

# ---------- 2. 季节性规律 ----------
elif analysis_type == "季节性规律":
    st.header(f"{pollutant} 月度变化与四季解读")

    # 月度平均折线图
    month_avg = df_main.groupby('月份')[pollutant].mean().reset_index()
    fig = px.line(month_avg, x='月份', y=pollutant, markers=True,
                  title=f"全国{pollutant}月度平均浓度")
    fig.update_xaxes(tickvals=list(range(1, 13)))
    fig.update_traces(line=dict(color='#1565c0', width=3))
    st.plotly_chart(fig, use_container_width=True)

    # 季节划分
    df_season = df_main.copy()
    def get_season(month):
        if month in [3, 4, 5]:
            return '春'
        elif month in [6, 7, 8]:
            return '夏'
        elif month in [9, 10, 11]:
            return '秋'
        else:
            return '冬'
    df_season['季节'] = df_season['月份'].apply(get_season)
    season_avg = df_season.groupby('季节')[pollutant].mean().reindex(['春', '夏', '秋', '冬'])

    seasons = [
        {"name": "春", "icon": "🌸", "avg": season_avg.get('春', 0)},
        {"name": "夏", "icon": "☀️", "avg": season_avg.get('夏', 0)},
        {"name": "秋", "icon": "🍂", "avg": season_avg.get('秋', 0)},
        {"name": "冬", "icon": "❄️", "avg": season_avg.get('冬', 0)}
    ]

    # 卡片悬浮样式
    st.markdown("""
    <style>
    .season-card {
        display: inline-block;
        width: 100%;
        border-radius: 20px;
        padding: 20px 10px;
        text-align: center;
        background: #f9f9f9;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: all 0.2s ease;
        cursor: pointer;
        margin-bottom: 12px;
    }
    .season-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        background: #ffffff;
    }
    .season-icon {
        font-size: 36px;
    }
    .season-name {
        font-weight: 600;
        color: #1b5e20;
        margin: 8px 0 4px 0;
    }
    .season-avg {
        font-size: 24px;
        font-weight: bold;
        color: #2e7d32;
    }
    </style>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    selected_season = None
    for i, (col, s) in enumerate(zip(cols, seasons)):
        with col:
            card_html = f"""
            <div class="season-card" id="season{i}">
                <div class="season-icon">{s['icon']}</div>
                <div class="season-name">{s['name']}季</div>
                <div class="season-avg">{s['avg']:.1f} <small>μg/m³</small></div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            if st.button(f"查看{s['name']}季详情", key=f"season_btn_{i}"):
                selected_season = s['name']

    # 点击后详情
    if selected_season:
        st.markdown("---")
        st.subheader(f"{selected_season}季 {pollutant} 深度解读")

        north_cities = ['北京', '天津', '石家庄', '太原', '沈阳']
        south_cities = ['广州', '深圳', '福州', '南宁', '海口']
        west_cities = ['拉萨', '西宁', '银川', '乌鲁木齐', '昆明']
        def season_city_avg(cities, season):
            return df_season[(df_season['季节'] == season) & (df_season['城市'].isin(cities))][pollutant].mean()
        north_val = season_city_avg(north_cities, selected_season)
        south_val = season_city_avg(south_cities, selected_season)
        west_val = season_city_avg(west_cities, selected_season)

        reasons = {
            'PM2.5': {
                '春': "北方沙尘增多，取暖期刚过，扬尘和残留污染物导致浓度仍较高。",
                '夏': "降水增多，湿沉降作用显著，空气质量全年最好。",
                '秋': "秸秆焚烧和静稳天气增加，污染物开始累积。",
                '冬': "燃煤取暖高峰，逆温层导致污染物不易扩散，浓度达全年最高。"
            },
            'O3': {
                '春': "太阳辐射增强，前体物累积，O₃浓度开始上升。",
                '夏': "高温强辐射，光化学反应最活跃，O₃浓度全年峰值。",
                '秋': "辐射减弱，浓度逐步回落。",
                '冬': "辐射弱，光化学反应减弱，浓度最低。"
            }
        }
        default_reasons = {
            '春': "排放稳定，气象条件开始转好。",
            '夏': "扩散条件好，浓度较低。",
            '秋': "扩散条件转差，浓度有所回升。",
            '冬': "采暖导致排放增加，浓度最高。"
        }
        health_tips = {
            'PM2.5': {
                '冬': "减少户外活动，佩戴N95口罩。",
                '春': "沙尘天注意防护。",
                '夏': "空气质量好，适宜开窗通风。",
                '秋': "关注秸秆焚烧，敏感人群减少外出。"
            }
        }

        reason = reasons.get(pollutant, default_reasons).get(selected_season, "浓度变化与排放和气象有关。")
        tip = health_tips.get(pollutant, {}).get(selected_season, "注意防护，关注空气质量预报。")

        col1, col2 = st.columns(2)
        with col1:
            st.metric(f"{selected_season}季全国均值", f"{season_avg[selected_season]:.1f} μg/m³")
            st.markdown(f"**成因分析**：{reason}")
            st.markdown(f"**健康提示**：{tip}")
        with col2:
            region_df = pd.DataFrame({
                '区域': ['华北', '华南', '西部'],
                '均值': [north_val, south_val, west_val]
            })
            fig_region = px.bar(region_df, x='区域', y='均值', color='区域',
                                title=f"{selected_season}季 {pollutant} 区域对比",
                                color_discrete_map={'华北': '#d32f2f', '华南': '#388e3c', '西部': '#1976d2'})
            fig_region.update_layout(showlegend=False)
            st.plotly_chart(fig_region, use_container_width=True)
    else:
        st.info("👆 点击上方任意季节卡片，查看该季节的详细解读和区域对比。")

# ---------- 3. 城市对比 ----------
else:
    st.header(f"主要城市{pollutant}历史趋势对比")

    all_cities = sorted(df_main['城市'].unique().tolist())
    default_cities = ['北京', '上海', '广州', '成都', '石家庄']
    default_cities = [c for c in default_cities if c in all_cities][:5]
    cities = st.sidebar.multiselect("选择城市（可多选）", all_cities, default=default_cities)

    if cities:
        city_trend = df_main[df_main['城市'].isin(cities)].groupby(['年份', '城市'])[pollutant].mean().reset_index()
        fig = px.line(city_trend, x='年份', y=pollutant, color='城市', markers=True,
                      title=f"所选城市{pollutant}年度趋势对比")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.subheader("城市差异解读")
        if pollutant == 'PM2.5':
            diff_text = """
            <li><b>改善显著的城市（如北京、上海）</b>：严格执行产业升级、机动车管控和清洁能源替代，治理投入大。</li>
            <li><b>改善较慢的城市（如石家庄、保定）</b>：地处华北平原，污染物易聚不易散；产业结构偏重。</li>
            <li><b>西部城市（如拉萨、昆明）</b>：本底值低，无重工业污染，空气质量持续优良。</li>
            """
        elif pollutant == 'O3':
            diff_text = """
            <li><b>沿海城市（如上海、广州）</b>：受海陆风和区域传输影响，O₃浓度易超标。</li>
            <li><b>北方城市（如北京、石家庄）</b>：夏季高温强辐射，O₃生成潜势大。</li>
            <li><b>西部高海拔城市（如拉萨、西宁）</b>：紫外线强，但前体物排放少，O₃浓度相对可控。</li>
            """
        else:
            diff_text = """
            <li><b>北方工业城市</b>：排放量大，浓度较高。</li>
            <li><b>南方城市</b>：扩散条件好，浓度较低。</li>
            <li><b>西部城市</b>：人为活动少，浓度最低。</li>
            """
        st.markdown(f"""
        <div style="background-color:#f0f2f6; padding:20px; border-radius:10px;">
        <h4>为什么不同城市{pollutant}趋势不同？</h4>
        <ul>
            {diff_text}
        </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("请在侧边栏至少选择一个城市。")

# ========== 页面末尾知识小贴士 ==========
st.markdown("---")
tips = {
    'PM2.5': "💡 **你知道吗？** PM2.5 直径不到头发丝的 1/20，可进入肺泡甚至血液循环。减少燃煤和机动车尾气是治理关键。",
    'PM10': "💡 **你知道吗？** PM10 主要来自道路扬尘和沙尘暴，戴口罩可有效阻挡大部分 PM10。",
    'So2': "💡 **你知道吗？** SO₂ 是酸雨的主要元凶，我国近十年 SO₂ 降幅是所有污染物中最大的。",
    'No2': "💡 **你知道吗？** NO₂ 主要来自机动车尾气，早晚高峰浓度明显升高，是城市交通污染的指示灯。",
    'O3': "💡 **你知道吗？** 地面 O₃ 是“隐形杀手”，夏季午后浓度最高，对儿童和哮喘患者威胁大。"
}
tip_text = tips.get(pollutant, f"💡 **你知道吗？** {pollutant} 是评价空气质量的重要指标，长期监测有助于保护公众健康。")
st.info(tip_text)
