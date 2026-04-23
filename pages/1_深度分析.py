import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import sys

st.set_page_config(page_title="城市排名与总结", layout="wide")
sys.path.append('../')  # 确保能找到 style 模块（因为 pages 在子目录）
from style import apply_custom_styles
apply_custom_styles()

# 获取共享数据
if 'df_main' not in st.session_state:
    st.error("请先返回主页加载数据！")
    st.stop()

df_main = st.session_state['df_main']
selected_year = st.session_state.get('selected_year', 2022)
pollutant = st.session_state.get('pollutant', 'PM2.5')

# ---------- 侧边栏 ----------
st.sidebar.header("⚙️ 控制面板")
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
st.session_state['pollutant'] = pollutant

# 筛选年份数据
df_year = df_main[df_main['年份'] == selected_year]
city_avg = df_year.groupby('城市')[pollutant].mean().reset_index().sort_values(pollutant, ascending=False)

st.title(f"📊 主要城市{pollutant}排名与区域总结")

# ==================== 1. 排名柱状图 ====================
col1, col2 = st.columns([1, 1])
with col1:
    st.subheader(f"🔴 {selected_year}年{pollutant}浓度最高城市")
    top10 = city_avg.head(10)
    fig1 = px.bar(top10, x=pollutant, y='城市', orientation='h',
                  color=pollutant, color_continuous_scale='Reds')
    fig1.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader(f"🟢 {selected_year}年{pollutant}浓度最低城市")
    bottom10 = city_avg.tail(10).sort_values(pollutant, ascending=True)
    fig2 = px.bar(bottom10, x=pollutant, y='城市', orientation='h',
                  color=pollutant, color_continuous_scale='Greens_r')
    fig2.update_layout(yaxis={'categoryorder': 'total descending'})
    st.plotly_chart(fig2, use_container_width=True)

# ==================== 2. 城市诊断卡片 ====================
st.markdown("---")
st.subheader("🏥 城市综合诊断（选择城市查看）")

all_cities = sorted(df_year['城市'].unique())
diag_city = st.selectbox("选择要诊断的城市", all_cities, index=0, key="diag_city")

if diag_city:
    # 该城市当年各污染物的均值
    avail_pol = ['PM2.5', 'PM10', 'So2', 'No2', 'O3', 'Co']
    avail_pol = [p for p in avail_pol if p in df_year.columns]
    city_pol_values = df_year[df_year['城市'] == diag_city][avail_pol].mean().to_dict()
    national_avg = df_year[avail_pol].mean().to_dict()

    col_diag1, col_diag2 = st.columns([1, 1])

    with col_diag1:
        # 雷达图：城市 vs 全国
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=[city_pol_values[p] for p in avail_pol],
            theta=avail_pol,
            fill='toself',
            name=diag_city,
            line=dict(color='#3498db')
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=[national_avg[p] for p in avail_pol],
            theta=avail_pol,
            fill='toself',
            name='全国均值',
            line=dict(color='#95a5a6', dash='dash')
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True)),
            title=f"{diag_city} vs 全国均值（{selected_year}年）"
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with col_diag2:
        # 该城市近5年排名变化
        city_rank_trend = []
        for y in range(max(2013, selected_year-4), selected_year+1):
            df_y = df_main[df_main['年份'] == y]
            avg_y = df_y.groupby('城市')[pollutant].mean().sort_values()
            if diag_city in avg_y.index:
                rank = list(avg_y.index).index(diag_city) + 1
            else:
                rank = None
            city_rank_trend.append((y, rank))
        rank_df = pd.DataFrame(city_rank_trend, columns=['年份', '全国排名']).dropna()
        fig_rank = px.line(rank_df, x='年份', y='全国排名', markers=True,
                           title=f"{diag_city} {pollutant} 排名变化 (越小越好)")
        fig_rank.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_rank, use_container_width=True)

    # 污染类型判断
    pm25_val = city_pol_values.get('PM2.5', 0)
    o3_val = city_pol_values.get('O3', 0)
    if pm25_val > o3_val * 1.2:
        poll_type = "PM2.5主导型"
    elif o3_val > pm25_val * 1.2:
        poll_type = "O3敏感型"
    else:
        poll_type = "复合型"
    st.caption(f"初步判断：{diag_city} 属于 **{poll_type}** 污染特征。")

# ==================== 3. 区域总结（保留原有解读） ====================
st.markdown("---")
st.subheader("📝 区域污染总结")

north_cities = ['北京', '天津', '石家庄', '唐山', '保定', '太原', '呼和浩特', '沈阳', '长春', '哈尔滨']
south_cities = ['广州', '深圳', '珠海', '佛山', '东莞', '南宁', '海口', '福州', '厦门', '南昌']
west_cities = ['拉萨', '西宁', '银川', '乌鲁木齐', '昆明', '贵阳', '成都', '重庆']

north_avg = df_year[df_year['城市'].isin(north_cities)][pollutant].mean()
south_avg = df_year[df_year['城市'].isin(south_cities)][pollutant].mean()
west_avg = df_year[df_year['城市'].isin(west_cities)][pollutant].mean()

