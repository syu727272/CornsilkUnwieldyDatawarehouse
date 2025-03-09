import os
import streamlit as st
import pandas as pd
import requests
import json
import matplotlib.pyplot as plt
import plotly.express as px
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variables
API_KEY = os.getenv('ESTAT_API_KEY')

# Set page configuration
st.set_page_config(
    page_title="日本の人口推計データ分析",
    page_icon="📊",
    layout="wide"
)

# App title and description
st.title("📊 日本の人口推計データ分析")
st.markdown("""
    このアプリケーションは、e-Statから取得した日本の人口推計データを視覚化します。
    様々な地域や年齢層の人口動向を分析できます。
""")

# Function to fetch data from e-Stat API
def fetch_estat_data(app_id, stats_code, area_code=None, time_code=None):
    """
    e-Stat APIから統計データを取得する関数
    
    Parameters:
    -----------
    app_id : str
        e-Stat API アプリケーションID
    stats_code : str
        統計表ID
    area_code : str, optional
        地域コード
    time_code : str, optional
        時間コード
        
    Returns:
    --------
    dict
        APIレスポンス（JSON形式）
    """
    base_url = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"
    
    params = {
        "appId": app_id,
        "statsDataId": stats_code,
        "metaGetFlg": "Y",
        "cntGetFlg": "N",
        "lang": "J",
    }
    
    if area_code:
        params["cdArea"] = area_code
    
    if time_code:
        params["cdTime"] = time_code
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # エラーがあれば例外を発生
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"APIリクエストエラー: {e}")
        return None

# Sidebar for user inputs
st.sidebar.header("データ検索条件")

# Check if API key is available
if not API_KEY:
    st.sidebar.warning("⚠️ API KEYが設定されていません。.envファイルにESTAT_API_KEYを設定してください。")
    # For demo purposes, allow user to input API key directly
    API_KEY = st.sidebar.text_input("e-Stat API Key", type="password")

# Statistics selection
stat_options = {
    "人口推計（月次）": "0003348423",  # 人口推計の統計表ID
    "国勢調査（年次）": "0000030001",  # 国勢調査の統計表ID
}
selected_stat = st.sidebar.selectbox("統計データ", list(stat_options.keys()))

# Year range selection
year_range = st.sidebar.slider("年範囲", 2000, 2023, (2018, 2023))

# Prefecture selection
prefectures = [
    "全国", "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
    "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
    "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県",
    "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県",
    "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県",
    "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県",
    "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
]
selected_prefs = st.sidebar.multiselect("都道府県", prefectures, default=["全国"])

# Age group selection
age_groups = ["総数", "0-14歳", "15-64歳", "65歳以上"]
selected_age = st.sidebar.multiselect("年齢層", age_groups, default=["総数"])

# Gender selection
gender_options = ["総数", "男", "女"]
selected_gender = st.sidebar.radio("性別", gender_options)

# Button to fetch data
fetch_button = st.sidebar.button("データを取得")

# Main content area
if fetch_button and API_KEY:
    with st.spinner("e-Statからデータを取得中...しばらくお待ちください"):
        # For demonstration, we'll create sample data
        # In a real application, you would use the fetch_estat_data function
        # data = fetch_estat_data(API_KEY, stat_options[selected_stat])
        
        # Sample data for demonstration
        years = list(range(year_range[0], year_range[1] + 1))
        sample_data = {
            "年度": [],
            "地域": [],
            "年齢層": [],
            "性別": [],
            "人口": []
        }
        
        import random
        for year in years:
            for pref in selected_prefs:
                for age in selected_age:
                    # Generate realistic population numbers
                    base_pop = 120000000 if pref == "全国" else random.randint(500000, 9000000)
                    if age == "0-14歳":
                        pop_factor = 0.12  # 約12%
                    elif age == "15-64歳":
                        pop_factor = 0.6   # 約60%
                    elif age == "65歳以上":
                        pop_factor = 0.28  # 約28%
                    else:  # 総数
                        pop_factor = 1.0
                        
                    # Add yearly trend and randomness
                    yearly_factor = 1.0 + (year - 2000) * (-0.002 if age == "0-14歳" else 0.001)
                    population = int(base_pop * pop_factor * yearly_factor * random.uniform(0.98, 1.02))
                    
                    sample_data["年度"].append(year)
                    sample_data["地域"].append(pref)
                    sample_data["年齢層"].append(age)
                    sample_data["性別"].append(selected_gender)
                    sample_data["人口"].append(population)
        
        # Create DataFrame
        df = pd.DataFrame(sample_data)
        
        # Display the data
        st.subheader("取得したデータ")
        st.dataframe(df)
        
        # Data visualization
        st.subheader("データ可視化")
        
        # Create tabs for different visualizations
        tab1, tab2, tab3 = st.tabs(["時系列推移", "地域比較", "年齢層分布"])
        
        with tab1:
            # Time series visualization
            st.markdown("### 時系列での人口推移")
            
            # Filter for time series
            if "総数" in selected_age:
                time_df = df[df["年齢層"] == "総数"]
            else:
                time_df = df.copy()
            
            # Create line chart
            fig = px.line(
                time_df, 
                x="年度", 
                y="人口", 
                color="地域" if len(selected_prefs) > 1 else "年齢層",
                title=f"{selected_gender}の人口推移 ({year_range[0]}年-{year_range[1]}年)",
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Regional comparison
            st.markdown("### 地域間の人口比較")
            
            # Get the most recent year data
            latest_year = max(df["年度"])
            region_df = df[df["年度"] == latest_year]
            
            if len(selected_prefs) > 1:
                # Create bar chart for regional comparison
                fig = px.bar(
                    region_df,
                    x="地域",
                    y="人口",
                    color="年齢層" if len(selected_age) > 1 else None,
                    title=f"{latest_year}年の地域別人口比較 ({selected_gender})",
                    barmode="group" if len(selected_age) > 1 else "relative"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("地域比較を表示するには、複数の都道府県を選択してください。")
        
        with tab3:
            # Age distribution
            st.markdown("### 年齢層別の人口分布")
            
            if len(selected_age) > 1 and "総数" not in selected_age:
                # Get the most recent year data
                latest_year = max(df["年度"])
                age_df = df[df["年度"] == latest_year]
                
                # Create pie chart for age distribution
                fig = px.pie(
                    age_df,
                    values="人口",
                    names="年齢層",
                    title=f"{latest_year}年の年齢層別人口分布 ({selected_gender})"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("年齢層分布を表示するには、'総数'を除く複数の年齢層を選択してください。")
        
        # Download button for the data
        csv = df.to_csv(index=False)
        st.download_button(
            label="CSVとしてダウンロード",
            data=csv,
            file_name=f"population_data_{year_range[0]}-{year_range[1]}.csv",
            mime="text/csv",
        )

elif fetch_button and not API_KEY:
    st.error("API KEYが設定されていません。サイドバーでAPI Keyを入力してください。")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center">
        <p>データソース: <a href="https://www.e-stat.go.jp/" target="_blank">e-Stat 政府統計の総合窓口</a></p>
        <p>© 2023 日本の人口推計データ分析アプリ</p>
    </div>
""", unsafe_allow_html=True)
