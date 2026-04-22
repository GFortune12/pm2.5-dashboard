import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="城市排名与总结", layout="wide")
import sys
sys.path.append('../')  # 确保能找到 styles 模块（因为 pages 在子目录）
from style import apply_custom_styles
apply_custom_styles()
# 获取共享数据
if 'df_main' not in st.session_state:
    st.error("请先返回主页加载数据！")
    st.stop()

df_main = st.session_state['df_main']
selected_year = st.session_state.get('selected_year', 2022)
pollutant = st.session_state.get('pollutant', 'PM2.5')

# 侧边栏
st.sidebar.header("⚙️ 控制面板")
#st.sidebar.write(f"当前年份：{selected_year} | 污染物：{pollutant}")
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
# 更新全局状态
st.session_state['pollutant'] = pollutant

# 筛选年份数据
df_year = df_main[df_main['年份'] == selected_year]
city_avg = df_year.groupby('城市')[pollutant].mean().reset_index().sort_values(pollutant, ascending=False)

st.title(f"📊 主要城市{pollutant}排名与区域总结")

# ---------- 左右布局：排名 + 区域总结 ----------
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

# ---------- 区域总结（动态解读）----------
st.markdown("---")
st.subheader("📝 区域污染总结")

# 定义区域城市列表（可自行扩展）
north_cities = ['北京', '天津', '石家庄', '唐山', '保定', '太原', '呼和浩特', '沈阳', '长春', '哈尔滨']
south_cities = ['广州', '深圳', '珠海', '佛山', '东莞', '南宁', '海口', '福州', '厦门', '南昌']
west_cities = ['拉萨', '西宁', '银川', '乌鲁木齐', '昆明', '贵阳', '成都', '重庆']

# 计算区域均值
north_avg = df_year[df_year['城市'].isin(north_cities)][pollutant].mean()
south_avg = df_year[df_year['城市'].isin(south_cities)][pollutant].mean()
west_avg = df_year[df_year['城市'].isin(west_cities)][pollutant].mean()

# 根据污染物类型生成不同的区域解读
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
