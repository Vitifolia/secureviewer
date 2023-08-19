import streamlit as st
st.set_page_config(layout="wide", initial_sidebar_state="collapsed", page_title="검사결과")
import Domain
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages, Section
import time
from markdownlit import mdlit
import pandas as pd
import streamlit.components.v1 as components
import openai
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.stateful_button import button
from streamlit_extras.colored_header import colored_header
from streamlit_extras.app_logo import add_logo
import datetime


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



st.markdown('''
<style>
    
    iframe {
            width : 900px;
    height : 550px;
        
    }
            .reportview-container .main .block-container{
        max-width: percentage_width_main%;
        padding-top: 0;
        padding-right: -200px;
        padding-left: -200px;
        padding-bottom: 1rem;
    }

        .uploadedFile {
            display: none
            }
        footer {
            visibility: hidden;
            }

        #report {
            font-size : 55px;
            }

        div[data-testid="stSidebarNav"] {
            height : 90vh;
            }        
        div[data-testid="stSidebarNav"] > ul {
            max-height: 90vh;
            }
        .element-container > .stButton {
            text-align : center;        
            }    
        button[kind="secondary"] {
                background: rgba(184,6,112,0.3);
            }    
</style>
            ''',
            unsafe_allow_html=True)

if st.sidebar.button("로그아웃", key="logout2"):
            if st.session_state.logout2 == True:
                st.session_state.logged_in_user = None
                switch_page("로그아웃")

openai.api_key = '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'

 
def generate_response(prompt):
    completions = openai.Completion.create (
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=3000,
        stop=None,
        temperature=0,
        top_p=1,
    )
 
    message = completions["choices"][0]["text"].replace("\n", "")
    return message
 
if 'generated' not in st.session_state:
            st.session_state['generated'] = []
 
if 'past' not in st.session_state:
            st.session_state['past'] = []


css_style="""
        {
            border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                background : rgba(25,27,38,0.6); 
                text-align : center;
        }
        """



if st.session_state.logged_in_user == None:
    hide_pages(
            ["로그인", "회원가입", "로그아웃", "감지", "구독", "감지목록", "검사결과", "My Page", "회원 정보 수정", "회원 탈퇴"]
)
    container = st.empty()
    container.error("로그인을 해주세요")  # Create a success alert
    time.sleep(1)  # Wait 3 seconds
    container.empty()
    switch_page("로그인")
else:


    hide_pages(
                ["로그인", "회원가입", "회원 정보 수정", "구독", "회원 탈퇴", "로그아웃"]
    )

    colored_header(
        label="Report",
        description="",
        color_name="blue-70"
    ) 

    with stylable_container(
                    key="container_with_border",
                    css_styles=css_style):
        attack = Domain.get_attack_data_info(st.session_state.logged_in_user)
        cnt = attack['count(label)']
        mdlit(f'''## 오늘 총 [red]{cnt}[/red]회 공격받았습니다.''')

        datas = Domain.get_all_data_info(st.session_state.logged_in_user)
        proto = []
        flags = []
        tos = []
        label = []
        for i in range(0,len(datas)):
            proto.append(datas[i].get('proto'))
            flags.append(datas[i].get('flags'))
            tos.append(datas[i].get('tos'))
            label.append(datas[i].get('label'))
        data = {'프로토콜': proto,
                'Flags' : flags,
                'Tos' : tos,
                '상태': label}

        df = pd.DataFrame(data)

        send_data1 = f'{data}와 같은 상황에서 proto,flags,tos가 어떤 상태일때 공격이 들어오는지 분석하고 이에 따른 사이버보안방법을 알려줘'
        send_data = '스마트인재개발원에 대해 알려줘'

        col1, col2 = st.columns([0.7, 0.3])

        with open("날짜별 악성 접근 빈도_tab.html", "r",encoding="UTF-8") as file:
            html_code1 = file.read()
            with col1:
                st.components.v1.html(html_code1)
        
            with col2:
                if button('자세히 분석실행 GPT',key='gpt_btn'):
                
                    with stylable_container(
                        key="container_with_border",
                        css_styles=css_style):
                        output = generate_response(send_data1)
                        st.write(output)
                        now = datetime.now()
                        # 년, 월, 일 형식으로 포맷팅
                        formatted_datetime = now.strftime("%Y-%m-%d %H:%M")
                        st.download_button("분석결과", output, file_name=f"{formatted_datetime} 분석결과.txt")        

            df = pd.DataFrame(data)  


        col3, col4 = st.columns([2,3])


        with open("접근 목적_pie.html", "r",encoding="UTF-8") as file:
            html_code2 = file.read()
            with col3:
                st.components.v1.html(html_code2)

        with open("총 Flags_pie-rose.html", "r",encoding="UTF-8") as file:
            html_code3 = file.read()
            with col4:
                st.components.v1.html(html_code3)




        




    

