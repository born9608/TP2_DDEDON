from fastapi import FastAPI, HTTPException
import pickle
from typing import List
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, Flatten, Dense
from keras import metrics
import tensorflow as tf
import numpy as np
app = FastAPI()

# 모델 로드

model = tf.keras.models.load_model('simple_model_3.h5')


from pydantic import BaseModel

class Item(BaseModel):
    data: List[List[List[float]]]




@app.post("/predict/")
async def get_prediction(item: Item):
    try:
        predictions = model.predict(item.data)  # 예측
        if np.where(predictions > 0.5, 1, 0)[0][0] == 1:
            return {'전세율이 85퍼 이상':'True'}
        else:
            return {'전세율이 85퍼 이상':'False'}

    except:
        raise HTTPException(status_code=400, detail="Model prediction failed.")


'''
5개월치 면적당보증금	면적당매매금	전세율	전세율_분류	위도	경도	이자율(주택대출이자율)
3중 리스트로 입력을 해야 합니다.
테스트데이터 양식: 
{
  "data": [[
    [207.164427, 228.137412, 90.806863, 1.0, 37.7726788, 128.943061, 0.0285],
    [199.646793, 223.839083, 89.1921065, 1.0, 37.7726788, 128.943061, 0.0264],
    [222.682534, 248.23809, 89.7052236, 1.0, 37.7726788, 128.943061, 0.0269],
    [260.329239, 248.297844, 104.84555, 1.0, 37.7726788, 128.943061, 0.0274],
    [220.91184, 236.294295, 93.4901286, 1.0, 37.7726788, 128.943061, 0.0294]
  ]]
}
'''
