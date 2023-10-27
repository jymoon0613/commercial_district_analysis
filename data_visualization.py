# 필요한 라이브러리 불러오기
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot
from sklearn import preprocessing
from scipy.stats import pearsonr
# 시각화를 위한 환경 설정
matplotlib.pyplot.rcdefaults()
matplotlib.pyplot.rcParams["font.family"] = 'Haansoft Dotum'
matplotlib.pyplot.rcParams['axes.unicode_minus'] = False

# 총 유동인구 및 성별 유동인구
def visual_fluid_total(df):

    # 대상 연도, 분기 선택
    target_year = 2020 # 연도
    target_quarter = 2 # 분기
    df_2020 = df[df['기준_년_코드'] == target_year]
    df_2020_2 = df_2020[df_2020['기준_분기_코드'] == target_quarter].reset_index(drop = True)

    # 필요한 값 추출
    total = df_2020_2.at[0, '총_유동인구_수']
    men = df_2020_2.at[0, '남성_유동인구_수']
    women = df_2020_2.at[0, '여성_유동인구_수']


    # 그래프 틀 생성
    row_size = 10 # 그래프의 폭 설정
    column_size = 5 # 그래프의 높이 설정
    fig, ax = matplotlib.pyplot.subplots(figsize = (row_size, column_size))

    # 그래프 그리기
    sns.barplot(['총 유동인구', '남성', '여성'], [total, men, women], ax = ax)

    # 그래프 title 설정
    ax.set_title('상권 유동인구 현황 (성별)')

    # 그래프 위에 수치 표시
    for p in ax.patches:
        left, bottom, width, height = p.get_bbox().bounds
        # 수치 표시 위치 설정
        x_axis = left + width / 2 # x축 기준 위치 설정
        y_axis = height * 1.01 # y축 기준 위치 설정
        ax.annotate("약 {:,d} 명".format(int(height)), (x_axis, y_axis), ha = 'center')

# 연령별 유동인구
def visual_fluid_age(df):

    # 대상 연도, 분기 선택
    target_year = 2020 # 연도
    target_quarter = 2 # 분기
    df_2020 = df[df['기준_년_코드'] == target_year]
    df_2020_2 = df[df['기준_분기_코드'] == target_quarter].reset_index(drop = True)

    # 필요한 값 추출
    a10 = df_2020_2.at[0, '연령대_10_유동인구_수']
    a20 = df_2020_2.at[0, '연령대_20_유동인구_수']
    a30 = df_2020_2.at[0, '연령대_30_유동인구_수']
    a40 = df_2020_2.at[0, '연령대_40_유동인구_수']
    a50 = df_2020_2.at[0, '연령대_50_유동인구_수']
    a60 = df_2020_2.at[0, '연령대_60_이상_유동인구_수']

    # 그래프 틀 생성
    row_size = 15 # 그래프의 폭 설정
    column_size = 5 # 그래프의 높이 설정
    fig, ax = matplotlib.pyplot.subplots(figsize = (row_size, column_size))

    # 그래프 그리기
    sns.barplot(['10대 유동인구 수', '20대 유동인구 수',
       '30대 유동인구 수', '40대 유동인구 수', '50대 유동인구 수', '60대 이상 유동인구 수'], [a10, a20, a30, a40, a50, a60], ax = ax)

    # 그래프 title 설정
    ax.set_title('상권 유동인구 현황 (연령대 별)')

    # 그래프 위에 수치 표시
    for p in ax.patches:
        left, bottom, width, height = p.get_bbox().bounds
        # 수치 표시 위치 설정
        x_axis = left + width / 2 # x축 기준 위치 설정
        y_axis = height * 1.01 # y축 기준 위치 설정
        ax.annotate("약 {:,d} 명".format(int(height)), (x_axis, y_axis), ha = 'center')

