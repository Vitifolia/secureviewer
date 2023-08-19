import streamlit as st
st.set_page_config(layout="centered", page_title="구독")
import pymysql
import Domain
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, add_page_title, hide_pages, Section
import time
from PIL import Image
from streamlit_extras.app_logo import add_logo
from streamlit_extras.colored_header import colored_header
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

if not st.session_state.get("logged_in_user"):
    st.session_state.logged_in_user = None

colored_header(
        label="Subscribe",
        description="",
        color_name="blue-70"
    )

if st.sidebar.button("로그아웃", key="logout2"):
            if st.session_state.logout2 == True:
                st.session_state.logged_in_user = None
                switch_page("로그아웃")

                
st.markdown('''
            <style>
            #subscribe {
                font-size : 55px;
                }
            
            div[data-testid="stSidebarNav"] {
                height : 90vh;
            }        
            div[data-testid="stSidebarNav"] > ul {
                max-height: 90vh;
            }
            .stButton {
                text-align : center;
            }
            button[kind="secondary"] {
                background: rgba(184,6,112,0.3);
            }
            div[data-testid="stMarkdownContainer"] {
                text-align : center;
            }
            </style>
            ''',
            unsafe_allow_html=True
            )


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

    css_style="""
        {
            border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                background : rgba(25,27,38,0.6); 
        }
        """


    col1, col5, col2 = st.columns([2,1,2])
    with col1:
        with stylable_container(
                key="container_with_border",
                css_styles=css_style): 
            st.markdown("### Month")
            st.write('')          
            st.write('')   
            st.markdown("#### 구독 30,000 won")
            st.write('') 
            st.write('')         
            st.write('') 
            st.write('')           
                    
                    
                    
            if st.button("1달 구독"):
                Domain.sub_month(st.session_state.logged_in_user)
                switch_page("My Page")

            
    with col2:
        with stylable_container(
                key="container_with_border",
                css_styles=css_style): 
            st.markdown("### Year")
            st.write('') 
            st.write('') 
            st.markdown(' #### 구독 300,000 won')
            st.markdown(' #### 약 17% 절약') 
            st.write('')     
                    
                    
                    
                
            if st.button("1년 구독"):
                Domain.sub_year(st.session_state.logged_in_user)
                switch_page("My Page")
    
    

