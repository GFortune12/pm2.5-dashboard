import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import chardet

# ---------- 页面配置 ----------
st.set_page_config(page_title="现状总览", page_icon="🗺️", layout="wide")
from style import apply_custom_styles
apply_custom_styles()


# ---------- 数据加载 ----------
@st.cache_data
def load_data():
    with open('airdata.csv', 'rb') as f:
        result = chardet.detect(f.read(200000))
        encoding = result['encoding']
    df = pd.read_csv('airdata.csv', encoding=encoding)
    df['日期'] = pd.to_datetime(df['日期'])
    df['年份'] = df['日期'].dt.year
    df['月份'] = df['日期'].dt.month
    return df

@st.cache_data
def load_city_coords():
    return pd.read_csv('city_coords.csv', encoding='utf-8')

df = load_data()
city_coords = load_city_coords()
#st.sidebar.write(df.columns.tolist())  # 查看所有列名
# 筛选主要城市
main_cities = city_coords['城市'].tolist()
df_main = df[df['城市'].isin(main_cities)]

# ---------- 侧边栏 ----------
# ---------- 侧边栏 ----------
st.sidebar.header("⚙️ 控制面板")
available_years = sorted(df_main['年份'].unique())
selected_year = st.sidebar.selectbox("选择年份", available_years, index=len(available_years)-1)

# 污染物选择
pollutant = st.sidebar.selectbox(
    "选择污染物",
    ['PM2.5', 'PM10', 'So2', 'No2', 'O3'],
    index=0,
    key="pollutant_selector"
)

st.sidebar.markdown("---")
st.sidebar.caption("数据范围：2013-2022年，三线及以上主要城市")
st.title(f"🗺️ 全国主要城市{pollutant}污染现状")
st.markdown(f"### 当前各主要城市{pollutant}浓度分布")


# 存储到session_state供其他页面使用
st.session_state['selected_year'] = selected_year
st.session_state['df_main'] = df_main
st.session_state['city_coords'] = city_coords

# ---------- 筛选数据 ----------
df_year = df_main[df_main['年份'] == selected_year]

# ---------- KPI卡片 ----------
city_avg = df_year.groupby('城市')[pollutant].mean()
best_city = city_avg.idxmin()
worst_city = city_avg.idxmax()
avg_val = df_year[pollutant].mean()

col1, col2, col3 = st.columns(3)
col1.metric(f"📊 全国年均{pollutant}", f"{avg_val:.1f} μg/m³")
col2.metric("🍃 空气质量最佳", best_city, f"{city_avg.min():.1f} μg/m³")
col3.metric("🏭 空气质量最差", worst_city, f"{city_avg.max():.1f} μg/m³")

st.markdown("---")

# 计算全国年度趋势（用于引导区）
national_trend = df_main.groupby('年份')[pollutant].mean()
val_2013 = national_trend.iloc[0]
val_2022 = national_trend.iloc[-1]
decline = (val_2013 - val_2022) / val_2013 * 100

# 计算冬夏倍数（可选，如果数据包含月份）
month_avg = df_main.groupby('月份')[pollutant].mean()
winter_avg = month_avg.loc[[12, 1, 2]].mean()
summer_avg = month_avg.loc[[6, 7, 8]].mean()
ratio = winter_avg / summer_avg

# 动态引导区文字
st.markdown(f"""
<div style="background-color:#e8f5e9; padding:18px; border-radius:12px; border-left:6px solid #2e7d32; margin-bottom:20px;">
<h4 style="margin-top:0; color:#1b5e20;">📌 核心洞察</h4>
<p style="font-size:16px; margin-bottom:8px;">
<b>2013-2022年，全国主要城市{pollutant}年均浓度下降{decline:.1f}%，但2022年出现反弹，华北城市群仍是治理难点。</b>
冬季{pollutant}浓度是夏季的<b>{ratio:.1f}倍</b>，季节性防控至关重要。
</p>
<p style="font-size:14px; color:#555; margin-bottom:0;">
👇 下方地图展示各城市{pollutant}浓度分布。点击气泡查看详情，左侧可切换年份。
</p>
</div>
""", unsafe_allow_html=True)

