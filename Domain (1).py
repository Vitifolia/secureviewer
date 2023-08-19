import streamlit as st
import pymysql
import requests
import hashlib
from datetime import datetime
import Data
from infobip_api_client.api_client import ApiClient, Configuration
from infobip_api_client.api import send_sms_api
from infobip_api_client.exceptions import ApiException

# MySQL 데이터베이스 연결 함수
def connect_to_db():
    db = pymysql.connect(
        host='project-db-campus.smhrd.com',
        user='secure',
        password='1234',
        database='secure',
        port = 3312
    )
    return db

# 회원 정보 가져오기 함수
def get_member_info(member_id):
    db = connect_to_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)

    query = f"SELECT * FROM tb_user WHERE user_id = '{member_id}'"
    cursor.execute(query)
    member_info = cursor.fetchone()

    db.close()
    return member_info

# 비밀번호 해시 함수
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# 회원 정보 삭제 함수
def delete_member(member_id):
    db = connect_to_db()
    cursor = db.cursor()

    query = f"DELETE FROM tb_user WHERE user_id = '{member_id}'"
    cursor.execute(query)
    db.commit()
    db.close()

# 회원 정보 수정 함수
def update_member_info(member_id, new_pw, new_info, new_tel):
    db = connect_to_db()
    cursor = db.cursor()

    hashed_pw = hash_password(new_pw)  # 비밀번호 해시
    query = f"UPDATE tb_user SET user_pw='{hashed_pw}', user_info='{new_info}', user_tel='{new_tel}' WHERE user_id='{member_id}'"
    cursor.execute(query)
    db.commit()
    db.close()

# 로그인 함수
def login(username, password):
    conn = connect_to_db()
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:  # 수정된 부분
        query = "SELECT * FROM tb_user WHERE user_id=%s AND user_pw=%s"
        hashed_password = hash_password(password)
        cursor.execute(query, (username, hashed_password))
        user = cursor.fetchone()

    conn.close()
    return user

# 로그인 상태 초기화
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False

# 로그인된 사용자 초기화
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None

# 메인 페이지
def main():
    st.title("Secure Viewer")
    
    # 로그인 상태일 때 오른쪽 상단에 로그아웃 버튼 표시
    if st.session_state.is_logged_in:
        logout_button = st.container()
        col1, col2 = logout_button.columns([1, 1])  # 버튼을 오른쪽 상단에 배치하기 위해 컬럼을 사용
        with col2:
            if col2.button("로그아웃"):
                st.session_state.is_logged_in = False
                st.session_state.logged_in_user = None

    menu = st.sidebar.selectbox("메뉴를 선택하세요", ["회원 가입", "로그인", "회원 정보 수정", "회원 탈퇴", "SMS" , "Pay"])

    if menu == "회원 가입":
        signin_page()
    elif menu == "로그인":
        login_page()
    elif menu == "회원 정보 수정":
        update_page()
    elif menu == "회원 탈퇴":
        delete_page()
    elif menu == "SMS":
        sms_page()
    elif menu == "Pay":
        pay_page()

# 로그인 페이지
def login_page():
    st.title("로그인 페이지")

    if not st.session_state.get("is_logged_in"):
        st.session_state.is_logged_in = False
        st.session_state.logged_in_user = None
        st.session_state.logged_in_user_tel = None

    if not st.session_state.is_logged_in:
        username = st.text_input("사용자 이름")
        password = st.text_input("비밀번호", type="password")

        if st.button("로그인"):
            user = login(username, password)
            if user:
                st.session_state.is_logged_in = True
                st.session_state.logged_in_user = username
                st.session_state.logged_in_user_tel = user['user_tel']  # 로그인한 사용자의 전화번호 저장
                st.success(f"{username}님, 로그인에 성공했습니다!")
                password = ""
            else:
                st.error("로그인에 실패했습니다. 아이디 또는 비밀번호를 확인하세요.")


