import streamlit as st
import pymysql
import Domain
import datetime
from streamlit_extras.colored_header import colored_header




# cidds 정보 가져오기 함수
def get_data_info(member_id):
    db = Domain.connect_to_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)

    query = f"SELECT * FROM tb_data WHERE user_id = '{member_id}'"
    cursor.execute(query)
    cidds_info = cursor.fetchone()

    db.close()
    return cidds_info

get_data_info()



