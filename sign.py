import streamlit as st
st.set_page_config(layout="centered" , page_title="회원가입")
import Domain
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, add_page_title, hide_pages, Section
from streamlit_extras.colored_header import colored_header
from streamlit_extras.app_logo import add_logo


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
        Page("analysis.py", "검사결과", ""),
        Page("dt_list.py", "감지목록", ""),
        Page("subscribe.py", "구독", ""),
        Section(name=""),
        Page("mypage.py", "My Page", ""),
        Page("update.py", "회원 정보 수정", ""),
        Page("delete.py", "회원 탈퇴", "")

    ]
)

hide_pages(
            ["로그인", "회원 정보 수정", "구독", "회원 탈퇴", "로그아웃", "My Page", "감지", "검사결과", "감지목록"]
)

st.markdown('''
            <style>
                #sign {
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

side_col1, side_col2 = st.sidebar.columns([2,1])

with side_col1:
    if st.button("로그인"):
        switch_page("로그인")

with side_col2:
    if st.button("회원가입"):
        switch_page("회원가입")

colored_header(
        label="Sign",
        description="",
        color_name="blue-70"
    )

Domain.signin_page()
if st.session_state.status == 'success':
    switch_page("로그인")
