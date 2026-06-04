from ultralytics import YOLO
import os

# -----------------------------------------
# KONFIGURASI
# -----------------------------------------
MODEL_PATH  = r"runs\detect\runs\train\kaganga_v1\weights\best.pt"
SOURCE      = "datasets/test/images"  # bisa: path 1 gambar, folder, atau 0 (webcam)
CONF        = 0.25                    # confidence threshold (0.0 - 1.0)
IOU         = 0.45                    # IoU threshold untuk NMS
IMG_SIZE    = 416                     # Ukuran gambar
SAVE_DIR    = "runs/predict"          # folder hasil prediksi
# -----------------------------------------


def predict():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model tidak ditemukan di '{MODEL_PATH}'.\n"
            "Pastikan path MODEL_PATH sudah benar."
        )

    print("=" * 50)
    print("  Deteksi Aksara Kaganga")
    print("=" * 50)
    print(f"  Model  : {MODEL_PATH}")
    print(f"  Source : {SOURCE}")
    print(f"  Conf   : {CONF}")
    print("=" * 50)

    model = YOLO(MODEL_PATH)

    results = model.predict(
        source      = SOURCE,
        conf        = CONF,
        iou         = IOU,
        imgsz       = IMG_SIZE,
        save        = True,          # simpan gambar hasil deteksi
        save_txt    = True,          # simpan label hasil deteksi
        save_conf   = True,          # tampilkan confidence di label
        project     = SAVE_DIR,
        name        = "hasil",
        show_labels = True,
        show_conf   = True,
        line_width  = 2,
    )

    print(f"\nPrediksi selesai!")
    print(f"  Hasil disimpan di: {SAVE_DIR}/hasil/")

    # Tampilkan ringkasan per gambar
    print("\nRingkasan Deteksi:")
    for r in results:
        nama_file = os.path.basename(r.path)
        jumlah    = len(r.boxes)
        print(f"  {nama_file} -> {jumlah} aksara terdeteksi")

        if jumlah > 0:
            # Urutkan kotak dari kiri ke kanan (urutan baca aksara)
            boxes = sorted(r.boxes, key=lambda b: b.xyxy[0][0].item())
            kelas = [r.names[int(b.cls)] for b in boxes]
            print(f"  Urutan aksara : {' | '.join(kelas)}")
            print()

def predict_single(image_path: str):
    """Prediksi satu gambar dan kembalikan hasilnya sebagai list suku kata."""
    model = YOLO(MODEL_PATH)
    results = model.predict(source=image_path, conf=CONF, iou=IOU, imgsz=IMG_SIZE, verbose=False)

    if not results:
        return []

    r = results[0]
    boxes = sorted(r.boxes, key=lambda b: b.xyxy[0][0].item())
    return [r.names[int(b.cls)] for b in boxes]

# Wajib di Windows agar multiprocessing tidak error
if __name__ == "__main__":
    predict()

