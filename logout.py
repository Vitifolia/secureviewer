import streamlit as st
st.set_page_config(layout="centered", page_title="로그아웃")
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, add_page_title, hide_pages, Section
import time
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
            ["로그인", "회원가입", "회원 정보 수정", "구독", "회원 탈퇴", "로그아웃", "My Page"]
)
if not st.session_state.get("logged_in_user"):
    st.session_state.logged_in_user = None
    

if st.session_state.logged_in_user == None:
    container = st.empty()
    container.success("로그아웃 완료")  # Create a success alert
    time.sleep(1)  # Wait 2 seconds
    container.empty()
    st.session_state.is_logged_in = False
    switch_page("Main")