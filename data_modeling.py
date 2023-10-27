# 필요한 라이브러리 불러오기
import warnings
warnings.filterwarnings(action='ignore')
import time
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder
from scipy.stats import pearsonr
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot

# 시각화를 위한 환경 설정
matplotlib.pyplot.rcdefaults()
matplotlib.pyplot.rcParams["font.family"] = 'Haansoft Dotum'
matplotlib.pyplot.rcParams['axes.unicode_minus'] = False


# 모델링 자동화 코드
def modeling(x_in, x_out):

    start = time.time()  # 시작 시간 저장

    # 학습 데이터 및 검증 데이터 생성
    test_size = 0.2 # 학습 데이터 비율
    random_state = 42 # 동일한 결과를 얻기 위해 seed 설정
    X_train, X_test, y_train, y_test= train_test_split(x_in, x_out, test_size = test_size, random_state = random_state)

####### xgboost 모델 생성 및 학습 #######

    # 모델의 Hyperparameters 설정
    n_estimators = 3000
    learning_rate = 0.001
    max_depth = 12
    n_jobs = -1
    subsample = 0.75
    reg_lambda = 1
    colsample_bytree = 1
    gamma = 0

    # 모델 생성
    model = XGBRegressor(booster = "gbtree", objective ='reg:squarederror', n_estimators = n_estimators, learning_rate = learning_rate ,
                      max_depth = max_depth, n_jobs = n_jobs, subsample = subsample, reg_lambda = reg_lambda,
                      colsample_bytree = colsample_bytree, gamma = gamma)

    eval_set = [(X_test, y_test)] # 평가 항목 설정

    model.fit(X_train, y_train, eval_set = eval_set, verbose = True) # 모델 학습
    pred_y = model.predict(X_test)

    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간

    return model # 생성된 모델 반환

# 모델 성능 시각화 코드
def visual_model(model, x_in, x_out):

    # 실제값 추출
    x_out_list = []
    for i in range(len(x_out)):
        n = x_out.values[i][0] # 항상 첫 번째 값만을 필요로 한다.
        x_out_list.append(n)

    # 그래프 틀 생
    row_size = 15 # 그래프의 폭 설정
    column_size = 5 # 그래프의 높이 설정
    fig, ax =matplotlib.pyplot.subplots(figsize=(row_size, column_size)) # 그래프 틀을 생성

    # 그래프 그리기
    line_width = 2 # 선의 두께 설정
    alpha = 0.7 # 선의 투명도 설정
    rng = pd.date_range('1/1/2016', periods=18, freq='Q') # x축 값으로 사용할 시계열 index 생성
    sns.lineplot(x = rng, y = model.predict(x_in), alpha = alpha, linewidth = line_width, ax = ax, label = '모델 예측값') # 파란색 : 예측값
    sns.lineplot(x = rng, y = x_out_list, alpha = alpha, linewidth = line_width, ax = ax, label = '실제값') # 주황색 : 실제값

    # 그래프 title 및 y축, x축 label 설정
    title_size = 20 # 제목의 글자 크기
    label_size = 13 # 축 label의 글자 크기
    ax.set_title('폐업률 예측 모델 성능', size = title_size)
    ax.set_ylabel('폐업률', size = label_size)
    ax.set_xlabel('연도', size = label_size)


# Feature Importance 시각화 코드
def feature_importance(model) :

    # 변수 중요도 항목과 값 추출
    feature_important = model.get_booster().get_score(importance_type='weight')
    keys = list(feature_important.keys())
    values = list(feature_important.values())

    # 그래프 틀 생성
    row_size = 20 # 그래프의 폭 설정
    column_size = 7 # 그래프의 높이 설정
    fig, ax = matplotlib.pyplot.subplots(figsize = (row_size, column_size))
    data_50 = pd.DataFrame(data = values, index = keys, columns = ["score"]).sort_values(by = "score", ascending=False)

    # 그래프 그리기
    limit = 10 # 표현할 최대의 변수 개수 설정
    data_50[:limit].plot(kind = 'barh', ax = ax, label = '')

    # 그래프 title 및 y축, x축 label 설정
    title_size = 20 # 제목의 글자 크기
    label_size = 20 # 축 label의 글자 크기
    ax.set_title('변수 중요도', size = title_size)
    ax.set_xlabel('Score', size = label_size)