# 회원가입 페이지
def signin_page():
    st.title("회원가입 페이지")
    
    user_id = st.text_input("회원 아이디")
    id_status = Data.id_chk(user_id)
    password = st.text_input("비밀번호", type = "password")
    confirm_password = st.text_input('비밀번호 확인', type = 'password')
    user_info = st.text_input("회사명", placeholder = "ex)스마트인재개발원")
    user_tel = st.text_input("휴대폰 번호", placeholder = "ex)000-0000-0000")
    
    if st.button("회원가입하기"):
        if password != confirm_password:
            st.error('비밀번호가 일치하지 않습니다.')
        if not user_id or not password or not user_info or not user_tel:
            st.error("모든 항목을 입력해주세요.")
        else:
            hashed_password = hash_password(password)
            conn = connect_to_db()
            cursor = conn.cursor()
            try:
                query = "INSERT INTO tb_user VALUES (%s, %s, %s,%s,now(),now(),'n', %s)"
                cursor.execute(query, (user_id, hashed_password, user_info, datetime.now(), user_tel))
                conn.commit()
                st.success("회원가입이 완료되었습니다.")
            except pymysql.Error as e:
                st.error(f"오류가 발생했습니다: {e}")
            finally:
                cursor.close()
                conn.close()

 # 회원 정보 수정 페이지
def update_page():
    st.title("회원 정보 수정")

    if not st.session_state.is_logged_in:
        st.warning("로그인되어 있지 않습니다.")
        return

    member_id = st.session_state.logged_in_user
    member_info = get_member_info(member_id)

    if member_info:
        st.subheader("회원 정보 수정")
        
        new_pw = st.text_input("변경할 비밀번호", type="password", value="")
        new_info = st.text_input("변경할 기업명", value=member_info['user_info'], help = "필수사항")
        new_tel = st.text_input("변경할 전화번호", value=member_info['user_tel'], help = "필수사항")
        
        if st.button("수정"):
            update_member_info(member_id, new_pw, new_info, new_tel)
            st.success("회원 정보가 성공적으로 수정되었습니다.")

# 회원 탈퇴 페이지
def delete_page():
    st.title("회원 탈퇴")

    if not st.session_state.is_logged_in:
        st.warning("로그인되어 있지 않습니다.")
        return

    member_id = st.session_state.logged_in_user
    member_info = get_member_info(member_id)

    if member_info:
        st.warning(f"{member_id}님 탈퇴를 진행하시겠습니까?")

        password = st.text_input("비밀번호를 입력하세요", type="password")

        if password:
            if hash_password(password) == member_info['user_pw']:
                if st.button("탈퇴"):
                    delete_member(member_id)
                    st.success("회원 탈퇴가 완료되었습니다.")
                    st.session_state.is_logged_in = False
                    st.session_state.logged_in_user = None
            else:
                st.warning("비밀번호가 잘못되었습니다.")




# Infobip API 설정
# api_key = '358acf62e00a082529a21efcf777ec20-145dd755-1f9f-4eb1-954c-ea4e46f3336b'
# configuration = Configuration(api_key=api_key)
# apiclient = ApiClient(configuration)

# SMS 전송 함수
def send_sms(user_tel, message):
    api_key = '358acf62e00a082529a21efcf777ec20-145dd755-1f9f-4eb1-954c-ea4e46f3336b'  # 여기에 Infobip API 키를 넣어주세요
    configuration = Configuration(api_key=api_key)
    api_client = ApiClient(configuration)

    sms_request = SmsAdvancedTextualRequest(
        messages=[
            SmsTextualMessage(
                destinations=[
                    SmsDestination(
                        to=user_tel,
                    ),
                ],
                _from='YourApp',
                text=message,
            )
        ]
    )

    try:
        send_sms_api_instance = SendSmsApi(api_client)
        api_response = send_sms_api_instance.send_sms_advanced_textual(sms_advanced_textual_request=sms_request)
        return api_response
    except ApiException as e:
        return str(e)



# Streamlit 애플리케이션 개발
def sms_page():
    st.title('SMS 전송 서비스')

    user_tel = st.text_input("수신자 전화번호", value="", help="수신자의 전화번호를 입력하세요. 예: 1234567890")
    message = st.text_area("메시지 내용", value="", height=150, help="보낼 메시지 내용을 입력하세요.")

    if st.button('SMS 전송'):
        if not user_tel or not message:
            st.warning("수신자 전화번호와 메시지 내용을 입력하세요.")
    else:
        response = send_sms(user_tel, message)
        st.write(f"SMS 전송 결과: {response}")

# PayPal API 토큰 설정
paypal_token = "EJHPe6XZtW5CG1jT9aU3aORuYW5RuVAP3jfvdLl6zKV5snIhMk3v9xl_OcNP-eZKabiztdu9qmIxWtL6"

