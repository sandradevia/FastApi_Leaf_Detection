# # import tensorflow as tf
# # import os

# # def load_model():
# #     try:
# #         path_model = os.getenv("MODEL_PATH", "models/paddy_disease_model.h5")
# #         model = tf.keras.models.load_model(path_model)
# #         print("Model berhasil dimuat.")
# #         return model
# #     except Exception as e:
# #         raise RuntimeError(f"Error saat memuat model: {e}")
    

# # def predict_disease(model, image):
# #     # Predict the disease
# #     predictions = model.predict(image)
# #     class_index = predictions.argmax(axis=-1)[0]
# #     class_names = ["Healthy", "Brown Spot", "Blast", "Sheath Blight"]  # Example classes
# #     return class_names[class_index]
    
# import os
# import shutil
# from fastapi import APIRouter, UploadFile, File, HTTPException
# from fastapi.responses import JSONResponse
# from .yolov5_model import detect_padi
# from .cnn_model import classify_disease

# # Inisialisasi router FastAPI
# router = APIRouter()

# def clean_folders(folders):
#     """
#     Menghapus folder secara rekursif jika ada.
#     """
#     for folder in folders:
#         if os.path.exists(folder):
#             try:
#                 shutil.rmtree(folder)
#                 print(f"Folder '{folder}' berhasil dihapus.")
#             except Exception as e:
#                 print(f"Gagal menghapus folder '{folder}': {e}")

# @router.post("/detect")
# async def detect(image: UploadFile = File(...)):
#     """
#     Endpoint untuk mendeteksi padi dan mengidentifikasi penyakitnya.
#     """
#     try:
#         # Path penyimpanan sementara untuk file yang diunggah
#         upload_dir = './static/uploads'
#         os.makedirs(upload_dir, exist_ok=True)
#         image_path = os.path.join(upload_dir, image.filename)

#         # Simpan file yang diunggah
#         with open(image_path, "wb") as buffer:
#             shutil.copyfileobj(image.file, buffer)

#         # Jalankan deteksi menggunakan YOLOv5
#         detections = detect_padi(image_path)

#         if detections:
#             # Jalankan identifikasi penyakit
#             label, confidence = classify_disease(image_path)

#             # Bersihkan folder setelah proses selesai
#             clean_folders(['./static/uploads', './static/results'])

#             if label == 'healthy':
#                 return JSONResponse(
#                     status_code=201,
#                     content={
#                         "status": "success",
#                         "message": "Padi yang dipindai sehat.",
#                         "data": None
#                     }
#                 )

#             return JSONResponse(
#                 status_code=200,
#                 content={
#                     "status": "success",
#                     "message": "Padi yang dipindai memiliki penyakit.",
#                     "data": {
#                         "label": label,
#                         "confidence": confidence
#                     }
#                 }
#             )
#         else:
#             # Bersihkan folder jika tidak ada deteksi
#             clean_folders(['./static/uploads', './static/results'])

#             return JSONResponse(
#                 status_code=202,
#                 content={
#                     "status": "error",
#                     "message": "Tidak dapat mendeteksi daun padi pada foto.",
#                     "data": None
#                 }
#             )
#     except Exception as e:
#         # Bersihkan folder jika terjadi kesalahan
#         clean_folders(['./static/uploads', './static/results'])
#         raise HTTPException(status_code=500, detail=str(e))
