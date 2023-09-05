# 아파트 역전세 위험 예측 프로젝트

'떼일 돈 받아드립니다' 팀

구성원: 

임진우 

조윤서 https://github.com/chobbong 

김우영 

김범성

진행기간: 2023.08.09~ 2023.09.05

<p align="center">
  <br>
  <img src="./images/logo-sample.jpeg">
  <br>
</p>

## 프로젝트 소개

<p align="justify">
프로젝트 개요/동기

   전세사기가 아파트 거래 시장의 새로운 화두로 떠올랐다. 현금 없이 전세보증금으로 주택을 매입하는 무자본 거래, HUG 보증보험의 허점을 이용한 사례, 법인으로 주택을 매입하고 등기로 확인할 수 없는 세금 차입을 이용한 사례 등 조직적인 전세사기가 부동산 시장에 파장을 일으키고 있다.
  의도적인 전세사기 뿐만 아니다. 불황으로 역전세 현상이 전국적으로 발생해 전세보증금을 돌려받지 못하는 세입자가 다수 발생하고 있다.  

  부동산 시장의 구조적 문제가 이를 심화시킨다. 주택 시장의 가격 결정 메커니즘은 매우 복잡해 소비자가 독자적인 판단 기준을 세우기 어렵다.
   신축 아파트의 경우, 물 밑에서 이뤄지는 호가와 합리적인 수준의 매매가에 접근하기 어려워 비대칭 정보로 인한 시장 왜곡이 강화된다.
   
  이번 프로젝트는 전세 수요자가 한정된 정보로도 적절한 전세가를 판단할 수 있고 단기 전세가율 추세를 예측해 역전세 위험을 판단할 수 있는 모델을 설계했다. 
</p>

### 프로젝트 목표
 1. 소비자가 역전세 위험을 판단할 수 있는 다양한 예측 모델을 설계한다.
 2. 개발한 모델을 웹앱으로 손쉽게 사용할 수 있도록 한다.(Django)
 3. 부동산이 낯선 소비자도 직관적으로 이해할 수 있도록 예측 결과를 시각화한다.


## 개발 환경

| Python | Xgboost |  Tensorflow   |  Django   |
| :--------: | :--------: | :------: | :-----: |
|   ![python]    |   ![xgboost]    | ![tf] | ![Django] |

python == 3.8.10 에서 개발

## 구현한 모델

### 모델 1 - ImJW 폴더
CNN 기반 딥러닝을 통해 전세가율 추세를 예측해 역전세 위험을 감지하는 분류 모델

### 모델 2 - KimBS 폴더
XGBoost 기반 머신러닝을 통해 전세가율에 따라 위험도를 판단하는 분류 모델

### 모델 3 - KimWY 폴더
LSTM 기반 딥러닝을 통해 과거 데이터로 다음 월의 면적당매매금 면적당보증금을 예측하는 회귀 모델

<br>

## 대시보드 및 웹앱 링크

[대시보드(스트림릿)](https://20230819.streamlit.app)

[웹앱(장고)](http://3.35.70.239:8000/)

## 발표 자료

[PPT 및 발표영상](https://drive.google.com/drive/folders/1oZtuQKOwznLOpZv-ERYOgFKYAMNhzJov?usp=sharing)

<p align="justify">

</p>

<br>

## 라이센스

MIT &copy; [NoHack](mailto:lbjp114@gmail.com)

<!-- Stack Icon Refernces -->

[python]: /images/stack/python.svg
[xgboost]: /images/stack/xgboost.svg
[tf]: /images/stack/Tf.svg
[Django]: /images/stack/django.svg
