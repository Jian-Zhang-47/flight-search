import streamlit as st
import datetime


st.title("机票查询")
col1, col2, col3, col4 = st.columns(4)
# 单程或往返选择
with col1:
    st.markdown("""
<style>
    div[data-testid="stRadio"] > div {
        flex-direction: row;
    }
</style>
""", unsafe_allow_html=True)
    
    T = st.radio('请选择：', ['单程', '往返'])
# 舱位选择
with col4:
    C = st.selectbox('请选择舱位：', ['不限舱等', '经济舱', '公务/头等舱'])

col1, col2, col3, col4 = st.columns(4)
# 出发城市
with col1:
    A_name = st.text_input(
        "出发城市:",
        key="A_name",
        placeholder="例如：Beijing",
        help="请输入城市的拼音或英文名称"
    )
# 到达城市
with col2:
    B_name = st.text_input(
        "到达城市:",
        key="B_name",
        placeholder="例如：Shanghai",
        help="请输入城市的拼音或英文名称"
    )
# 出发日期和返回日期
with col3:
    A_date = st.date_input("请选择出发日期:", datetime.date.today())
with col4:
    B_date = None
    if T == '往返':
        B_date = st.date_input("请选择返回日期:", datetime.date.today())

col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
# 人数
with col1:
    adult_n = st.number_input("成人:", min_value=1, max_value=10, step=1, value=1)
with col2:
    child_n = st.number_input("儿童:", min_value=0, max_value=10, step=1, value=0)
with col3:
    infant_n = st.number_input("婴儿:", min_value=0, max_value=10, step=1, value=0)

import webbrowser
from airportsdata import load

def if_round(T):
    if T == '单程':
            x = 'oneway'
    elif T == '往返':
            x = 'round'
    return x

def cabin(C):
    if C == '不限舱等':
        x = 'y_s_c_f'
    elif C == '经济舱':
        x = 'y'
    elif C == '公务/头等舱':
        x = 'c_f'

airports = load("IATA")  # 加载 IATA 代码数据

def get_city_code(city_name):
    for code, data in airports.items():
        if city_name.lower() in data['city'].lower():
            return code
    return "Unknown"

def xiecheng_search(departure, destination, T, A_date, B_date, C, adult, child, infant):
    base_url = "https://flights.ctrip.com/online/list/"
    departure_encoded = get_city_code(departure)
    destination_encoded = get_city_code(destination)
    oneway_or_round = if_round(T)
    cabin_type = cabin(C)
    if T == '单程':          
        date = f'{A_date}'
    elif T == '往返':
        date = f'{A_date}_{B_date}'

    search_url = f"{base_url}{oneway_or_round}-{departure_encoded}-{destination_encoded}?depdate={date}&cabin={cabin_type}&adult={adult}&child={child}&infant={infant}"

    # 打开默认浏览器
    webbrowser.open(search_url)

if st.button("携程"):
    if not A_name or not B_name:
        st.error("请完整填写出发城市和到达城市！")
    elif T == '往返' and B_date < A_date:
        st.error("返回日期不能早于出发日期，请重新选择！")
    else:
        xiecheng_search(A_name, B_name, T, A_date, B_date, C, adult_n, child_n, infant_n)
        st.success("已查询携程")

          