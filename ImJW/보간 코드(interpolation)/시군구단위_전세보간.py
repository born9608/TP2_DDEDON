


import pandas as pd
import os


total_apart = pd.read_csv("latlng_results.csv")
city_apart = pd.read_csv("시단위_noise보간_데이터.csv")

total_apart

city_apart= city_apart[['시',	'계약년월'	,'면적당매매금'	,'도'	,'면적당보증금']]

# directory containing the files
dir_path = "파일경로지정"

# 현재 디렉토리의 모든 파일 목록을 가져옵니다.
files = os.listdir(dir_path)
# print(files)

# .xlsx 또는 .xls 확장자를 가진 파일만 선택합니다.
excel_files = [f for f in files if f.endswith(('.csv'))]
dfs_list = []

# 각 엑셀 파일을 순차적으로 읽어들이고, 데이터프레임 리스트에 추가합니다.
for file in excel_files:
    full_path = os.path.join(dir_path, file)
    try:
        df = pd.read_csv(full_path)
        dfs_list.append(df)
    except:
        try:
            df = pd.read_csv(full_path,encoding='cp949')
            dfs_list.append(df)
        except:
            print('오류발생')
    # print(len(dfs_list))

merged_df = pd.concat(dfs_list, ignore_index=True)
# display(merged_df)


merged_df = merged_df[merged_df['전월세구분']=='전세']

merged_df['보증금(만원)'] = merged_df['보증금(만원)'].astype(str)
merged_df['보증금(만원)']= merged_df['보증금(만원)'].str.replace(',', '').astype(float)

merged_df['면적당보증금'] = merged_df['보증금(만원)'] /merged_df['전용면적(㎡)']

df = merged_df[['시군구','면적당보증금','계약년월']]
df.reset_index(drop=True,inplace = True)
# display(df)

df['면적당보증금'] = df['면적당보증금'].astype(str)
df['면적당보증금']= df['면적당보증금'].str.replace(',', '').astype(float)
total_df = df.groupby(['계약년월', '시군구'])['면적당보증금'].mean().reset_index()

total_df['시'] = total_df['시군구'].str.split().str[0] + " " + total_df['시군구'].str.split().str[1]
# display(total_df)

grouped_data = total_df.groupby(['시군구', '계약년월'])[['면적당보증금']].mean().reset_index()

# 201908부터 202308까지의 데이터만 필터링
filtered_data = grouped_data[(grouped_data['계약년월'] >= 201908) & (grouped_data['계약년월'] <= 202307)]

filtered_data.head()

filtered_data = filtered_data.sort_values(['시군구','계약년월'])

filtered_data.reset_index(inplace = True,drop = True)

unique_dates_per_city = filtered_data.groupby('시군구')['계약년월'].nunique()
# print(unique_dates_per_city)
s = 0
for i in unique_dates_per_city:
    if i!=48:
        s+=1

# print(s)

# 시단위와 계약년월에 따른 면적당매매가와 면적당보증금의 평균 계산
grouped_data_2 = city_apart[['시'	,'계약년월'	,'면적당보증금']]
grouped_data_2


# 201908부터 202308까지의 데이터만 필터링
filtered_data_2 = grouped_data_2[(grouped_data_2['계약년월'] >= 201908) & (grouped_data_2['계약년월'] <= 202307)]

filtered_data_2.head()

filtered_data_2 = filtered_data_2.sort_values(['시','계약년월'])
filtered_data_2.reset_index(inplace = True,drop = True)
unique_dates_per_city = filtered_data_2.groupby('시')['계약년월'].nunique()
# print(unique_dates_per_city)
s = 0
for i in unique_dates_per_city:
    if i!=48:
        s+=1

# print(s)

filtered_data_2['변화율'] = filtered_data_2.groupby('시')['면적당보증금'].pct_change() * 100
# display(filtered_data_2)

Do_rc = filtered_data_2[['시','계약년월','변화율','면적당보증금']]


unique_dates_per_city = filtered_data.groupby('시군구')['계약년월'].nunique()

# 인덱스 이름 출력
cities_with_different_dates = unique_dates_per_city[unique_dates_per_city != 48].index.tolist()
cities_with_different_dates


cities = filtered_data ['시군구'].unique()
months = filtered_data ['계약년월'].unique()
all_combinations = [(city, month) for city in cities for month in months]
all_combinations_df = pd.DataFrame(all_combinations, columns=['시군구', '계약년월'])
all_combinations_df

merged_df = pd.merge(all_combinations_df, filtered_data , on=['시군구', '계약년월'], how='left')

# 누락된 값 처리
# '도' 컬럼은 '시' 컬럼에서 추출 가능
# '면적당보증금' 및 '변화율' 컬럼은 NaN으로 둠 (이후 필요에 따라 처리 가능)

