# Comvis_Kaganga_Kelompok_9

Model deteksi Aksara Kaganga/Ulu Rejang menggunakan YOLOv8.

## Anggota Kelompok

1. Aditya Saputa (G1A023024)
2. Muhammad Yasser Ghifari Tegar Awally (G1A023030)
3. Migel Ray Sirait (G1A023088)

## Deskripsi Project

Project ini adalah sistem computer vision untuk mendeteksi Aksara Kaganga atau Aksara Ulu Rejang pada gambar. Sistem menggunakan model object detection YOLOv8 untuk mengenali aksara dalam bentuk suku kata, lalu menghasilkan bounding box, nama kelas aksara, dan nilai confidence untuk setiap objek yang terdeteksi.

Secara umum, alur kerja project adalah:

```text
Dataset YOLO -> Training YOLOv8 -> Evaluasi model -> Prediksi aksara
```

Project ini dapat digunakan sebagai dasar eksperimen pengenalan aksara daerah berbasis citra digital, khususnya untuk deteksi Aksara Kaganga/Ulu Rejang.

## Teknologi yang Digunakan

| Komponen | Keterangan |
| --- | --- |
| Bahasa | Python |
| Framework model | Ultralytics YOLOv8 |
| Task | Object Detection |
| Format dataset | YOLO format |
| Model awal training | `yolov8n.pt` |
| Output utama | Model `.pt`, metrik evaluasi, gambar hasil prediksi, dan label deteksi |
| Akselerasi | CUDA/GPU NVIDIA, sesuai konfigurasi `train.py` |

## Dataset

Dataset disimpan di folder `datasets/` dan dikonfigurasi melalui file `datasets/data.yaml`.

Ringkasan dataset lokal:

| Split | Jumlah gambar | Jumlah label | Folder |
| --- | ---: | ---: | --- |
| Train | 1403 | 1403 | `datasets/train/` |
| Validation | 166 | 166 | `datasets/valid/` |
| Test | 64 | 64 | `datasets/test/` |

Dataset memiliki `253` kelas aksara/suku kata. Daftar lengkap kelas berada di `datasets/data.yaml`. Contoh kelas yang tersedia antara lain `a`, `ba`, `ka`, `nga`, `nyu`, `yang`, dan variasi suku kata lain.

Sumber dataset:

| Informasi | Nilai |
| --- | --- |
| Platform | Roboflow |
| Workspace | `novalrizkiansyah-ymail-com` |
| Project | `aksara-ulu-rejang` |
| Versi | 4 |
| Lisensi | CC BY 4.0 |
| URL | `https://universe.roboflow.com/novalrizkiansyah-ymail-com/aksara-ulu-rejang/dataset/4` |

Struktur dataset mengikuti format YOLO:

```text
datasets/
+-- data.yaml
+-- train/
|   +-- images/
|   +-- labels/
+-- valid/
|   +-- images/
|   +-- labels/
+-- test/
    +-- images/
    +-- labels/
```

Setiap file label `.txt` berisi anotasi bounding box dalam format YOLO:

```text
class_id x_center y_center width height
```

Nilai `x_center`, `y_center`, `width`, dan `height` sudah dinormalisasi terhadap ukuran gambar.

## Struktur Project

Struktur utama project:

```text
project/
+-- datasets/
|   +-- data.yaml
|   +-- train/
|   +-- valid/
|   +-- test/
+-- runs/
|   +-- detect/
|       +-- runs/
|       |   +-- train/
|       |   |   +-- kaganga_v1/
|       |   |       +-- weights/
|       |   +-- predict/
|       |       +-- hasil/
|       +-- val/
+-- train.py
+-- eval.py
+-- predict.py
+-- yolo26n.pt
+-- yolov8n.pt
+-- yolov8s.pt
```

Penjelasan file dan folder utama:

