import pymysql
import streamlit as st
from infobip_channels.sms.channel import SMSChannel
import Domain
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None
# MySQL 연결 설정
db_config = {
    "host": "project-db-campus.smhrd.com",
    "user": "secure",
    "password": "1234",
    "database": "secure",
    "port": 3312
}

# MySQL에 접속
conn = pymysql.connect(**db_config)
cursor = conn.cursor()

# 회원 정보 조회 쿼리
query = "SELECT user_id, user_tel FROM tb_user;"
cursor.execute(query)
members = cursor.fetchall()

# MySQL 연결 종료
cursor.close()
conn.close()

# Infobip API 설정
# configuration = Configuration(api_key=api_key)
# apiclient = ApiClient(configuration)

# SMS 전송 함수
BASE_URL = "https://6jx85z.api.infobip.com"
API_KEY = "358acf62e00a082529a21efcf777ec20-145dd755-1f9f-4eb1-954c-ea4e46f3336b"

def change_tel():
    user_info = Domain.get_member_info(st.session_state.logged_in_user)
    user_tel = user_info['user_tel']
    tel = user_tel.replace("-", "")
    tel2 = '82'+tel[1:]
    return tel2

def send_sms():
    RECIPIENT = change_tel()
    # Initialize the SMS channel with your credentials.
    channel = SMSChannel.from_auth_params(
        {
            "base_url": BASE_URL,
            "api_key": API_KEY,
        }
    )
    
    # Send a message with the desired fields.
    response = channel.send_sms_message(
        {
            "messages": [
                {
                    "destinations": [{"to": RECIPIENT}],
                    "text": "Secure Viewer 에서 알려드립니다. 네트워크 침입이 감지 되었으니, 신속하게 조치 하시길 바랍니다.",
                }
            ]
        }
    )
    return response
# Streamlit 애플리케이션 개발
def sms_page():
    st.title('Secure Viewer 침입 알림 서비스')

    if st.session_state.is_logged_in:
        user_info = get_member_info(st.session_state.logged_in_user)
        user_tel = user_info['user_tel']

        message = "Secure Viewer 에서 알려드립니다. 네트워크 침입이 감지 되었으니, 신속하게 조치 하시길 바랍니다."

        if st.button('SMS 전송'):
            response = send_sms()
            st.write(f"SMS 전송 결과 : 수신번호:{user_tel}, 내용: {message}")
    else:
        st.warning("로그인되어 있지 않습니다. 로그인 후에 SMS를 전송할 수 있습니다.")