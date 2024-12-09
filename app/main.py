# import os
# import numpy as np
# from fastapi import FastAPI, UploadFile, File
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing import image
# from tensorflow.keras.optimizers import Adam
# from io import BytesIO
# from PIL import Image
# from typing import List

# # Inisialisasi aplikasi FastAPI
# app = FastAPI()

# # Memuat model yang sudah dilatih
# model = load_model('models/rice_leaf_disease_model (2).h5')

# # Compile model (opsional jika hanya untuk inferensi)
# model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

# # Ukuran input model
# input_size = (150, 150)

# # Membaca daftar nama kelas dari direktori dataset
# class_names = sorted(os.listdir('dataset/train'))  # Sesuaikan path dengan dataset Anda

# # Fungsi untuk memproses gambar agar sesuai dengan input model
# def preprocess_image(img: Image.Image) -> np.ndarray:
#     """
#     Memproses gambar untuk model:
#     - Konversi ke RGB
#     - Resize ke ukuran input model
#     - Normalisasi ke [0, 1]
#     - Menambah dimensi batch
#     """
#     img = img.convert("RGB")  # Konversi gambar ke RGB
#     img = img.resize(input_size)  # Sesuaikan ukuran dengan model
#     img_array = np.array(img, dtype=np.float32) / 255.0  # Normalisasi
#     img_array = np.expand_dims(img_array, axis=0)  # Tambah dimensi batch
#     return img_array

# # Fungsi untuk prediksi penyakit
# def predict_disease(img: Image.Image, threshold: float = 0.85) -> dict:
#     """
#     Prediksi penyakit dari gambar yang diunggah:
#     - Mengembalikan nama kelas dengan probabilitas tertinggi dan daftar semua probabilitas.
#     """
#     img_array = preprocess_image(img)  # Preproses gambar
#     predictions = model.predict(img_array)[0]  # Prediksi
#     predicted_class_idx = np.argmax(predictions)  # Indeks kelas dengan skor tertinggi
#     probability = float(predictions[predicted_class_idx])  # Probabilitas tertinggi

#     if probability < threshold:  # Jika probabilitas di bawah ambang batas
#         return {
#             "predicted_disease": "unknown",
#             "probability": probability,
#             "all_probabilities": predictions.tolist()
#         }

#     # Nama penyakit berdasarkan prediksi
#     predicted_disease = class_names[predicted_class_idx]

#     return {
#         "predicted_disease": predicted_disease,
#         "probability": probability,
#         "all_probabilities": predictions.tolist()
#     }

# # Endpoint untuk menerima gambar dan memberikan prediksi
# @app.post("/predict/")
# async def predict(file: UploadFile = File(...)):
#     """
#     Endpoint untuk prediksi:
#     - Menerima file gambar
#     - Mengembalikan hasil prediksi
#     """
#     try:
#         # Membaca dan memproses gambar
#         image_data = await file.read()
#         img = Image.open(BytesIO(image_data))

#         # Melakukan prediksi
#         result = predict_disease(img)

#         # Mengembalikan hasil sebagai JSON
#         return result

#     except Exception as e:
#         # Mengembalikan error jika ada kesalahan
#         return {"error": str(e)}

from fastapi import FastAPI
from app.routes.classify_routes import router

app = FastAPI()

# Daftarkan router
app.include_router(router, prefix="/api", tags=["Classification"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Rice Leaf Disease Classification API"}
