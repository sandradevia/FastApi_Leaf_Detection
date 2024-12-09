import tensorflow as tf
import numpy as np
from PIL import Image
import os

def classify_disease(image_path: str, model_path: str = 'models/rice_leaf_disease_model (2).h5'):
    """
    Melakukan klasifikasi penyakit pada daun padi menggunakan model .h5.

    Args:
        image_path (str): Path ke gambar input.
        model_path (str): Path ke model .h5.

    Returns:
        tuple: (label_prediksi, confidence) dalam bentuk string dan float.
    """
    try:
        # Validasi keberadaan file
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file '{image_path}' tidak ditemukan.")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file '{model_path}' tidak ditemukan.")

        # Label penyakit (sesuaikan dengan urutan kelas di model Anda)
        labels = [
            "Bacterial Leaf Blight",
            "Brown Spot",
            "Healthy",
            "Leaf Blast",
            "Leaf Scald",
            "Narrow Brown Spot",
        ]

        # Memuat model .h5
        model = tf.keras.models.load_model(model_path)

        # Menentukan ukuran input yang diharapkan oleh model
        input_size = (150, 150)  # Sesuaikan dengan ukuran input model Anda

        # Memuat dan memproses gambar
        image = Image.open(image_path).convert("RGB")  # Pastikan format gambar RGB
        image = image.resize(input_size)  # Resize gambar sesuai model
        image = np.array(image, dtype=np.float32) / 255.0  # Normalisasi ke [0, 1]
        image = np.expand_dims(image, axis=0)  # Tambahkan dimensi batch

        # Menjalankan inferensi dengan model
        output_data = model.predict(image)

        # Menampilkan hasil probabilitas
        print("Probabilitas kelas yang terdeteksi:")
        print(output_data)

        # Menentukan prediksi label dan confidence tertinggi
        predicted_index = np.argmax(output_data)
        confidence = float(output_data[0][predicted_index])
        label_prediksi = labels[predicted_index]

        # Mengembalikan hasil
        return label_prediksi, confidence
    except Exception as e:
        raise RuntimeError(f"Error saat melakukan klasifikasi: {str(e)}")
