import streamlit as st
st.set_page_config(layout="centered", page_title="Secure Viewer")
import pymysql
import scapy_run
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, add_page_title, hide_pages, Section
import time
from PIL import Image
from streamlit_extras.app_logo import add_logo
from markdownlit import mdlit
from streamlit_extras.grid import grid
import pandas as pd
import numpy as np
from pyecharts.charts import Bar
from pyecharts import options as opts
import streamlit.components.v1 as components
from streamlit_extras.stylable_container import stylable_container




img = Image.open('img.png')

add_logo("logo.png", height=100)

with open('css/main.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
st.markdown('''
<style>
    
    iframe {
        
        height : 550px;
        
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
    div[data-testid="stImage"] {
        margin : 0 auto;
    }      
</style>
            ''',
            unsafe_allow_html=True)

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
    
if not st.session_state.get("login_chk"):
    st.session_state.login_chk = None
    
if not st.session_state.get("dt_status"):
    st.session_state.dt_status = None


def main():
    
    if st.session_state.login_chk == '1':
        container = st.empty()
        container.success(f"{st.session_state.logged_in_user}님 환영합니다.")  # Create a success alert
        time.sleep(1)  # Wait 2 seconds
        st.session_state.login_chk = None
        container.empty()

    
    if st.session_state.logged_in_user == None:
        hide_pages(
            ["로그인", "회원가입", "로그아웃", "감지", "구독", "검사결과", "감지목록", "My Page", "회원 정보 수정", "회원 탈퇴"]
)
        side_col1, side_col2 = st.sidebar.columns([2,1])

        with side_col1:
            if st.button("로그인"):
                switch_page("로그인")

        with side_col2:
            if st.button("회원가입"):
                switch_page("회원가입")

        

        
    else:
        hide_pages(
            ["로그인", "회원가입", "회원 정보 수정", "구독", "회원 탈퇴", "로그아웃"]
)
        if st.session_state.login_chk == '1':
            container = st.empty()
            container.success(f"{st.session_state.logged_in_user}님 환영합니다.")  # Create a success alert
            time.sleep(1)  # Wait 1 seconds
            st.session_state.login_chk = None
            container.empty()

        
        
        if st.sidebar.button("로그아웃", key="logout2"):
            if st.session_state.logout2 == True:
                st.session_state.logged_in_user = None
                switch_page("로그아웃")

    css_style="""
        {
            border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                background : rgba(25,27,38,0.6); 
        }
        """
    with stylable_container(key="container_with_border",
    css_styles=css_style):   
        
        st.image("img.png", width=450)
        mdlit('''### 안녕하십니까? 저희 [green]"Secure Viewer"[/green] 를 찾아주셔서 감사합니다.''')

        mdlit('''[green]"Secure Viewer"[/green]는 데이터 시각화 분야에서 선도적인 기업으로, 고객들에게 안전하고 효과적인 데이터 시각화 솔루션을 제공하고 있습니다. 
        또한, 혁신적인 데이터 시각화 솔루션을 개발하여 기업들이 데이터의 가치를 최대한 끌어내고, 
        비즈니스 인텔리전스를 활용하여 경쟁 우위를 얻을 수 있도록 지원하고 있습니다. 
        다양한 데이터 시각화 형식을 지원하여 고객들이 자신들의 데이터를 가장 효과적으로 시각화할 수 있도록 돕습니다. ''')

        with open("test1.html", "r", encoding='utf-8') as file:
            html_code1 = file.read()
            st.components.v1.html(html_code1)
     
        mdlit(''' [green]"Secure Viewer"[/green]는 데이터 시각화 뿐만 아니라 데이터 분석에도 중점을 두고 있습니다. 
        고급 분석 기능을 통해 데이터의 패턴, 추세, 통계 등을 깊이 있게 분석하여 더 나은 의사 결정을 가능하게 합니다.
        각 기업의 요구 사항에 맞게 시각화와 분석 도구를 수정하고 조정할 수 있습니다. 
        이로써 각 조직은 자신만의 독특한 데이터 시각화 솔루션을 구축할 수 있습니다.''')

        mdlit('''[green]"Secure Viewer"[/green]는 혁신적인 데이터 시각화와 분석을 통해 기업들이 더 나은 비즈니스 전략을 개발하고, 효율성을 극대화하며, 미래에 대한 확신을 가질 수 있도록 지원합니다. 
            많은 이용바랍니다. 감사합니다.''')

        with open("test2.html", "r", encoding='utf-8') as file:
            html_code3 = file.read()

            st.components.v1.html(html_code3)

if __name__ == "__main__":
    main()