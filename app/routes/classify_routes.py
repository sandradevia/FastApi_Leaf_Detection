import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.models.cnn_model import classify_disease
from app.models.yolov5_model import detect_padi

# Inisialisasi router FastAPI
router = APIRouter()

# Fungsi untuk membersihkan folder sementara
def clean_folders(folders):
    """
    Menghapus folder secara rekursif jika ada.
    """
    for folder in folders:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
                print(f"Folder '{folder}' berhasil dihapus.")
            except Exception as e:
                print(f"Gagal menghapus folder '{folder}': {e}")

@router.post("/predict")
async def classify(image: UploadFile = File(...)):
    """
    Endpoint untuk mengklasifikasikan penyakit pada daun padi.
    """
    try:
        # Path penyimpanan sementara untuk file yang diunggah
        upload_dir = './static/uploads'
        os.makedirs(upload_dir, exist_ok=True)
        image_path = os.path.join(upload_dir, image.filename)

        # Simpan file yang diunggah
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        # Jalankan deteksi menggunakan YOLOv5 untuk mendeteksi padi
        detections = detect_padi(image_path)

        if detections:
            # Jika ada deteksi, jalankan klasifikasi penyakit pada daun padi
            label, confidence = classify_disease(image_path)

            # Bersihkan folder setelah proses selesai
            clean_folders([upload_dir, './static/results'])

            # Respon jika tanaman sehat
            if label == 'healthy':
                return JSONResponse(
                    status_code=201,
                    content={
                        "status": "success",
                        "message": "Padi yang dipindai sehat.",
                        "data": None
                    }
                )

            # Respon jika tanaman memiliki penyakit
            return JSONResponse(
                status_code=200,
                content={
                    "status": "success",
                    "message": "Padi yang dipindai memiliki penyakit.",
                    "data": {
                        "label": label,
                        "confidence": confidence
                    }
                }
            )
        else:
            # Jika tidak ada deteksi padi, bersihkan folder dan kembalikan respons error
            clean_folders([upload_dir, './static/results'])

            return JSONResponse(
                status_code=202,
                content={
                    "status": "error",
                    "message": "Tidak dapat mendeteksi daun padi pada foto.",
                    "data": None
                }
            )

    except Exception as e:
        # Bersihkan folder jika terjadi kesalahan
        clean_folders([upload_dir])
        raise HTTPException(status_code=500, detail=str(e))
