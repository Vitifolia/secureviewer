import streamlit as st
import pymysql
import hashlib
from datetime import datetime, timedelta, date
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from infobip_channels.sms.channel import SMSChannel
from dateutil.relativedelta import relativedelta





# MySQL 데이터베이스 연결 함수
def connect_to_db():
    db = pymysql.connect(
        host='project-db-campus.smhrd.com',
        user='secure',
        password='1234',
        database='secure',
        port=3312
    )
    return db

# 아이디 확인
def id_chk(user_id):
    db = connect_to_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)

    # 쿼리 실행
    cursor.execute('SELECT user_id FROM tb_user')

    # 결과 조회
    results = cursor.fetchall()

    # 결과 출력
    cnt = 0
    if user_id == '':
        id_status = ''
    else:
        for user in results:
            if user['user_id'] == f'{user_id}':
                cnt += 1
        if cnt == 1:
            id_status = st.error('사용 중인 아이디 입니다.') 
        else:
            id_status = st.success('사용 가능한 아이디 입니다.')

    cursor.close()
    db.close()

    return id_status


    


# 회원 정보 가져오기 함수
def get_member_info(member_id):
    db = connect_to_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)

    query = f"SELECT * FROM tb_user WHERE user_id = '{member_id}'"
    cursor.execute(query)
    member_info = cursor.fetchone()
    cursor.close()
    db.close()
    return member_info


# data 정보 가져오기 함수
def get_data_info(member_id):
    db = connect_to_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)

    query = f"SELECT date_first_seen, label FROM tb_data WHERE user_id = '{member_id}' and label = 'attacker'"
    cursor.execute(query)
    data_info = cursor.fetchall()
    cursor.close()
    db.close()
    return data_info

# 오늘 공격받은 data 정보 최신순 10개 가져오기 함수
def get_all_data_info(member_id):
    db = connect_to_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)

    query = f"SELECT proto, flags, tos, label FROM tb_data WHERE user_id = '{member_id}' and DATE(date_first_seen) = CURDATE() ORDER BY date_first_seen DESC LIMIT 10"
    cursor.execute(query)
    data_info = cursor.fetchall()
    cursor.close()
    db.close()
    return data_info

# 공격 data 정보 가져오기 함수
def get_attack_data_info(member_id):
    db = connect_to_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)

    query = f"SELECT count(label) FROM tb_data WHERE user_id = '{member_id}' and label = 'attacker' and DATE(date_first_seen) = CURDATE()"
    cursor.execute(query)
    attack_data_info = cursor.fetchone()
    cursor.close()
    db.close()
    return attack_data_info


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
    cursor.close()
    db.close()

# 회원 정보 수정 함수
def update_member_info(member_id, new_pw, new_info, new_tel):
    db = connect_to_db()
    cursor = db.cursor()

    hashed_pw = hash_password(new_pw)  # 비밀번호 해시
    query = f"UPDATE tb_user SET user_pw='{hashed_pw}', user_info='{new_info}', user_tel='{new_tel}' WHERE user_id='{member_id}'"
    cursor.execute(query)
    db.commit()
    cursor.close()
    db.close()

# 로그인 함수
def login(username, password):
    conn = connect_to_db()
    with conn.cursor() as cursor:
        query = "SELECT * FROM tb_user WHERE user_id=%s AND user_pw=%s"
        hashed_password = hash_password(password)
        cursor.execute(query, (username, hashed_password))
        user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user
# 로그인 상태 초기화
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False

# 로그인된 사용자 초기화
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None

# 로그인 페이지
def login_page():
    # st.title("로그인 페이지")

    if not st.session_state.get("is_logged_in"):
        st.session_state.is_logged_in = False
        st.session_state.logged_in_user = None
    
    if not st.session_state.is_logged_in:
        username = st.text_input("아이디")
        password = st.text_input("비밀번호", type="password")
        col1, col2 = st.columns([6,1])
        col1.button("로그인", key="login")
        col2.button("회원가입", key="sign")
        if st.session_state.login == True:
            user = login(username, password)
            if user:
                st.session_state.is_logged_in = True
                st.session_state.logged_in_user = username
                password = ""
                sub_chk(st.session_state.get("logged_in_user"))
            else:
                st.error("로그인에 실패했습니다. 사용자 이름 또는 비밀번호를 확인하세요.")
        elif st.session_state.sign == True:
            switch_page("회원가입")


# 구독(1달) 하기
def sub_month(member_id):
    db = connect_to_db()
    cursor = db.cursor()
    # 구독 날짜 가져오기
    query = f"SELECT exp_at FROM tb_user WHERE user_id = '{member_id}'"
    cursor.execute(query)
    exp_at = cursor.fetchone()[0]

    one_month_later = exp_at + relativedelta(months=1)

    # 구독 확인 상태를 MySQL에 저장
    update_query = f"UPDATE tb_user SET exp_at = '{one_month_later}' WHERE user_id = '{member_id}'"
    cursor.execute(update_query)
    db.commit()
    cursor.close()
    # 연결 종료
    db.close()


