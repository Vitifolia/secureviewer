import pandas as pd
import numpy as np
import pymysql.cursors
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Tab, Pie
import streamlit as st

ymn = [] 
yma = []
ymv = []
yhn = []
yha = []
yhv = []
ydn = []
yda = []
ydv = []
xf = []  # Flags
yf = []  # 비율    
zf  = [] # 비율이 0인 index 리스트

def graph_main():
    user_id = f"{st.session_state.logged_in_user}"

    connection = pymysql.connect(
        host='project-db-campus.smhrd.com', port=3312, user='secure', password='1234', db='secure', charset='utf8', cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    sql = f"SELECT * FROM secure.tb_data WHERE user_id = '{user_id}'"
    cursor.execute(sql)
    result = cursor.fetchall()

    W0 = pd.DataFrame(result)
    W1 = pd.DataFrame(result)
    W2 = pd.DataFrame(result)
    
    connection.close()

    # date_first_seen 그룹화(분)
    W0['date_first_seen'] = W0['date_first_seen'].apply(lambda x: pd.to_datetime(x))
    W0['date_first_seen'] = W0['date_first_seen'].dt.strftime("%Y-%m-%d %H:%M")

    # date_first_seen 그룹화(시간)
    W1['date_first_seen'] = W1['date_first_seen'].apply(lambda x: pd.to_datetime(x))
    W1['date_first_seen'] = W1['date_first_seen'].dt.strftime("%Y-%m-%d %H")

    # date_first_seen 그룹화(날짜)
    W2['date_first_seen'] = W2['date_first_seen'].apply(lambda x: pd.to_datetime(x))
    W2['date_first_seen'] = W2['date_first_seen'].dt.strftime("%Y-%m-%d")

    # 날짜별 접근 목적
    xm = list(W0["date_first_seen"].unique())
    xh = list(W1["date_first_seen"].unique())
    xd = list(W2["date_first_seen"].unique())

    
    W1_nor = W1['label'].str.contains('normal')
    W1_att = W1['label'].str.contains('attacker')
    W1_vic = W1['label'].str.contains('victim')
    
    for i in xm:
        ymn.append(len(W0[W0['date_first_seen'].str.contains(f'{i}') & W1_nor]))
        yma.append(len(W0[W0['date_first_seen'].str.contains(f'{i}') & W1_att]))
        ymv.append(len(W0[W0['date_first_seen'].str.contains(f'{i}') & W1_vic]))

    for i in xh:
        yhn.append(len(W1[W1['date_first_seen'].str.contains(f'{i}') & W1_nor]))
        yha.append(len(W1[W1['date_first_seen'].str.contains(f'{i}') & W1_att]))
        yhv.append(len(W1[W1['date_first_seen'].str.contains(f'{i}') & W1_vic]))
        
    for i in xd:
        ydn.append(len(W2[W2['date_first_seen'].str.contains(f'{i}') & W1_nor]))
        yda.append(len(W2[W2['date_first_seen'].str.contains(f'{i}') & W1_att]))
        ydv.append(len(W2[W2['date_first_seen'].str.contains(f'{i}') & W1_vic]))

    # 접근 목적 비율
    class_n = len(W1['label'])
    normal_n = len(W1[W1_nor])
    attacker_n = len(W1[W1_att])
    victim_n = len(W1[W1_vic])

    a = round(normal_n / class_n * 100)
    b = round(attacker_n / class_n * 100)
    c = round(victim_n / class_n * 100)

    # 총 Flags
    flags = W1['flags'].unique()
    flags[0]
    lenf = len(list(flags)) -1

    Fl = len(W1['flags'])

    # 비율
    Fl = len(W1['flags'])
    for i in range(lenf):
        globals()["Fl_{}".format(i)] = len(W1[W1['flags'] == (flags[i])])

    for i in range(lenf):
        globals()["f{}".format(i)] = round(globals()["Fl_{}".format(i)]/ Fl* 100)

    xf = []
    yf = []
    for i in range(lenf):
        xf.append(flags[i])
        yf.append(globals()["f{}".format(i)])

    for i in range(lenf):
        if yf[i] == 0:
            zf.append(i)

    for i in sorted(zf, reverse=True):
        del xf[i]
        del yf[i]

# 악성 접근 빈도 Tab
    z1 = (
        Bar(init_opts=opts.InitOpts(width="800px", height="500px"))
        .add_xaxis(xm)
        .add_yaxis("정상", ymn, color = '#4FBDBA')
        .add_yaxis("공격시도", yma, color = '#E96479')
        .add_yaxis("피해", ymv, color = '#072227')
        .set_global_opts(
            title_opts = opts.TitleOpts(title = "분별 악성 접근 빈도-Bar"),
            xaxis_opts = opts.AxisOpts(name = "분"),  # X축 이름
            yaxis_opts = opts.AxisOpts(name = "횟수",
                axislabel_opts = opts.LabelOpts(formatter="{value} (회)")), # Y축 눈금 포맷            
            datazoom_opts = [opts.DataZoomOpts(), opts.DataZoomOpts(type_ = "inside")]       
        )
    )

    z2 = (
        Line(init_opts=opts.InitOpts(width="800px", height="500px"))
        .add_xaxis(xm)
        .add_yaxis("정상", ymn, color = '#4FBDBA', markline_opts = opts.MarkLineOpts(data=[opts.MarkLineItem(type_= 'average', name='평균')]))
        .add_yaxis("공격시도", yma, color = '#E96479', markline_opts = opts.MarkLineOpts(data=[opts.MarkLineItem(type_= 'average', name='평균')]))
        .add_yaxis("피해", ymv, color = '#072227', markline_opts = opts.MarkLineOpts(data=[opts.MarkLineItem(type_= 'average', name='평균')]))
        .set_global_opts(
            title_opts = opts.TitleOpts(title = "분별 악성 접근 빈도-Line"),
            xaxis_opts = opts.AxisOpts(name = "분"),  # X축 이름
            yaxis_opts = opts.AxisOpts(name = "횟수",
                axislabel_opts = opts.LabelOpts(formatter="{value} (회)")), # Y축 눈금 포맷            
            datazoom_opts = [opts.DataZoomOpts(), opts.DataZoomOpts(type_ = "inside")]
        )
    )

    z3 = (
        Line(init_opts=opts.InitOpts(width="800px", height="500px"))
        .add_xaxis(xh)
        .add_yaxis("정상", yhn, color = '#4FBDBA', markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max")]))
        .add_yaxis("공격시도", yha, color = '#E96479', markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max")]))
        .add_yaxis("피해", yhv, color = '#072227', markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max")]))
        .set_global_opts(
            title_opts = opts.TitleOpts(title = "시간별 악성 접근 빈도-Line"),
            xaxis_opts = opts.AxisOpts(name = "시간"),  # X축 이름
            yaxis_opts = opts.AxisOpts(name = "횟수",
                axislabel_opts = opts.LabelOpts(formatter="{value} (회)")), # Y축 눈금 포맷            
            datazoom_opts = [opts.DataZoomOpts(), opts.DataZoomOpts(type_ = "inside")]
        )
    )

    z4 = (
        Bar(init_opts=opts.InitOpts(width="800px", height="500px"))
        .add_xaxis(xh)
        .add_yaxis("정상", yhn, color = '#4FBDBA')
        .add_yaxis("공격시도", yha, color = '#E96479')
        .add_yaxis("피해", yhv, color = '#072227')
        .set_global_opts(
            title_opts = opts.TitleOpts(title = "시간별 악성 접근 빈도-Bar"),
            xaxis_opts = opts.AxisOpts(name = "시간"),  # X축 이름
            yaxis_opts = opts.AxisOpts(name = "횟수",
                axislabel_opts = opts.LabelOpts(formatter="{value} (회)")), # Y축 눈금 포맷            
            datazoom_opts = [opts.DataZoomOpts(), opts.DataZoomOpts(type_ = "inside")]       
        )
    )

    z5 = (
        Line(init_opts=opts.InitOpts(width="800px", height="500px"))
        .add_xaxis(xd)
        .add_yaxis("정상", ydn, color = '#4FBDBA', markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_= "max")]))
        .add_yaxis("공격시도", yda, color = '#E96479', markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_= "max")]))
        .add_yaxis("피해", ydv, color = '#072227', markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_= "max")]))
        .set_global_opts(
            title_opts = opts.TitleOpts(title = "날짜별 악성 접근 빈도-Line"),
            xaxis_opts = opts.AxisOpts(name = "날짜"),  # X축 이름
            yaxis_opts = opts.AxisOpts(name = "횟수",
                axislabel_opts = opts.LabelOpts(formatter="{value} (회)")), # Y축 눈금 포맷            
            datazoom_opts = [opts.DataZoomOpts(), opts.DataZoomOpts(type_ = "inside")]
        )
    )

    z6 = (
        Bar(init_opts=opts.InitOpts(width="800px", height="500px"))
        .add_xaxis(xd)
        .add_yaxis("정상", ydn, color = '#4FBDBA')
        .add_yaxis("공격시도", yda, color = '#E96479')
        .add_yaxis("피해", ydv, color = '#072227')
        .set_global_opts(
            title_opts = opts.TitleOpts(title = "날짜별 악성 접근 빈도-Bar"),
            xaxis_opts = opts.AxisOpts(name = "날짜"),  # X축 이름
            yaxis_opts = opts.AxisOpts(name = "횟수",
                axislabel_opts = opts.LabelOpts(formatter="{value} (회)")), # Y축 눈금 포맷            
            datazoom_opts = [opts.DataZoomOpts(), opts.DataZoomOpts(type_ = "inside")]       
        )
    )
    tab = Tab()
    tab.add(z2, "분별 선형 그래프 ")
    tab.add(z1, "분별 바 그래프")
    tab.add(z3, "시간별 선형 그래프")
    tab.add(z4, "시간별 바 그래프")
    tab.add(z5, "날짜별 선형 그래프")
    tab.add(z6, "날짜별 바 그래프")
    tab.render("graph1.html")

    # 접근 목적
    xp = ["정상", "공격시도", "피해"]

    # 비율
    yp = [a, b, c]

    # 총 접근 목적 Pie
    z = (
        Pie(init_opts=opts.InitOpts(width="700px", height="500px"),)
        .add(
            "",
            [list(i) for i in zip(xp, yp)],
            radius = ["35%", "60%"],
            center = ["35%","50%"]
        )
        .set_colors(['#4FBDBA', '#E96479', '#072227'])
        .set_global_opts(title_opts = opts.TitleOpts(title = "총 접근 목적(%)"),
                        legend_opts=opts.LegendOpts(orient="vertical", pos_top="80%", pos_left="5%"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        .render("graph2.html")
    )

    # 총 Flags 분류 Pie-Rose
    z = (
        Pie(init_opts=opts.InitOpts(width="700px", height="500px"))
        .add(
            "",
            [list(i) for i in zip(xf, yf)],
            radius = ["20%", "45%"],
            center = ["20%", "50%"],
            rosetype ="radius",
            label_opts = opts.LabelOpts(is_show = False),
        )
        .add(
            "",
            [list(i) for i in zip(xf, yf)],
            radius = ["20%", "45%"],
            center = ["70%", "50%"],
            rosetype = "area",
        )
        .set_colors(['#072227', '#778899', '#4FBDBA', '#E96479', '#4FBDBA', '#7A5DC1', '#444693'])
        .set_global_opts(title_opts = opts.TitleOpts(title = "총 Flags(%)"))
        .render("graph3.html")
    )