# ---------- 左右布局：地图 + 信息栏 ----------
col_map, col_info = st.columns([3, 2])

with col_map:
    st.subheader(f"📍 {selected_year}年主要城市{pollutant}浓度地图")
    st.caption(f"气泡颜色：🟢 <35 🟠 35-75 🔴 >75 μg/m³（{pollutant}）")

    city_year_avg = df_year.groupby('城市')[pollutant].mean().reset_index(name='avg_val')
    map_data = pd.merge(city_coords, city_year_avg, on='城市', how='inner')

    def get_color(pm):
        if pm < 35:
            return 'green'
        elif pm < 75:
            return 'orange'
        else:
            return 'red'

    m = folium.Map(location=[35, 110], zoom_start=4, tiles='CartoDB positron')
    for _, row in map_data.iterrows():
        folium.CircleMarker(
            location=[row['纬度'], row['经度']],
            radius=8,
            popup=f"{row['城市']}: {row['avg_val']:.1f} μg/m³",
            color=get_color(row['avg_val']),
            fill=True,
            fill_opacity=0.7
        ).add_to(m)

    st_folium(m, width=None, height=550)

    # 引导语放在地图正下方
    st.markdown("---")
    st.info("""
    **👆 操作提示**：在左侧选择年份，地图和右侧信息栏会实时更新。下拉选择城市，查看该城市详细数据和历年趋势。  
    **👉 下一步**：点击左侧导航栏的“深度分析”或“趋势分析”，探索更多数据洞察。
    """)

with col_info:
    st.subheader("📋 城市详情")

    all_cities = sorted(df_year['城市'].unique())
    default_city = '北京' if '北京' in all_cities else all_cities[0]
    default_index = all_cities.index(default_city)
    selected_city = st.selectbox("选择城市", all_cities, index=default_index, key="city_info_selector")

    if selected_city:
        city_data = df_year[df_year['城市'] == selected_city]
        city_val = city_data[pollutant].mean()

        def get_pollution_level(val):
            if val < 35:
                return "🟢 优", "green"
            elif val < 75:
                return "🟡 良", "gold"
            elif val < 115:
                return "🟠 轻度污染", "orange"
            elif val < 150:
                return "🟠 中度污染", "darkorange"
            elif val < 250:
                return "🔴 重度污染", "red"
            else:
                return "🟣 严重污染", "purple"

        level_text, level_color = get_pollution_level(city_val)

        city_avg_all = df_year.groupby('城市')[pollutant].mean().sort_values()
        rank = list(city_avg_all.index).index(selected_city) + 1
        total = len(city_avg_all) 

# 历史数据表格
        city_history = df_main[df_main['城市'] == selected_city].groupby('年份')[pollutant].mean().round(1).reset_index()
        city_history.columns = ['年份', f'{pollutant} (μg/m³)']

        st.markdown(f"### {selected_city}")
        st.metric(f"🌫️ {selected_year}年 {pollutant} 浓度", f"{city_val:.1f} μg/m³")
        st.metric("🏆 全国主要城市排名", f"{rank} / {total}")
        st.markdown(f"**污染等级**：<span style='color:{level_color}; font-weight:bold;'>{level_text}</span>", unsafe_allow_html=True)

        st.markdown(f"**📅 历年{pollutant}数据**")
        city_history = df_main[df_main['城市'] == selected_city].groupby('年份')['PM2.5'].mean().round(1).reset_index()
        city_history.columns = ['年份', 'PM2.5 (μg/m³)']
        st.dataframe(city_history.set_index('年份'), use_container_width=True)

    else:
        st.info("请选择一个城市")