# 구독(1년) 하기
def sub_year(member_id):
    db = connect_to_db()
    cursor = db.cursor()
    # 구독 날짜 가져오기
    query = f"SELECT exp_at FROM tb_user WHERE user_id = {member_id}"
    cursor.execute(query)
    exp_at = cursor.fetchone()[0]

    one_year_later = exp_at + relativedelta(years=1)

    # 구독 확인 상태를 MySQL에 저장
    update_query = f"UPDATE tb_user SET exp_at = '{one_year_later}' WHERE user_id = {member_id}"
    cursor.execute(update_query)
    db.commit()
    cursor.close()
    # 연결 종료
    db.close()

# 구독확인
def sub_chk(member_id):
    db = connect_to_db()
    cursor = db.cursor()
    # 구독 날짜 가져오기
    query = f"SELECT exp_at FROM tb_user WHERE user_id = '{member_id}'"
    cursor.execute(query)
    exp_at = cursor.fetchone()[0]
    # 구독 확인 상태 설정
    if exp_at >= date.today():
        svc_status = 'Y'
    else:
        svc_status = 'N'
    st.session_state.svc_status = svc_status
    # 구독 확인 상태를 MySQL에 저장
    update_query = f"UPDATE tb_user SET svc_status = '{svc_status}' WHERE user_id = '{member_id}'"
    cursor.execute(update_query)
    db.commit()
    cursor.close()
    # 연결 종료
    db.close()


# 회원가입 페이지
def signin_page():
    # st.title("회원가입 페이지")
    
    user_id = st.text_input("회원 아이디")
    id_chk(user_id)
    password = st.text_input("비밀번호", type="password")
    confirm_password = st.text_input('비밀번호 확인', type='password')
    user_info = st.text_input("회사명",placeholder= "ex)스마트인재개발원")
    user_tel = st.text_input("전화번호",placeholder="전화번호를 입력하세요. ex)000-0000-0000")
    st.session_state.status = None
    one_week_later = datetime.now() + timedelta(weeks=1)

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
                query = "INSERT INTO tb_user VALUES (%s, %s, %s, %s, %s, now(), %s,'n')"
                cursor.execute(query, (user_id, hashed_password, user_info, user_tel, datetime.now(), one_week_later))
                conn.commit()
                st.session_state.status = 'success'
            except pymysql.Error as e:
                st.session_state.status = 'error'
                st.error("양식에 맞춰 작성해주세요")
            finally:
                cursor.close()
                conn.close()

 # 회원 정보 수정 페이지
def update_page():

    if not st.session_state.is_logged_in:
        st.warning("로그인되어 있지 않습니다.")
        return

    member_id = st.session_state.logged_in_user
    member_info = get_member_info(member_id)

    if member_info:
 
        current_pw = st.text_input("현재 비밀번호", type="password" , placeholder = "현재 비밀번호를 입력하지 않을 시 수정 불가.")
        new_pw = st.text_input("변경할 비밀번호", type="password", value=f"{current_pw}")
        if new_pw == "":
            st.error("비밀번호를 입력해주세요")
            
        new_info = st.text_input("변경할 기업명", value=member_info['user_info'])
        new_tel = st.text_input("변경할 전화번호", value=member_info['user_tel'])

        # 현재 비밀번호와 새 비밀번호가 동일한 경우 수정 안되도록 함
        is_current_pw_same_as_new_pw = hash_password(current_pw) == hash_password(new_pw)

        update_button_disabled = current_pw == "" or new_pw == ""
        if st.button("수정", disabled=update_button_disabled):
            if current_pw and hash_password(current_pw) != member_info['user_pw']:
                st.warning("현재 비밀번호가 틀렸습니다.")
            elif is_current_pw_same_as_new_pw:
                st.warning("새 비밀번호가 현재 비밀번호와 동일합니다.")
            else:
                update_member_info(member_id, new_pw, new_info, new_tel)
                st.session_state.status = 'success'


# 회원 탈퇴 페이지
def delete_page():

    if not st.session_state.is_logged_in:
        st.warning("로그인되어 있지 않습니다.")
        return

    member_id = st.session_state.logged_in_user
    member_info = get_member_info(member_id)

    if member_info:
        st.warning(f"{member_id}님 회원탈퇴를 진행하시겠습니까?")

        password = st.text_input("비밀번호를 입력하세요", type="password")

        if password:
            if hash_password(password) == member_info['user_pw']:
                if st.button("탈퇴"):
                    delete_member(member_id)
                    st.session_state.is_logged_in = False
                    st.session_state.logged_in_user = None
                    st.session_state.status = 'success'
            else:
                st.warning("비밀번호가 잘못되었습니다.")





def change_tel():
    member_info = get_member_info(st.session_state.logged_in_user)
    tel = member_info['user_tel']
    tel1 = tel.replace("-", "")
    tel2 = '+82'+tel1[1:]
    return tel2

def send_sms():
    # SMS 전송 함수
    BASE_URL = "https://6jx85z.api.infobip.com"
    API_KEY = "358acf62e00a082529a21efcf777ec20-145dd755-1f9f-4eb1-954c-ea4e46f3336b"   
    
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

        
        send_sms()
        st.write(f"SMS 전송 결과 : 수신번호:{user_tel}, 내용: {message}")
    else:
        st.warning("로그인되어 있지 않습니다. 로그인 후에 SMS를 전송할 수 있습니다.")