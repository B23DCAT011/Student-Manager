import os
import joblib
import numpy as np

model_path = os.path.join(os.path.dirname(__file__), 'C:\\Users\\Admin\\PycharmProjects\\PredAI_Gemini\\models\\du_doan_rot_mon.pkl')
model = joblib.load(model_path)

def convert_to_numpy_array(s):
    """
    Chuyển chuỗi như '8.5, 7.0, 9.0, 1, 7.2' sang mảng NumPy kiểu float
    """
    # Tách chuỗi thành danh sách, loại bỏ khoảng trắng và ép kiểu float
    float_list = [float(x.strip()) for x in s.split(',')]
    return np.array(float_list)

def predict_percent(data):
  # Dữ liệu đầu vào cần có các trường: diem_chuyen_can, diem_bai_tap, diem_giua_ky, so_mon_da_rot, GPA
  data = convert_to_numpy_array(data)
  arr = data.reshape(1, -1)  # Reshape để phù hợp với đầu vào của mô hình
  proba = model.predict_proba(arr)[0][1]
  return round(proba * 100, 2)  # Trả về xác suất dưới dạng phần trăm