def create_payment(order_amount):
    headers = {
        "Content-Type": "application/json",
        "Authorization": paypal_token
    }

    data = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": order_amount
                }
            }
        ],
        "payment_source": {
            "paypal": {
                "experience_context": {
                    "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED",
                    "brand_name": "EXAMPLE INC",
                    "locale": "en-US",
                    "landing_page": "LOGIN",
                    "shipping_preference": "SET_PROVIDED_ADDRESS",
                    "user_action": "PAY_NOW",
                    "return_url": "https://example.com/returnUrl",
                    "cancel_url": "https://example.com/cancelUrl"
                }
            }
        }
    }

    response = requests.post('https://api-m.sandbox.paypal.com/v2/checkout/orders', headers=headers, json=data)
    response_data = response.json()
    return response_data

# Streamlit 애플리케이션 개발
def pay_page():
    st.title("PayPal 구독결제")

    if st.session_state.is_logged_in:
        st.write(f"로그인된 사용자: {st.session_state.logged_in_user}")
        order_amount = st.number_input("결제 금액 (USD)", value=30.0, step=10.0)

        if st.button("구독 결제"):
            st.write("결제를 위해 링크를 클릭하세요:")
            payment_url = "https://www.paypal.com/checkoutnow?token=EJHPe6XZtW5CG1jT9aU3aORuYW5RuVAP3jfvdLl6zKV5snIhMk3v9xl_OcNP-eZKabiztdu9qmIxWtL6"
            st.markdown(f"[결제하기]({payment_url})")
    else:
        st.warning("로그인되어 있지 않습니다. 로그인 후에 결제가 가능합니다.")

def get_user_info(user_id, user_pw):
    # 데이터베이스에서 사용자 정보를 가져오는 함수를 작성해야 합니다.
    conn = pymysql.connect(
        host='project-db-campus.smhrd.com',
        user='secure',
        password='1234',
        database='secure',
        port = 3312
    )
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    query = f"SELECT * FROM tb_user WHERE user_id = '{user_id}' AND user_pw = '{user_pw}'"
    cursor.execute(query)
    user_info = cursor.fetchone()

    conn.close()
    return user_info

if __name__ == "__main__":
    main()












CREATE TABLE `tb_user` (
  `user_id` varchar(30) NOT NULL COMMENT '회원 아이디',
  `user_pw` varchar(100) NOT NULL COMMENT '회원 비밀번호',
  `user_info` text NOT NULL COMMENT '회원 기업정보',
  `user_tel` varchar(30) NOT NULL COMMENT '회원 전화번호',
  `created_at` datetime NOT NULL COMMENT '회원 가입일자',
  `svc_at` date NOT NULL COMMENT '회원 서비스구독일',
  `exp_at` date NOT NULL COMMENT '회원 서비스만기일',
  `svc_status` char(1) NOT NULL COMMENT '회원 구독상태',
  PRIMARY KEY (`user_id`)
);



    CREATE TABLE `tb_data` (
  `data_idx` int unsigned NOT NULL AUTO_INCREMENT COMMENT '데이터 식별자',
  `date_first_seen` datetime NOT NULL COMMENT '첫발견시기',
  `proto` varchar(10) NOT NULL COMMENT '프로토콜',
  `src_ip_addr` varchar(30) NOT NULL COMMENT '소스IP주소',
  `dst_ip_addr` varchar(30) NOT NULL COMMENT '타겟IP주소',
  `src_pt` int NOT NULL COMMENT '소스포트',
  `dst_pt` int NOT NULL COMMENT '타겟포트',
  `flags` varchar(20) NOT NULL COMMENT '트래픽플래그',
  `label` varchar(10) DEFAULT NULL COMMENT '탐지 결과',
  `user_id` varchar(30) NOT NULL COMMENT '사용자 아이디',
  PRIMARY KEY (`data_idx`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `tb_user` (`user_id`) ON DELETE CASCADE
);
    
CREATE TABLE `tb_report` (
  `report_idx` int unsigned NOT NULL AUTO_INCREMENT COMMENT '분석 식별자',
  `user_id` varchar(30) NOT NULL COMMENT '사용자 아이디',
  `report_info` text NOT NULL COMMENT '분석 정보',
  `created_at` datetime NOT NULL COMMENT '분석 날짜',
  PRIMARY KEY (`report_idx`),
  KEY `FK_tb_report_user_id_tb_user_user_id` (`user_id`),
  CONSTRAINT `FK_tb_report_user_id_tb_user_user_id` FOREIGN KEY (`user_id`) REFERENCES `tb_user` (`user_id`) ON DELETE CASCADE
);