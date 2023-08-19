import streamlit as st
st.set_page_config(layout="centered", page_title="감지")
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, add_page_title, hide_pages, Section
import time
from PIL import Image
from streamlit_extras.app_logo import add_logo
from markdownlit import mdlit
from streamlit_extras.grid import grid
import pandas as pd
import streamlit.components.v1 as components
from streamlit_extras.colored_header import colored_header
from streamlit_extras.stateful_button import button
import scapy_run
from streamlit_extras.stylable_container import stylable_container


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

colored_header(
        label="Detecting",
        description="",
        color_name="blue-70"
    )


st.markdown('''
            <style>
            #detecting {
                font-size : 55px;
                }
            div[data-testid="stImage"] {
                text-align : center;
                margin : 0 auto;
            }
            .stButton {
                text-align : center;
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
            unsafe_allow_html=True
            )

css_style="""
        {
            
            text-align : center !important;
        }
        """

if not st.session_state.get("logged_in_user"):
    st.session_state.logged_in_user = None

if not st.session_state.get("dt_status"):
    st.session_state.dt_status = None

if not st.session_state.get("svc_status"):
    st.session_state.svc_status = None

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
    if st.session_state.svc_status != 'Y':
        container = st.empty()
        container.error("구독 후 이용가능합니다.")  # Create a success alert
        time.sleep(2)  # Wait 2 seconds
        container.empty()
        switch_page("구독")
    
    else:
        if st.sidebar.button("로그아웃", key="logout2"):
                if st.session_state.logout2 == True:
                    st.session_state.logged_in_user = None
                    switch_page("로그아웃")
        
        
        with stylable_container(
                key="container_with_border",
                css_styles=css_style):
            scapy_run.main()