| File/Folder | Fungsi |
| --- | --- |
| `train.py` | Script utama untuk melatih model YOLOv8 pada dataset Aksara Kaganga/Ulu Rejang. |
| `eval.py` | Script evaluasi model pada validation set. |
| `predict.py` | Script prediksi untuk gambar, folder gambar, atau webcam. |
| `datasets/data.yaml` | Konfigurasi path dataset, jumlah kelas, dan daftar nama kelas. |
| `runs/` | Folder output otomatis dari proses training, validation, dan prediction. |
| `yolov8n.pt` | Bobot YOLOv8 nano yang digunakan sebagai model awal training. |
| `yolov8s.pt` | Bobot YOLOv8 small untuk alternatif eksperimen model. |
| `yolo26n.pt` | File bobot model `.pt` lain untuk alternatif eksperimen. |

## Instalasi

Project dapat dijalankan di dalam virtual environment agar dependency Python terpisah dari environment utama.

Buat virtual environment:

```bash
python -m venv .venv
```

Aktifkan virtual environment di Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependency utama:

```bash
pip install ultralytics
```

Jika ingin menggunakan GPU NVIDIA, pastikan driver NVIDIA, CUDA, dan PyTorch yang terpasang sudah mendukung CUDA. Package `ultralytics` akan menggunakan PyTorch yang tersedia di environment.

## Training Model

Training dijalankan dengan command:

```bash
python train.py
```

Konfigurasi utama training berada di bagian atas `train.py`:

| Parameter | Nilai | Keterangan |
| --- | --- | --- |
| `DATA_YAML` | `datasets/data.yaml` | File konfigurasi dataset. |
| `MODEL` | `yolov8n.pt` | Model YOLOv8 nano sebagai pretrained model awal. |
| `EPOCHS` | `100` | Jumlah maksimum epoch training. |
| `IMG_SIZE` | `640` | Ukuran input gambar saat training. |
| `BATCH_SIZE` | `4` | Jumlah gambar per batch. |
| `WORKERS` | `0` | Mematikan multiprocessing agar aman di Windows. |
| `DEVICE` | `cuda` | Menggunakan GPU NVIDIA/CUDA. |
| `PROJECT_DIR` | `runs/train` | Folder output training yang dikirim ke Ultralytics. |
| `RUN_NAME` | `kaganga_v1` | Nama eksperimen training. |
| `optimizer` | `AdamW` | Optimizer yang digunakan. |
| `save_period` | `10` | Checkpoint disimpan setiap 10 epoch. |
| `patience` | `20` | Early stopping jika metrik tidak membaik. |

Script `train.py` juga mengaktifkan augmentasi data seperti variasi warna, rotasi kecil, translasi, scaling, dan mosaic. Horizontal flip dan vertical flip dimatikan karena bentuk aksara dapat berubah makna jika dibalik.

Setelah training selesai, `train.py` mengambil lokasi output aktual dari Ultralytics melalui `results.save_dir`, lalu melakukan evaluasi otomatis menggunakan model `weights/best.pt` dari hasil training tersebut.

## Evaluasi Model

Evaluasi manual dapat dijalankan dengan:

```bash
python eval.py
```

Metrik yang ditampilkan:

| Metrik | Arti singkat |
| --- | --- |
| `mAP50` | Rata-rata akurasi deteksi pada threshold IoU 0.50. |
| `mAP50-95` | Rata-rata akurasi pada beberapa threshold IoU dari 0.50 sampai 0.95. |
| `Precision` | Perbandingan prediksi benar terhadap seluruh prediksi yang dibuat model. |
| `Recall` | Perbandingan objek yang berhasil ditemukan terhadap seluruh objek sebenarnya. |

Konfigurasi model pada `eval.py` menggunakan path:

```text
runs\detect\runs\train\kaganga_v1\weights\best.pt
```

Path tersebut mengarah ke model terbaik dari eksperimen `kaganga_v1`.

## Prediksi Gambar

Prediksi dijalankan dengan:

```bash
python predict.py
```

Konfigurasi utama prediksi berada di `predict.py`:

