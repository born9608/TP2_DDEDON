from django.shortcuts import render
from .ijw_utils import Model_predict
import pandas as pd
import json
import numpy as np
# 데이터 로드
file_path = "./ijw/save/learndata.csv"
model_path = './ijw/save/simple_model_3.h5'

model_predict_instance = Model_predict(file_path, model_path)
df, location_dict = model_predict_instance.load_data()

# '시군구' 컬럼을 공백으로 쪼개서 새로운 DataFrame 생성
split_df = df['시군구'].str.split(' ', expand=True)
split_df.columns = ['도', '시군', '읍면동', '리']
def predict_view(request):
    context = {
        'years': range(2023, 2024),
        'months': range(6, 12),
        'dos': np.insert(split_df['도'].fillna("").unique(),0, '--선택--'),
        'siguns': [],  # 초기에는 비어있음
        'eups': [],    # 초기에는 비어있음
        'ris': [],     # 초기에는 비어있음
    }

    if request.method == 'POST':
        year = int(request.POST.get('year'))
        month = int(request.POST.get('month'))

        selected_do = request.POST.get('do')
        selected_sigun = request.POST.get('sigun')
        selected_eup = request.POST.get('eup')
        selected_ri = request.POST.get('ri')

        try:
            prediction = model_predict_instance.predict(year, month, selected_do, selected_sigun, selected_eup, selected_ri)
            context["prediction"] = prediction

            target_date = int(f"{year}{month:02d}") - 1
            input_dict = model_predict_instance.get_data_by_location(df, year, month, selected_do, selected_sigun, selected_eup, selected_ri)
            df_chart = model_predict_instance.get_chart_data(target_date, input_dict)
            context['plot'] = model_predict_instance.create_plot(df_chart)
            print(context['plot'] )

        except ValueError as e:
            context["warning"] = str(e)

    return render(request, 'ijw/ijw.html', context)

from django.http import JsonResponse
# 'do'에 따른 'sigun'을 반환
# 'do'에 따른 'sigun'을 반환

# 'do'에 따른 'sigun'을 반환
def get_sigun(request):
    selected_do = request.GET.get('selected_value')
    filtered_sigun = split_df[split_df['도'] == selected_do]['시군'].unique()
    filtered_sigun = np.insert(filtered_sigun, 0, '--선택--')
    return JsonResponse(list(filtered_sigun), safe=False)

# 'do'와 'sigun'에 따른 'eup'을 반환
def get_eup(request):
    selected_do = request.GET.get('selected_do')
    selected_sigun = request.GET.get('selected_value')
    filtered_eup = split_df[(split_df['도'] == selected_do) & (split_df['시군'] == selected_sigun)]['읍면동'].unique()
    filtered_eup = np.insert(filtered_eup, 0, '--선택--')
    return JsonResponse(list(filtered_eup), safe=False)

# 'do', 'sigun', 'eup'에 따른 'ri'을 반환
def get_ri(request):
    selected_do = request.GET.get('selected_do')
    selected_sigun = request.GET.get('selected_sigun')
    selected_eup = request.GET.get('selected_value')
    filtered_ri = split_df[(split_df['도'] == selected_do) & (split_df['시군'] == selected_sigun) & (split_df['읍면동'] == selected_eup)]['리'].unique()
    filtered_ri = np.insert(filtered_ri, 0, '--선택--')
    return JsonResponse(list(filtered_ri), safe=False)