if pollutant == 'PM2.5':
    north_text = "是全国污染最重的区域，主要受工业排放、冬季燃煤取暖及不利地形条件影响"
    south_text = "空气质量普遍较好，得益于湿润气候和较少的重工业"
    west_text = "地广人稀、工业活动少，空气质量最优"
elif pollutant == 'O3':
    north_text = "夏季O₃浓度较高，受前体物排放和高温强辐射影响"
    south_text = "珠三角、长三角O₃污染突出，与VOCs和NOx排放高度相关"
    west_text = "浓度相对较低，但高原边缘受平流层输入影响偶有升高"
elif pollutant in ['PM10', 'So2', 'No2']:
    north_text = "浓度较高，与工业及采暖排放相关"
    south_text = "浓度较低，但部分城市存在机动车尾气污染"
    west_text = "浓度整体较低，受人为活动影响小"
else:
    north_text = "浓度相对较高"
    south_text = "浓度相对较低"
    west_text = "浓度最低"

st.markdown(f"""
<div style="background-color:#f0f2f6; padding:20px; border-radius:10px;">
<h4>🏭 区域差异分析</h4>
<ul>
    <li><b>华北地区</b>：年均{pollutant}约为 <b>{north_avg:.1f} μg/m³</b>。{north_text}。</li>
    <li><b>华南地区</b>：年均{pollutant}约为 <b>{south_avg:.1f} μg/m³</b>。{south_text}。</li>
    <li><b>西部地区</b>：年均{pollutant}约为 <b>{west_avg:.1f} μg/m³</b>。{west_text}。</li>
</ul>
<p><b>💡 结论</b>：{pollutant}浓度呈现明显的区域差异。{selected_year}年，污染最重的城市是<b>{city_avg.iloc[0]['城市']}</b>（{city_avg.iloc[0][pollutant]:.1f} μg/m³），最轻的是<b>{city_avg.iloc[-1]['城市']}</b>（{city_avg.iloc[-1][pollutant]:.1f} μg/m³）。</p>
</div>
""", unsafe_allow_html=True)

# ==================== 4. 排名波动分析 ====================
st.markdown("---")
st.subheader("📈 城市排名波动分析（2013-2022）")

all_years = sorted(df_main['年份'].unique())
city_rank_history = []
for y in all_years:
    df_y = df_main[df_main['年份'] == y]
    avg_y = df_y.groupby('城市')[pollutant].mean().sort_values()
    ranks = {city: i+1 for i, city in enumerate(avg_y.index)}
    for city, rank in ranks.items():
        city_rank_history.append((y, city, rank))

rank_df = pd.DataFrame(city_rank_history, columns=['年份', '城市', '排名'])
rank_std = rank_df.groupby('城市')['排名'].std().reset_index()
rank_std.columns = ['城市', '排名标准差']
mean_rank = rank_df.groupby('城市')['排名'].mean().reset_index()
mean_rank.columns = ['城市', '平均排名']
rank_analysis = pd.merge(mean_rank, rank_std, on='城市')

fig_rank_scatter = px.scatter(rank_analysis, x='平均排名', y='排名标准差',
                             hover_name='城市',
                             title=f"城市{pollutant}排名波动性（点越靠右越污染，越高波动越大）")
# 标注波动最大的三个城市
extreme = rank_analysis.nlargest(3, '排名标准差')
for _, row in extreme.iterrows():
    fig_rank_scatter.add_annotation(x=row['平均排名'], y=row['排名标准差'],
                                    text=row['城市'], showarrow=True)
st.plotly_chart(fig_rank_scatter, use_container_width=True)

# ==================== 5. 污染物相关性热力图 ====================
st.markdown("---")
st.subheader("🔗 污染物相关性分析")

pollutants_list = ['PM2.5', 'PM10', 'So2', 'No2', 'O3', 'Co']
available_pollutants = [p for p in pollutants_list if p in df_main.columns]
if len(available_pollutants) >= 2:
    corr_matrix = df_main[available_pollutants].corr()
    fig_corr = ff.create_annotated_heatmap(
        z=corr_matrix.values,
        x=available_pollutants,
        y=available_pollutants,
        colorscale='RdYlGn', reversescale=True, showscale=True
    )
    fig_corr.update_layout(title="各污染物皮尔逊相关系数矩阵")
    st.plotly_chart(fig_corr, use_container_width=True)

    if 'PM2.5' in available_pollutants:
        pm25_corr = corr_matrix['PM2.5'].drop('PM2.5')
        strongest = pm25_corr.abs().idxmax()
        strongest_val = pm25_corr[strongest]
        st.markdown(f"**📌 解读**：PM2.5 与 **{strongest}** 的正相关性最强（r={strongest_val:.2f}），说明它们同源性高，协同减排效果更佳。")
else:
    st.info("数据中缺少足够的污染物列，无法计算相关性矩阵。")