| Parameter | Nilai | Keterangan |
| --- | --- | --- |
| `MODEL_PATH` | `runs\detect\runs\train\kaganga_v1\weights\best.pt` | Path model yang digunakan untuk prediksi. |
| `SOURCE` | `datasets/test/images` | Sumber gambar, bisa berupa satu gambar, folder, atau `0` untuk webcam. |
| `CONF` | `0.25` | Confidence threshold minimum. |
| `IOU` | `0.45` | IoU threshold untuk Non-Maximum Suppression. |
| `IMG_SIZE` | `416` | Ukuran gambar saat inference. |
| `SAVE_DIR` | `runs/predict` | Folder penyimpanan hasil prediksi baru. |

Output prediksi meliputi:

| Output | Keterangan |
| --- | --- |
| Gambar hasil deteksi | Gambar dengan bounding box, label kelas, dan confidence. |
| Label `.txt` | Hasil deteksi dalam format teks YOLO. |
| Confidence | Nilai keyakinan model untuk setiap prediksi. |
| Ringkasan terminal | Jumlah aksara yang terdeteksi pada setiap gambar. |
| Urutan aksara | Aksara diurutkan dari kiri ke kanan berdasarkan posisi bounding box. |

Jika menggunakan konfigurasi default `predict.py`, hasil prediksi baru akan disimpan ke:

```text
runs/predict/hasil/
```

Artefak prediksi lain berada di:

```text
runs/detect/runs/predict/hasil/
```

## Prediksi Satu Gambar

Untuk prediksi satu gambar, gunakan fungsi `predict_single()` dari `predict.py`.

Contoh penggunaan:

```python
from predict import predict_single

hasil = predict_single(r"datasets\test\images\103_jpg.rf.9bbd8c9d7defd7ea4de352ced697c4ed.jpg")
print("Aksara terdeteksi:", hasil)
```

Fungsi `predict_single()` akan mengembalikan list nama kelas aksara yang terdeteksi dan sudah diurutkan dari kiri ke kanan.

## Hasil Training dan Artefak Output

Artefak training berada di:

```text
runs/detect/runs/train/kaganga_v1/
```

File model:

```text
runs/detect/runs/train/kaganga_v1/weights/best.pt
runs/detect/runs/train/kaganga_v1/weights/last.pt
runs/detect/runs/train/kaganga_v1/weights/epoch0.pt
runs/detect/runs/train/kaganga_v1/weights/epoch10.pt
runs/detect/runs/train/kaganga_v1/weights/epoch20.pt
runs/detect/runs/train/kaganga_v1/weights/epoch30.pt
runs/detect/runs/train/kaganga_v1/weights/epoch40.pt
runs/detect/runs/train/kaganga_v1/weights/epoch50.pt
runs/detect/runs/train/kaganga_v1/weights/epoch60.pt
```

Artefak penting lain:

| Artefak | Fungsi |
| --- | --- |
| `weights/best.pt` | Model terbaik berdasarkan performa validasi. |
| `weights/last.pt` | Model dari epoch terakhir. |
| `results.csv` | Riwayat loss dan metrik setiap epoch. |
| `results.png` | Grafik ringkasan training. |
| `confusion_matrix.png` | Confusion matrix antar kelas. |
| `confusion_matrix_normalized.png` | Confusion matrix versi normalisasi. |
| `BoxPR_curve.png` | Kurva Precision-Recall. |
| `BoxF1_curve.png` | Kurva F1 terhadap confidence. |
| `BoxP_curve.png` | Kurva Precision terhadap confidence. |
| `BoxR_curve.png` | Kurva Recall terhadap confidence. |
| `val_batch*_pred.jpg` | Contoh hasil prediksi model pada validation set. |
| `val_batch*_labels.jpg` | Ground truth label pada validation set. |

Artefak validasi berada di:

```text
runs/detect/val/
```

## Ringkasan Command

```bash
# Install dependency utama
pip install ultralytics

# Training model
python train.py

# Evaluasi model
python eval.py

# Prediksi folder/gambar
python predict.py
```

## Kesimpulan

Project ini membangun pipeline deteksi Aksara Kaganga/Ulu Rejang menggunakan YOLOv8, mulai dari dataset berformat YOLO, proses training, evaluasi performa, sampai prediksi gambar baru. Sistem ini menyediakan alur kerja lengkap untuk melatih model, mengevaluasi performa, dan menjalankan deteksi aksara melalui script Python yang terstruktur.
