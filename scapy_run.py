import streamlit as st
import pymysql
import datetime
import pandas as pd
import joblib
from lightgbm import LGBMClassifier
from scapy.all import *
from streamlit_extras.add_vertical_space import add_vertical_space
import graph
from streamlit_extras.switch_page_button import switch_page
import time
import SMS


# MySQL 서버 연결 정보 설정
db_config = {
    "host": "project-db-campus.smhrd.com",
    "user": "secure",
    "password": "1234",
    "database": "secure",
    "port": 3312
}

st.markdown('''
            <style>
            div[data-testid="stImage"] {
                text-align : center;
                margin : 0 auto;
            }
            </style>
            ''',
            unsafe_allow_html=True)

current_datetime = datetime.today()
formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
# MySQL 연결 생성
db_connection = pymysql.connect(**db_config)
db_cursor = db_connection.cursor()

# 머신러닝 모델 불러오기
load_model_lgbm = joblib.load("lgbm_model.pkl")

# ... (기존 코드를 여기에 추가)
def insert_packet_data(proto, src_ip, dst_ip, src_pt, dst_pt, flags, tos, label):
    # INSERT 쿼리 작성
    insert_query = ("INSERT INTO tb_data (date_first_seen, proto, src_ip_addr, dst_ip_addr, src_pt, dst_pt, flags, tos, label, user_id) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    values = (datetime.now(), proto, src_ip, dst_ip, src_pt, dst_pt, flags, tos, label, f"{st.session_state.logged_in_user}")
    if label == 'attacker':
        SMS.send_sms()
    else:
        status = st.empty()
        status.write("")
        status.empty()
    # 데이터베이스에 쿼리 실행
    db_cursor.execute(insert_query, values)
    db_connection.commit()

# 변수 초기화
x_test = None
proto = None
src_pt = None
dst_pt = None
flags = None
tos = None
label = None

def packet_callback(packet):
    # 전역 변수 사용
    global x_test
    global proto
    global src_pt
    global dst_pt
    global flags
    global tos
    global label

    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        tos = packet[IP].tos

        if TCP in packet:
            proto = "TCP"
            src_pt = packet[TCP].sport
            dst_pt = packet[TCP].dport
            flags = packet[TCP].flags

            # 패킷 데이터 확인
            print(f"Proto: {proto}, Src IP Addr: {src_ip}, Dst IP Addr: {dst_ip}, "
                  f"Src Pt: {src_pt}, Dst Pt: {dst_pt}, Flags: {flags}, Tos: {tos}")

            # 데이터 프레임 생성
            x_test = pd.DataFrame([[proto, src_pt, dst_pt, flags, tos]],
                                     columns=["Proto", "Src Pt", "Dst Pt", "Flags", "Tos"])

        elif UDP in packet:
            proto = "UDP"
            src_pt = packet[UDP].sport
            dst_pt = packet[UDP].dport
            flags = "none"  # UDP 패킷에는 플래그가 없습니다.

            # 패킷 데이터 확인
            print(f"Proto: {proto}, Src IP Addr: {src_ip}, Dst IP Addr: {dst_ip}, "
                  f"Src Pt: {src_pt}, Dst Pt: {dst_pt}, Flags: {flags}, Tos: {tos}")

            # 데이터 프레임 생성
            x_test = pd.DataFrame([[proto, src_pt, dst_pt, flags, tos]],
                                     columns=["Proto", "Src Pt", "Dst Pt", "Flags", "Tos"])

        x_test["Proto"] = x_test["Proto"].astype("category")
        x_test["Src Pt"] = x_test["Src Pt"].astype("int32")
        x_test["Dst Pt"] = x_test["Dst Pt"].astype("int32")
        x_test["Flags"] = x_test["Flags"].astype("category")
        x_test["Tos"] = x_test["Tos"].astype("int32")

        label = load_model_lgbm.predict(x_test)[0]

        # 데이터 프레임 생성
        result_df = pd.DataFrame([[proto, src_pt, dst_pt, flags, tos, label]],
                                 columns=["Proto", "Src Pt", "Dst Pt", "Flags", "Tos", "label"])

        print(result_df)
        print()

        # 데이터 삽입
        insert_packet_data(proto, src_ip, dst_ip, src_pt, dst_pt, flags, tos, label)
        
        time.sleep(1)

def main():
    add_vertical_space(5)
    col1, col2 = st.columns([2,1.5])
    status = st.empty()
    with col1:
        start_button = st.button("감지 시작")
        stop_button = st.button("감지 종료")
    db_connection = pymysql.connect(**db_config)
    db_cursor = db_connection.cursor()
    if start_button:
        st.image("loading.gif")
        status.markdown(f' ## {formatted_datetime} 감지시작')
        interface = "Wi-Fi"
        sniff(iface=interface, prn=packet_callback)

    if stop_button:
        db_cursor.close()
        db_connection.close()
        graph.graph_main()
        st.success(f"{formatted_datetime} 감지가 완료되었습니다. 잠시 후 검사결과로 이동합니다.")
        time.sleep(2)
        switch_page("검사결과")

if __name__ == "__main__":
    main()