# 요일별 유동인구
def visual_fluid_day(df) :

    # 대상 연도, 분기 선택
    target_year = 2020 # 연도
    target_quarter = 2 # 분기
    df_2020 = df[df['기준_년_코드'] == target_year]
    df_2020_2 = df[df['기준_분기_코드'] == target_quarter].reset_index(drop = True)

    # 필요한 값 추출
    mon = df_2020_2.at[0, '월요일_유동인구_수']
    tue = df_2020_2.at[0, '화요일_유동인구_수']
    wed = df_2020_2.at[0, '수요일_유동인구_수']
    thu = df_2020_2.at[0, '목요일_유동인구_수']
    fri = df_2020_2.at[0, '금요일_유동인구_수']
    sat = df_2020_2.at[0, '토요일_유동인구_수']
    sun = df_2020_2.at[0, '일요일_유동인구_수']

    # 그래프 틀 생성
    row_size = 15 # 그래프의 폭 설정
    column_size = 5 # 그래프의 높이 설정
    fig, ax = matplotlib.pyplot.subplots(figsize = (row_size, column_size))

    # 그래프 그리기
    sns.barplot(['월요일 유동인구 수', '화요일 유동인구 수',
       '수요일 유동인구 수', '목요일 유동인구 수', '금요일 유동인구 수', '토요일 유동인구 수', '일요일 유동인구 수'], [mon, tue, wed, thu, fri, sat, sun], ax = ax)

    # 그래프 title 설정
    ax.set_title('상권 유동인구 현황 (요일별)')

    # 그래프 위에 수치 표시
    for p in ax.patches:
        left, bottom, width, height = p.get_bbox().bounds
        # 수치 표시 위치 설정
        x_axis = left + width / 2 # x축 기준 위치 설정
        y_axis = height * 1.01 # y축 기준 위치 설정
        ax.annotate("약 {:,d} 명".format(int(height)), (x_axis, y_axis), ha = 'center')

# 시간대별 유동인구
def visual_fluid_time(df) :

    # 대상 연도, 분기 선택
    target_year = 2020 # 연도
    target_quarter = 2 # 분기
    df_2020 = df[df['기준_년_코드'] == target_year]
    df_2020_2 = df[df['기준_분기_코드'] == target_quarter].reset_index(drop = True)

    # 필요한 값 추출
    t1 = df_2020_2.at[0, '시간대_1_유동인구_수']
    t2 = df_2020_2.at[0, '시간대_2_유동인구_수']
    t3 = df_2020_2.at[0, '시간대_3_유동인구_수']
    t4 = df_2020_2.at[0, '시간대_4_유동인구_수']
    t5 = df_2020_2.at[0, '시간대_5_유동인구_수']
    t6 = df_2020_2.at[0, '시간대_6_유동인구_수']

    # 값의 범위를 조절
    t12 = t1 + t2 # 오전 시간대
    t34 = t3 + t4 # 오후 시간대
    t56 = t5 + t6 # 저녁 시간대

    # 그래프 틀 생성
    row_size = 8 # 그래프의 폭 설정
    column_size = 5 # 그래프의 높이 설정
    fig, ax = matplotlib.pyplot.subplots(figsize = (row_size, column_size))

    # 그래프 그리기
    sns.barplot(['오전(00시 - 11시)', '오후(11시 - 17시)', '저녁(17시 - 24시)'], [t12, t34, t56], ax = ax)

    # 그래프 title 설정
    ax.set_title('상권 유동인구 현황 (시간대별)')

    # 그래프 위에 수치 표시
    for p in ax.patches:
        left, bottom, width, height = p.get_bbox().bounds
        # 수치 표시 위치 설정
        x_axis = left + width / 2 # x축 기준 위치 설정
        y_axis = height * 1.01 # y축 기준 위치 설정
        ax.annotate("약 {:,d} 명".format(int(height)), (x_axis, y_axis), ha = 'center')

