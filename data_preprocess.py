# 필요한 라이브러리 불러오기
import warnings
warnings.filterwarnings(action = 'ignore')
import time
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from sklearn import preprocessing
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import pandas as pd
import seaborn as sns
# 판다스 환경 설정
pd.set_option('display.float_format', lambda x: '%.2f' % x)

# 시계열 Input Data 생성 함수
def four_season_data_in(all_data_in, y_1, q_1, y_2, q_2, y_3, q_3, y_4, q_4):

    # 1년치(4분기) 데이터를 row에서 column으로 변환함.
    # 예를 들어, 변환 후에 4분기 전 데이터는 '변수명 - 4'로 표현됨
    _test = pd.merge(all_data_in.groupby(['기준_년_코드','기준_분기_코드']).get_group((y_1,q_1)).drop(['기준_년_코드','기준_분기_코드'], axis=1),
                     all_data_in.groupby(['기준_년_코드','기준_분기_코드']).get_group((y_2,q_2)).drop(['기준_년_코드','기준_분기_코드'], axis=1), how='left',on=['서비스_업종_코드'],suffixes=('-4', '-3'))
    _test = pd.merge(_test,all_data_in.groupby(['기준_년_코드','기준_분기_코드']).get_group((y_3,q_3)).drop(['기준_년_코드','기준_분기_코드'], axis=1), how='left',on=['서비스_업종_코드'],suffixes=('', '-2'))
    _test = pd.merge(_test,all_data_in.groupby(['기준_년_코드','기준_분기_코드']).get_group((y_4,q_4)).drop(['기준_년_코드','기준_분기_코드'], axis=1), how='left',on=['서비스_업종_코드'],suffixes=('', '-1'))
    return _test

# 시계열 Output Data 생성 함수
def four_season_data_out(all_data_c, y_5, q_5):

    _test = pd.DataFrame(all_data_c.groupby(['기준_년_코드','기준_분기_코드']).get_group((y_5, q_5))['폐업_률'])

    return _test

# 폐업률 모델 전처리 함수
def data_preprocessing_fail(total, market_code, service_code):
    # 상권 선택
    select_market = total[total['상권_코드'] == market_code]
    # 업종 선택
    select_service = select_market[select_market['서비스_업종_코드'] == service_code]

    # 시계열 데이터 준비
    list_season = []
    start_year = 2015 # 시작 연도
    end_year = 2020 # 끝 연도
    start_quarter = 1 # 시작 분기
    end_quarter = 4 # 끝 분기

    # 시계열 index를 리스트로 생성
    for i in range(start_year, end_year):
        for j in range(start_quarter, end_quarter + 1):
            _list = []
            _list.append(i)
            _list.append(j)
            list_season.append(_list)

    for i in range(end_year, end_year + 1):

        for j in range(start_quarter, end_quarter - 1):
            _list = []
            _list.append(i)
            _list.append(j)
            list_season.append(_list)

    # 시계열 x,y 데이터 생성
    for i in range(0,18):
        globals()["x_predict_{}_{}".format(list_season[i+4][0], list_season[i+4][1])] = four_season_data_in(select_service.drop(['폐업_률', '상권_코드', '상권_코드_명', '서비스_업종_코드_명'], axis = 1),
                                                                                                                  list_season[i][0],list_season[i][1],
                                                                                                                  list_season[i+1][0],list_season[i+1][1],
                                                                                                                  list_season[i+2][0],list_season[i+2][1],
                                                                                                                  list_season[i+3][0],list_season[i+3][1]
                                                                                                              )
        globals()["y_predict_{}_{}".format(list_season[i+4][0], list_season[i+4][1])] = four_season_data_out(select_service,
                                                                                                                 list_season[i+4][0],list_season[i+4][1])

    # DataFrame을 vertically concat 하기 위해 append 함
    x_in = pd.DataFrame(columns = x_predict_2020_2.columns)
    x_out = pd.DataFrame(columns = y_predict_2020_2.columns)
    for i in range(0, 18):
        x_in = x_in.append(globals()["x_predict_{}_{}".format(list_season[i+4][0], list_season[i+4][1])], ignore_index=False)
        x_out = x_out.append(globals()["y_predict_{}_{}".format(list_season[i+4][0], list_season[i+4][1])], ignore_index=False)

    # 불필요한 column 제거
    x_in = x_in.drop(['서비스_업종_코드'], axis=1)
    x_in = x_in.reset_index(drop=True, inplace=False)

    # 불필요한 column 제거
    x_out = x_out.reset_index(drop = True)
    x_out['폐업_률'] = pd.to_numeric(x_out['폐업_률'])

    # 2020_3분기 폐업률 예측을 위한 데이터 생성
    x_predict_2020_3 = four_season_data_in(select_service.drop(['폐업_률', '상권_코드', '상권_코드_명', '서비스_업종_코드_명'], axis = 1),2019,3,2019,4,2020,1,2020,2)
    x_predict_2020_3 = x_predict_2020_3.drop('서비스_업종_코드', axis = 1)

    # 시계열 변환 x,y 데이터 및 2020-3분기 예측용 데이터 반환
    return (x_in, x_out, x_predict_2020_3)

