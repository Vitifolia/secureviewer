import streamlit as st
st.set_page_config(layout="centered", page_title="로그인")
import Domain
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, add_page_title, hide_pages, Section
import time
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
            ["로그인", "회원가입", "회원 정보 수정", "구독", "회원 탈퇴", "로그아웃", "감지", "감지목록", "검사결과", "My Page"]
)

side_col1, side_col2 = st.sidebar.columns([2,1])

with side_col1:
    if st.button("로그인"):
        switch_page("로그인")

with side_col2:
    if st.button("회원가입"):
        switch_page("회원가입")



if not st.session_state.get("logged_in_user"):
    st.session_state.logged_in_user = None
    

if not st.session_state.get("status"):
    st.session_state.status = None

if st.session_state.status == 'success':
    container = st.empty()
    container.success("회원가입에 성공했습니다.")  # Create a success alert
    time.sleep(1)  # Wait 1 seconds
    st.session_state.status = None
    container.empty()


colored_header(
        label="Login",
        description="",
        color_name="blue-70"
    )
st.markdown('''
            <style>
                #login {
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

Domain.login_page()

if st.session_state.logged_in_user != None:
    st.session_state.login_chk = '1'
    switch_page("Main")

