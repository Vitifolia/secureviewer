import streamlit as st
st.set_page_config(page_title="My Page" ,layout="centered")
import pymysql
import Domain
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, add_page_title, hide_pages, Section
import time
from PIL import Image
from streamlit_extras.app_logo import add_logo
from streamlit_extras.colored_header import colored_header
from streamlit_extras.stylable_container import stylable_container
from datetime import datetime, date



add_logo("logo.png", height=100)
with open('css/main.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

show_pages(
    [
        Page("main.py", "Main", ""),
        Page("login.py", "로그인", ""),
        Page("sign.py", "회원가입", ""),
        Page("logout.py", "로그아웃", ""),
        Page("detect.py", "감지", ""),
        Page("subscribe.py", "구독", ""),
        Page("analysis.py", "검사결과", ""),
        Page("dt_list.py", "감지목록", ""),
        Section(name=""),
        Page("mypage.py", "My Page", ""),
        Page("update.py", "회원 정보 수정", ""),
        Page("delete.py", "회원 탈퇴", "")

    ]
)
if not st.session_state.get("logged_in_user"):
    st.session_state.logged_in_user = None
    
if not st.session_state.get("logged_in_user_tel"):
    st.session_state.logged_in_user_tel = None

st.markdown('''
            <style>
                #my-page {
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
            </style>
            ''',
            unsafe_allow_html=True)
    

if st.session_state.logged_in_user == None:
    hide_pages(
            ["로그인", "회원가입", "로그아웃", "구독", "감지", "감지목록", "검사결과", "My Page", "회원 정보 수정", "회원 탈퇴"]
)
    container = st.empty()
    container.error("로그인을 해주세요")  # Create a success alert
    time.sleep(1)  # Wait 3 seconds
    container.empty()
    switch_page("로그인")
else:
    hide_pages(
                ["로그인", "회원가입", "로그아웃", "구독", "회원 정보 수정", "회원 탈퇴"]
    )
    
    Domain.sub_chk(st.session_state.logged_in_user)

    if st.sidebar.button("로그아웃", key="logout2"):
            if st.session_state.logout2 == True:
                st.session_state.logged_in_user = None
                switch_page("로그아웃")

                
    colored_header(
        label="My Page",
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

    member_info = Domain.get_member_info(st.session_state.logged_in_user)
    Domain.sub_chk(st.session_state.get("logged_in_user"))
    date1 = date.today()

    col3, col4 = st.columns([2,5])
    with col3:
            st.markdown("### 기업명")
        
            st.markdown("### 아이디")
        
            st.markdown("### 전화번호")

            
            st.markdown("### 구독")
            if date1 <= member_info['exp_at']:
                st.markdown("### 구독만료일")

    with col4:
        with stylable_container(
            key="container_with_border",
            css_styles=css_style):    
            st.markdown(f"### {member_info['user_info']}")
        with stylable_container(
            key="container_with_border",
            css_styles=css_style):
            st.markdown(f"### {member_info['user_id']}")
        with stylable_container(
            key="container_with_border",
            css_styles=css_style):
            st.markdown(f"### {member_info['user_tel']}")
        with stylable_container(
            key="container_with_border",
            css_styles=css_style):
            st.markdown(f"### {member_info['svc_status']}")

        if date1 <= member_info['exp_at']:
            with stylable_container(
                key="container_with_border",
                css_styles=css_style):
                st.markdown(f"### {member_info['exp_at']}")

    col1, col2, col3 = st.columns([4,1.5,1.3])
    col1.button('구독', key='subscribe')
    col2.button('회원정보수정', key='user_update')
    col3.button('회원 탈퇴', key='user_delete')
    if st.session_state.subscribe == True:
        switch_page("구독")
    if st.session_state.user_update == True:
        switch_page("회원 정보 수정")
    if st.session_state.user_delete == True:
        switch_page("회원 탈퇴")
    
