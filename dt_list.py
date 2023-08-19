import streamlit as st
st.set_page_config(layout="centered", page_title="검사목록")
import pymysql
import Domain
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, add_page_title, hide_pages, Section
import time
from PIL import Image
from streamlit_extras.app_logo import add_logo
from streamlit_extras.grid import grid
import pandas as pd
import numpy as np
import datetime
from streamlit_extras.colored_header import colored_header
from streamlit_extras.stylable_container import stylable_container


add_logo("logo.png", height=100)

with open('css/main.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

if not st.session_state.get("logged_in_user"):
    st.session_state.logged_in_user = None


show_pages(
    [
        Page("main.py", "Main", ""),
        Page("login.py", "로그인", ""),
        Page("sign.py", "회원가입", ""),
        Page("logout.py", "로그아웃", ""),
        Page("detect.py", "감지", ""),
        Page("analysis.py", "검사결과", ""),
        Page("dt_list.py", "감지목록", ""),
        Section(name=""),
        Page("mypage.py", "My Page", ""),
        Page("update.py", "회원 정보 수정", ""),
        Page("delete.py", "회원 탈퇴", "")

    ]
)
st.markdown('''
    <style>
        #detecting-list {
            font-size : 55px;
        }
        div[data-testid="stSidebarNav"] {
            height : 90vh;
        }        
        div[data-testid="stSidebarNav"] > ul {
            max-height: 90vh;
        }
        .element-container > .stButton {
            text-align : right;        
        }    
        button[kind="secondary"] {
            background: rgba(184,6,112,0.3);
        }
        button[data-baseweb="tab"] {
            background : none !important;
            width : 100px;
        }
       
</style>
            ''',
            unsafe_allow_html=True)

colored_header(
        label="Detecting List",
        description="",
        color_name="blue-70"
    ) 
css_style="""
        {
            border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                background : rgba(25,27,38,0.6); 
        }
        """
if st.session_state.logged_in_user == None:
    hide_pages(
            ["로그인", "회원가입", "로그아웃", "감지", "감지목록", "검사결과", "My Page", "회원 정보 수정", "회원 탈퇴"]
)
    container = st.empty()
    container.error("로그인을 해주세요")  # Create a success alert
    time.sleep(1)  # Wait 3 seconds
    container.empty()
    switch_page("로그인")
else:
    hide_pages(
                ["로그인", "회원가입", "로그아웃", "회원 정보 수정", "회원 탈퇴"]
    )

    if st.sidebar.button("로그아웃", key="logout2"):
            if st.session_state.logout2 == True:
                st.session_state.logged_in_user = None
                switch_page("로그아웃")

    with stylable_container(
            key="container_with_border",
            css_styles=css_style):
        tab1, tab2, tab3 = st.tabs(["오늘", "구간", "전체"])
        with tab1:
            d1 = datetime.date.today()
            datas = Domain.get_data_info(st.session_state.logged_in_user)
            date_first_seen = []
            label = []
            for i in range(0,len(datas)):
                if datas[i].get('date_first_seen').date() == d1:
                    date_first_seen.append(datas[i].get('date_first_seen'))
                    label.append(datas[i].get('label'))
            data = {'감지시간': date_first_seen,
                        '상태': label}
            df = pd.DataFrame(data)
            df.index = df.index+1

            st.table(df)
            
        with tab2:
            min_date = datetime.datetime(2023,8,1)
            max_date = datetime.date.today()

            d2 = st.date_input("확인할 감지 날짜를 선택해주세요", (min_date, max_date))
            datas = Domain.get_data_info(st.session_state.logged_in_user)
            date_first_seen = []
            label = []
            if d2[0] is not None and d2[-1] is not None:
                for i in range(0,len(datas)):
                    if d2[0] <= datas[i].get('date_first_seen').date() <= d2[-1]:
                        date_first_seen.append(datas[i].get('date_first_seen'))
                        label.append(datas[i].get('label'))
                data = {'감지시간': date_first_seen,
                        '상태': label}

                df = pd.DataFrame(data)
                df.index = df.index+1

                st.table(df)


        
        with tab3:
            datas = Domain.get_data_info(st.session_state.logged_in_user)
            date_first_seen = []
            label = []
            for i in range(0,len(datas)):
                date_first_seen.append(datas[i].get('date_first_seen'))
                label.append(datas[i].get('label'))
            data = {'감지시간': date_first_seen,
                    '상태': label}

            df = pd.DataFrame(data)
            df.index = df.index+1

            st.table(df)