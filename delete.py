import streamlit as st
st.set_page_config(layout="centered", page_title="회원탈퇴")
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
        Section(name=""),
        Page("mypage.py", "My Page", ""),
        Page("update.py", "회원 정보 수정", ""),
        Page("delete.py", "회원 탈퇴", "")

    ]
)



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
                ["로그인", "회원가입", "로그아웃", "My Page", "회원 정보 수정", "회원 탈퇴"]
    )

    st.markdown('''
            <style>
                #leave {
                font-size : 55px;
                }
                div[data-testid="stSidebarNav"] {
                    height : 90vh;
                }        
                div[data-testid="stSidebarNav"] > ul {
                    max-height: 90vh;
                }
                button[kind="secondary"] {
                background: rgba(184,6,112,0.3);
                }
                .element-container > .stButton {
                text-align : center;        
                }
            </style>
            ''',
            unsafe_allow_html=True)

    if st.sidebar.button("로그아웃", key="logout2"):
            if st.session_state.logout2 == True:
                st.session_state.logged_in_user = None
                switch_page("로그아웃")

    colored_header(
        label="Leave",
        description="",
        color_name="blue-70"
    )

    Domain.delete_page()
    if st.session_state.status == 'success':
        container = st.empty()
        container.success("탈퇴가 완료 되었습니다.")  # Create a success alert
        time.sleep(1)  # Wait 2 seconds
        st.session_state.status = None
        container.empty()
        switch_page("Main")