merged_df.info()

merged_df

merged_df['시'] = merged_df['시군구'].str.split().str[0] +" " + merged_df['시군구'].str.split().str[1] 
merged_df

merged_df = merged_df.sort_values(['시군구','계약년월'])
merged_df.reset_index(drop=True,inplace = True)

merged_df


# 연속된 결측치 찾기
merged_df['missing'] = merged_df['면적당보증금'].isna()
merged_df['block'] = (merged_df['missing'] != merged_df['missing'].shift()).cumsum()

# 각 연속된 결측치 블록의 시작과 끝 계산
missing_periods = merged_df[merged_df['missing']].groupby('block').agg({
    '시군구': 'first',
    '계약년월': ['first', 'last'],
    '시': 'first'
})


merged_df

missing_periods.reset_index(inplace=True,drop=True)
# display(missing_periods)

missing_not_converted = missing_periods[missing_periods['계약년월']['first']==201908]
# display(missing_not_converted)

set_delete_city = set(missing_not_converted['시군구']['first'])
set_delete_city 

merged_df = merged_df[~merged_df['시군구'].isin(set_delete_city)]

# display(merged_df)

merged_df.reset_index(drop=True,inplace=True)

merged_df

merged_df['missing'] = merged_df['면적당보증금'].isna()
merged_df['block'] = (merged_df['missing'] != merged_df['missing'].shift()).cumsum()
merged_df

L = []
for i in range(len(merged_df['시군구'])):
    if merged_df.loc[i]['missing'] == True and merged_df.loc[i]['계약년월'] ==201908:
        L.append(merged_df.loc[i]['시군구'])

L = set(L)
merged_df = merged_df[~merged_df['시군구'].isin(L)]

# display(merged_df)

merged_df.reset_index(inplace = True,drop=True)

for i in range(len(merged_df['시군구'])):
    if merged_df.loc[i]['missing'] == True and merged_df.loc[i]['계약년월'] ==201908:
        print('연속적이지않음')

merged_df['missing'] = merged_df['면적당보증금'].isna()
merged_df['block'] = (merged_df['missing'] != merged_df['missing'].shift()).cumsum()
missing_start = None
# 결측치 시작 및 끝 인덱스 찾기
missing_periods = []
missing_start = None
for idx, row in merged_df.iterrows():
    if pd.isna(row['면적당보증금']) and missing_start is None:
        missing_start = idx
    elif not pd.isna(row['면적당보증금']) and missing_start is not None:
        missing_periods.append([missing_start, idx-1])
        missing_start = None

# 마지막 부분에 연속된 결측치가 있는 경우
if missing_start is not None:
    missing_periods.append([missing_start, merged_df.index[-1]])

# print(missing_periods)

Do_rc

merged_df

merged_df.info()

B = []
for i in missing_periods:
    A = []
    missing_start = i[0]
    idx = i[1]
    for j in range(missing_start,idx+1):
        if Do_rc[(Do_rc['시'] == merged_df.loc[j]['시']) & (Do_rc['계약년월'] == merged_df.loc[j]['계약년월'])]['변화율'].empty:
            # print('a')
        else:
            A.append(float(Do_rc[(Do_rc['시'] == merged_df.loc[j]['시']) & (Do_rc['계약년월'] == merged_df.loc[j]['계약년월'])]['변화율']))
    B.append(A)
# print(B)

# print(set([len(i) for i in B]))

merged_df

missing_periods

total_list =[]
for i in range(len(missing_periods)):
    save_list = []
    missing_start = missing_periods[i][0]
    idx = missing_periods[i][1]
    # print(merged_df.loc[missing_start]['시군구'])
    # print(merged_df.loc[missing_start-1]['면적당보증금'])
    rc = (merged_df.loc[idx+1]['면적당보증금'] - merged_df.loc[missing_start -1 ]['면적당보증금'])/(idx+2-missing_start)
    # print(f"변화량: {rc}")
    for k in range(len(B[i])):
       save_list.append(((k+1)*rc*((B[i][k]/100)+1))+merged_df.loc[missing_start -1 ]['면적당보증금'])
    # print(merged_df.loc[idx+1]['면적당보증금'])
    total_list.append(save_list)

total_list

for i in range(len(missing_periods)):
    for j in range(missing_periods[i][0],missing_periods[i][1]+1):
        try:
            merged_df['면적당보증금'].loc[j] = float(total_list[i][j-missing_periods[i][0]])
        except:
            continue
    # print('------')

merged_df.info()

merged_df

merged_df['면적당보증금'] = merged_df['면적당보증금'].interpolate(method='linear')

merged_df.info()

merged_df.info()

merged_df.to_csv("시군구단위_noise_보간데이터_2_전세.csv")

merged_df