# 생존율 모델 전처리 함수
def data_preprocessing_survive(total, market_code, service_code, select):
    # 상권 선택
    select_market = total[total['상권_코드'] == market_code]
    # 업종 선택
    select_service = select_market[select_market['서비스_업종_코드'] == service_code].reset_index(drop = True)

    # 필요한 column 추출
    if select == 'gender':
        select_service = select_service[['기준_년_코드', '기준_분기_코드', '서비스_업종_코드', '남성_매출_비율', '여성_매출_비율', '폐업_률']]
    elif select == 'age':
        select_service  = select_service[['기준_년_코드', '기준_분기_코드', '서비스_업종_코드', '연령대_10_매출_비율', '연령대_20_매출_비율', '연령대_30_매출_비율',
       '연령대_40_매출_비율', '연령대_50_매출_비율', '연령대_60_이상_매출_비율', '폐업_률']]
    elif select == 'day':
        select_service = select_service[['기준_년_코드', '기준_분기_코드', '서비스_업종_코드', '월요일_매출_비율', '화요일_매출_비율',
       '수요일_매출_비율', '목요일_매출_비율', '금요일_매출_비율', '토요일_매출_비율', '일요일_매출_비율', '폐업_률']]
    else:
        select_service = select_service[['기준_년_코드', '기준_분기_코드', '서비스_업종_코드','시간대_00~06_매출_비율', '시간대_06~11_매출_비율', '시간대_11~14_매출_비율',
       '시간대_14~17_매출_비율', '시간대_17~21_매출_비율', '시간대_21~24_매출_비율', '폐업_률']]

    # 폐업률 추출
    y = select_service[['기준_년_코드', '기준_분기_코드','서비스_업종_코드', '폐업_률']].reset_index(drop = True)
    y = y.drop(0).reset_index(drop = True)
    y_new = pd.DataFrame(columns = y.columns)

    # 폐업률 데이터를 헷갈리지 않도록 직전 분기로 변경해줌
    start_quarter = 1 # 시작 분기
    end_quarter = 4 # 끝 분기
    for i in range(len(y)):
        row = y.iloc[i]
        if row['기준_분기_코드'] != start_quarter: # 1분기가 아니면
            row['기준_분기_코드'] -= start_quarter # 분기를 하나씩 뒤로 보내고
            y_new = y_new.append(row)
        else:
            row['기준_년_코드'] -= start_quarter # 1분기인 경우
            row['기준_분기_코드'] = end_quarter # 이전 연도의 4분기로 변경
            y_new = y_new.append(row)

    # 2020-3분기 예측에 사용되는 'X_predict' 데이터 추출
    target_index = 21 #추출할 index 설정 (2019년 2분기 ~ 2020년 2분기 데이터)
    x_predict = pd.DataFrame(columns = select_market.columns)
    x_predict = x_predict.append(select_service.iloc[target_index, :])
    x_predict = x_predict.drop(['기준_년_코드', '기준_분기_코드', '서비스_업종_코드', '폐업_률'], axis = 1)

    # 인풋 데이터 추출
    x = select_service.drop('폐업_률', axis = 1).drop(target_index).reset_index(drop = True)

    # x와 y를 하나로 merge
    xy_train = pd.merge(x, y_new, how = 'left', on = ['기준_년_코드', '기준_분기_코드', '서비스_업종_코드'])

    # 불필요한 column 삭제
    xy_train_new = xy_train.drop(['기준_년_코드', '기준_분기_코드', '서비스_업종_코드'], axis = 1)

    # Input 데이터와, Output 데이터 분리 할당
    x_in = xy_train_new.drop('폐업_률', axis = 1)
    x_out = xy_train_new['폐업_률']

    # 폐업률을 생존율로 변환
    total = 100 # 폐업률 + 생존율
    x_out = total - x_out # 생존율 = 100 - 폐업률

    # 시계열 변환 x,y 데이터 및 2020-3분기 예측용 데이터 반환
    return x_in, x_out, x_predict