# 집객시설
def visual_facil(df):
    # 대상 연도, 분기 선택
    target_year = 2020 # 연도
    target_quarter = 2 # 분기
    df_2020 = df[df['기준_년_코드'] == target_year]
    df_2020_2 = df[df['기준_분기_코드'] == target_quarter].reset_index(drop = True)

    # 필요한 column 선택 (집객시설 정보)
    dff = df_2020_2[['관공서_수', '은행_수', '종합병원_수', '일반_병원_수', '약국_수', '유치원_수', '초등학교_수', '중학교_수', '고등학교_수',
                    '대학교_수', '백화점_수', '슈퍼마켓_수', '극장_수', '숙박_시설_수', '공항_수', '철도_역_수','버스_터미널_수',
                    '지하철_역_수', '버스_정거장_수']]


    # 파이 차트 형태로 그리기 위해 값의 표현 방식을 변경
    aa = pd.DataFrame()
    for col in dff.columns: # 추출한 column에 대해서
        if int(dff.at[0, col]) == 0: # 집객시설이 없으면 넘어간다.
            continue
        else:
            n = int(dff.at[0, col])
            word = col.replace('_', ' ') # 집객시설의 종류를 저장
            w_list = []
            w_list.append(word)
            ww = w_list * n
            aa = aa.append(ww) # 집객시설이 얼마나 있는지 저장

    # 그래프 틀 생성
    row_size = 5 # 그래프의 폭 설정
    column_size = 5 # 그래프의 높이 설정
    fig, ax = matplotlib.pyplot.subplots(figsize = (row_size, column_size))
    df = aa.loc[:,0].value_counts() # 정리한 집객시설 수 추출

    # 그래프 위에 수치 표시
    def func(pct, allvals):
        value = pct/100.*np.sum(allvals) # 비율 형태를 갯수 형태로 변환
        return "{:d} 개".format(int(value))

    # 파이 그래프 그리기
    df.plot.pie(title = '상권 집객시설 현황', autopct=lambda pct: func(pct, df), label = '')

# 총 직장인구
def visual_work_total(df) :
    # 총 직장인구 및 성별 (2020-2)

    # 대상 연도, 분기 선택
    target_year = 2020 # 연도
    target_quarter = 2 # 분기
    df_2020 = df[df['기준_년_코드'] == target_year]
    df_2020_2 = df[df['기준_분기_코드'] == target_quarter].reset_index(drop = True)

    # 필요한 값 추출
    total = df_2020_2.at[0, '총_직장_인구_수']
    men = df_2020_2.at[0, '남성_직장_인구_수']
    women = df_2020_2.at[0, '여성_직장_인구_수']

    # 그래프 틀 생성
    row_size = 8 # 그래프의 폭 설정
    column_size = 5 # 그래프의 높이 설정
    fig, ax = matplotlib.pyplot.subplots(figsize = (row_size, column_size))

    # 그래프 그리기
    sns.barplot(['총 직장인구', '남성', '여성'], [total,men,women], ax = ax)

    # 그래프 title 설정
    ax.set_title('상권 직장인구 현황 (성별)')

    # 그래프 위에 수치 표시
    for p in ax.patches:
        left, bottom, width, height = p.get_bbox().bounds
        # 수치 표시 위치 설정
        x_axis = left + width / 2 # x축 기준 위치 설정
        y_axis = height * 1.01 # y축 기준 위치 설정
        ax.annotate("약 {:,d} 명".format(int(height)), (x_axis, y_axis), ha = 'center')

# 연령대별 직장인구
def visual_work_age(df):
    # 연령대별 직장인구 (2020-2)

    # 대상 연도, 분기 선택
    target_year = 2020 # 연도
    target_quarter = 2 # 분기
    df_2020 = df[df['기준_년_코드'] == target_year]
    df_2020_2 = df[df['기준_분기_코드'] == target_quarter].reset_index(drop = True)

    # 필요한 값 추출
    a10 = df_2020_2.at[0, '연령대_10_직장_인구_수']
    a20 = df_2020_2.at[0, '연령대_20_직장_인구_수']
    a30 = df_2020_2.at[0, '연령대_30_직장_인구_수']
    a40 = df_2020_2.at[0, '연령대_40_직장_인구_수']
    a50 = df_2020_2.at[0, '연령대_50_직장_인구_수']
    a60 = df_2020_2.at[0, '연령대_60_이상_직장_인구_수']

    # 그래프 틀 생성
    row_size = 10 # 그래프의 폭 설정
    column_size = 5 # 그래프의 높이 설정
    fig, ax = matplotlib.pyplot.subplots(figsize = (row_size, column_size))

    # 그래프 그리기
    sns.barplot(['10대 직장인구 수', '20대 직장인구 수',
       '30대 직장인구 수', '40대 직장인구 수', '50대 직장인구 수',
       '60대 이상 직장인구 수'], [a10, a20, a30, a40, a50, a60], ax = ax)

    # 그래프 title 설정
    ax.set_title('상권 직장인구 현황 (연령대별)')

    # 그래프 위에 수치 표시
    for p in ax.patches:
        left, bottom, width, height = p.get_bbox().bounds
        # 수치 표시 위치 설정
        x_axis = left + width / 2 # x축 기준 위치 설정
        y_axis = height * 1.01 # y축 기준 위치 설정
        ax.annotate("약 {:,d} 명".format(int(height)), (x_axis, y_axis), ha = 'center')

