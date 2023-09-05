import pandas as pd
from .class_model import MyModel
import plotly.graph_objs as go
import plotly.utils
import json


import pandas as pd
from .class_model import MyModel
import plotly.graph_objs as go
import plotly.offline as pyo
import json

class Model_predict:
    def __init__(self, file_path, model_path):
        self.file_path = file_path
        self.my_model = MyModel(model_path=model_path)

    def load_data(self):
        df = pd.read_csv(self.file_path)
        location_dict = {}
        for index, row in df.iterrows():
            location_dict[row['시군구']] = {'위도': row['위도'], '경도': row['경도']}
        return df, location_dict
    

    def get_data_by_location(self,df, year, month, selected_do, selected_sigun, selected_eup, selected_ri):
          target_date = int(f"{year}{month:02d}") - 1
          if target_date >= 202308:
               raise ValueError('선택하신 연월은 2023년 8월보다 클 수 없습니다.')
          A = (selected_do or "") + " " + (selected_sigun or "") + " " + (selected_eup or "") + " " + (selected_ri or "")
          A = A.replace("--선택--", "")
          input_data = str(A).rstrip()
          print(target_date)
          print(input_data)
          try: 
              matched_indices = list(df.query("`계약년월` == @target_date and `시군구` == @input_data").index)[0]
          except:
              raise ValueError('유효하지 않은 matched_indices 값입니다.')
          if matched_indices is not None and 0 <= matched_indices < len(df):
               start_index = max(0, matched_indices - 4)
               end_index = min(len(df) -1, matched_indices)

               input_dict = {}
               for col in ['면적당보증금', '면적당매매금', '전세율', '위도', '경도', '이자율']:
                    input_dict[col] = list(df[col].iloc[start_index:end_index+1])
               return input_dict
          else:
               raise ValueError('유효하지 않은 matched_indices 값입니다.')

    def predict(self, year, month, selected_do, selected_sigun, selected_eup, selected_ri):
        df, location_dict = self.load_data()
        input_dict = self.get_data_by_location(df, year, month, selected_do, selected_sigun, selected_eup, selected_ri)
        input_data = self.my_model.input_data(input_dict)
        
        prediction = self.my_model.model_2(input_data)
        if prediction == 0:
          return "전세율이 80퍼센트를 넘지 않을 것으로 예상됩니다"
        else:
          return "전세율이 80퍼센트를 넘을 것으로 예상됩니다"


    def get_chart_data(self,target_date, input_dict):
          new_dict = {
               '연월': range(target_date-4, target_date+1),
               '전세율': input_dict['전세율']
          }

          df = pd.DataFrame(new_dict)
          df['연월'] = pd.to_datetime(df['연월'], format='%Y%m')  # 연월을 datetime 타입으로 변환
          df.set_index('연월', inplace=True)
          return df


    def create_plot(self,df):
          data = [
               go.Scatter(
                    x=df.index,
                    y=df['전세율'],
                    mode='lines'
               )
          ]

          layout = go.Layout(
               title='전세율 추이',
               xaxis=dict(title='연월'),
               yaxis=dict(title='전세율'),
          )

          figure = go.Figure(data=data, layout=layout)
          graph_json = json.dumps(figure, cls=plotly.utils.PlotlyJSONEncoder)
          return graph_json