# 총 상주인구
def visual_live_total(df) :
    # 총 상주인구 및 성별 (2020-2)

    # 대상 연도, 분기 선택
    target_year = 2020 # 연도
    target_quarter = 2 # 분기
    df_2020 = df[df['기준_년_코드'] == target_year]
    df_2020_2 = df[df['기준_분기_코드'] == target_quarter].reset_index(drop = True)

    # 필요한 값 추출
    total = df_2020_2.at[0, '총 상주인구 수']
    men = df_2020_2.at[0, '남성 상주인구 수']
    women = df_2020_2.at[0, '여성 상주인구 수']

    # 그래프 틀 생성
    row_size = 8 # 그래프의 폭 설정
    column_size = 5 # 그래프의 높이 설정
    fig, ax = matplotlib.pyplot.subplots(figsize = (row_size, column_size))

    # 그래프 그리기
    sns.barplot(['총 상주인구', '남성', '여성'], [total, men, women], ax = ax)

    # 그래프 title 설정
    ax.set_title('상권 상주인구 현황 (성별)')

    # 그래프 위에 수치 표시
    for p in ax.patches:
        left, bottom, width, height = p.get_bbox().bounds
        # 수치 표시 위치 설정
        x_axis = left + width / 2 # x축 기준 위치 설정
        y_axis = height * 1.01 # y축 기준 위치 설정
        ax.annotate("약 {:,d} 명".format(int(height)), (x_axis, y_axis), ha = 'center')

# 연령대별 상주인구
def visual_live_age(df) :
    # 연령대별 직장인구 (2020-2)

    # 대상 연도, 분기 선택
    target_year = 2020 # 연도
    target_quarter = 2 # 분기
    df_2020 = df[df['기준_년_코드'] == target_year]
    df_2020_2 = df[df['기준_분기_코드'] == target_quarter].reset_index(drop = True)

    # 필요한 값 추출
    a10 = df_2020_2.at[0, '연령대 10 상주인구 수']
    a20 = df_2020_2.at[0, '연령대 20 상주인구 수']
    a30 = df_2020_2.at[0, '연령대 30 상주인구 수']
    a40 = df_2020_2.at[0, '연령대 40 상주인구 수']
    a50 = df_2020_2.at[0, '연령대 50 상주인구 수']
    a60 = df_2020_2.at[0, '연령대 60 이상 상주인구 수']


    # 그래프 틀 생성
    row_size = 10 # 그래프의 폭 설정
    column_size = 5 # 그래프의 높이 설정
    fig, ax = matplotlib.pyplot.subplots(figsize = (row_size, column_size))

    # 그래프 그리기
    sns.barplot(['10대 상주인구 수', '20대 상주인구 수',
       '30대 상주인구 수', '40대 상주인구 수', '50대 상주인구 수',
       '60대 이상 상주인구 수'], [a10, a20, a30, a40, a50, a60], ax = ax)

    # 그래프 title 설정
    ax.set_title('상권 상주인구 현황 (연령대별)')

    # 그래프 위에 수치 표시
    for p in ax.patches:
        left, bottom, width, height = p.get_bbox().bounds
        # 수치 표시 위치 설정
        x_axis = left + width / 2 # x축 기준 위치 설정
        y_axis = height * 1.01 # y축 기준 위치 설정
        ax.annotate("약 {:,d} 명".format(int(height)), (x_axis, y_axis), ha = 'center')
