# Comvis_Kaganga_Kelompok_9
Model Deteksi Aksara Kaganga

# Anggota Kelompok
1. Aditya Saputa (G1A023024)
2. Muhammad Yasser Ghifari Tegar Awally (G1A023030)
3. Migel Ray Sirait (G1A023088)

# Deteksi Aksara Kaganga/Ulu Rejang Menggunakan YOLOv8

Project ini adalah sistem computer vision untuk mendeteksi Aksara Kaganga atau Aksara Ulu Rejang pada gambar menggunakan model object detection YOLOv8. Model dilatih untuk mengenali aksara dalam bentuk suku kata, lalu menghasilkan bounding box, nama kelas aksara, dan nilai confidence untuk setiap aksara yang terdeteksi.
Project ini digunakan sebagai dasar eksperimen computer vision untuk pengenalan aksara daerah, khususnya pada proses deteksi Aksara Kaganga dari citra digital.

## Teknologi yang Digunakan

| Komponen | Keterangan |
| --- | --- |
| Bahasa | Python |
| Framework model | Ultralytics YOLOv8 |
| Model awal | `yolov8n.pt` |
| Jenis task | Object Detection |
| Format dataset | YOLO format |
| Akselerasi | CUDA/GPU NVIDIA |
| Output utama | Model `.pt`, metrik evaluasi, gambar hasil prediksi, dan label deteksi |

## Dataset

Dataset disimpan di folder `datasets/` dan dikonfigurasi melalui file `datasets/data.yaml`.

Ringkasan dataset lokal:

| Split | Jumlah gambar | Jumlah label | Folder |
| --- | ---: | ---: | --- |
| Train | 1403 | 1403 | `datasets/train/` |
| Validation | 166 | 166 | `datasets/valid/` |
| Test | 64 | 64 | `datasets/test/` |

Dataset memiliki `253` kelas aksara/suku kata. Contoh kelas yang tersedia antara lain `a`, `ba`, `ka`, `nga`, `nyu`, `yang`, dan banyak variasi suku kata lain yang didefinisikan di `datasets/data.yaml`.

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

Nilai koordinat pada label YOLO sudah dinormalisasi terhadap ukuran gambar.

## Struktur Project

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
|       |   +-- predict/
|       +-- val*/
+-- train.py
+-- eval.py
+-- predict.py
+-- cek.py
+-- yolov8n.pt
+-- yolo26n.pt
```

Penjelasan file utama:

| File/Folder | Fungsi |
| --- | --- |
| `train.py` | Script utama untuk melatih model YOLOv8 pada dataset Aksara Kaganga. |
| `eval.py` | Script evaluasi model terbaik pada validation set. |
| `predict.py` | Script prediksi untuk gambar baru, folder gambar, atau webcam. |
| `cek.py` | Contoh sederhana penggunaan fungsi `predict_single()` untuk satu gambar. |
| `datasets/data.yaml` | Konfigurasi path dataset, jumlah kelas, dan daftar nama kelas. |
| `runs/` | Folder output otomatis dari proses training, validation, dan prediction. |
| `*.pt` | File bobot model YOLO/PyTorch. |

## Alur Kerja Project

Project ini memiliki empat tahap utama:

1. Menyiapkan dataset dalam format YOLO di folder `datasets/`.
2. Melatih model YOLOv8 menggunakan `train.py`.
3. Mengevaluasi model hasil training menggunakan `eval.py` atau validasi otomatis di akhir `train.py`.
4. Menggunakan model untuk mendeteksi aksara pada gambar baru melalui `predict.py` atau `cek.py`.

Secara umum, alurnya seperti berikut:

```text
Dataset YOLO -> Training YOLOv8 -> Model best.pt -> Evaluasi -> Prediksi aksara
```

## Instalasi

Project dapat dijalankan di dalam virtual environment agar dependency Python berada dalam lingkungan yang terpisah.

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

Jika ingin menggunakan GPU NVIDIA, pastikan driver NVIDIA, CUDA, dan versi PyTorch yang terpasang sudah mendukung CUDA. Package `ultralytics` biasanya akan menggunakan PyTorch yang tersedia di environment.

## Training Model

Training dijalankan melalui:

```bash
python train.py
```

Konfigurasi utama training berada di bagian atas `train.py`:

| Parameter | Nilai | Keterangan |
| --- | --- | --- |
| `DATA_YAML` | `datasets/data.yaml` | File konfigurasi dataset. |
| `MODEL` | `yolov8n.pt` | Model YOLOv8 nano sebagai pretrained model awal. |
| `EPOCHS` | `100` | Jumlah maksimum epoch training. |
| `IMG_SIZE` | `416` | Ukuran input gambar saat training. |
| `BATCH_SIZE` | `4` | Jumlah gambar per batch. |
| `WORKERS` | `0` | Mematikan multiprocessing agar aman di Windows. |
| `DEVICE` | `cuda` | Menggunakan GPU NVIDIA/CUDA. |
| `PROJECT_DIR` | `runs/train` | Folder output training yang dikirim ke Ultralytics. |
| `RUN_NAME` | `kaganga_v1` | Nama eksperimen training. |
| `optimizer` | `AdamW` | Optimizer yang digunakan. |
| `save_period` | `10` | Checkpoint disimpan setiap 10 epoch. |
| `patience` | `20` | Early stopping jika metrik tidak membaik. |

Script `train.py` juga menggunakan augmentasi data, antara lain variasi warna, rotasi kecil, translasi, scaling, dan mosaic. Augmentasi horizontal dan vertical flip dimatikan karena bentuk aksara dapat berubah makna jika dibalik.

## Evaluasi Model

Setelah training selesai, `train.py` otomatis melakukan validasi menggunakan model terbaik `best.pt` dan menampilkan metrik:

| Metrik | Arti singkat |
| --- | --- |
| `mAP50` | Rata-rata akurasi deteksi pada threshold IoU 0.50. |
| `mAP50-95` | Rata-rata akurasi pada beberapa threshold IoU dari 0.50 sampai 0.95. |
| `Precision` | Seberapa banyak prediksi model yang benar dari seluruh prediksi yang dibuat. |
| `Recall` | Seberapa banyak objek sebenarnya yang berhasil ditemukan model. |

Evaluasi juga dapat dijalankan manual dengan:

```bash
python eval.py
```

Model yang digunakan pada `eval.py` berada pada path:

```text
runs\detect\runs\train\kaganga_v1-4\weights\best.pt
```

## Prediksi Gambar

Prediksi dijalankan melalui:

```bash
python predict.py
```

Konfigurasi utama prediksi berada di `predict.py`:

| Parameter | Nilai default | Keterangan |
| --- | --- | --- |
| `MODEL_PATH` | `runs\detect\runs\train\kaganga_v1\weights\best.pt` | Path model yang digunakan untuk prediksi. |
| `SOURCE` | `datasets/test/images` | Sumber gambar, bisa berupa satu gambar, folder, atau `0` untuk webcam. |
| `CONF` | `0.25` | Confidence threshold minimum. |
| `IOU` | `0.45` | IoU threshold untuk Non-Maximum Suppression. |
| `IMG_SIZE` | `416` | Ukuran gambar saat inference. |
| `SAVE_DIR` | `runs/predict` | Folder penyimpanan hasil prediksi. |

Output prediksi meliputi:

| Output | Keterangan |
| --- | --- |
| Gambar hasil deteksi | Gambar dengan bounding box, label kelas, dan confidence. |
| Label `.txt` | Hasil deteksi dalam format teks. |
| Confidence | Nilai keyakinan model untuk setiap prediksi. |
| Ringkasan terminal | Jumlah aksara terdeteksi pada setiap gambar. |
| Urutan aksara | Aksara diurutkan dari kiri ke kanan berdasarkan posisi bounding box. |

Hasil prediksi disimpan pada folder:

```text
runs/predict/hasil/
```

Pada repo saat ini juga terdapat hasil prediksi di:

```text
runs/detect/runs/predict/hasil/
```

## Prediksi Satu Gambar

File `cek.py` berisi contoh penggunaan fungsi `predict_single()` dari `predict.py`.

Jalankan:

```bash
python cek.py
```

Contoh konsep penggunaannya:

```python
from predict import predict_single

hasil = predict_single(r"datasets\test\images\3_jpg.rf.09612c2902eaf8ac9193bff9abd81b3c.jpg")
print("Aksara terdeteksi:", hasil)
```

Fungsi `predict_single()` akan mengembalikan list nama kelas aksara yang terdeteksi, sudah diurutkan dari kiri ke kanan.

## Hasil Training dan Artefak Output

Hasil training YOLOv8 biasanya tersimpan di folder eksperimen dalam `runs/`. Pada project ini ditemukan output training seperti:

```text
runs/detect/runs/train/kaganga_v1/
runs/detect/runs/train/kaganga_v1-4/
```

Artefak penting yang dihasilkan:

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

Berdasarkan `results.csv` yang tersimpan, metrik training dan validasi dapat dianalisis per epoch. File ini menjadi ringkasan numerik untuk melihat perkembangan performa model selama proses pelatihan.

## Lokasi Model

Model hasil training tersimpan sebagai file bobot PyTorch dengan ekstensi `.pt`. File utama yang digunakan untuk evaluasi dan prediksi adalah `best.pt`, yaitu model terbaik dari proses validasi.

```text
runs\detect\runs\train\kaganga_v1\weights\best.pt
runs\detect\runs\train\kaganga_v1-4\weights\best.pt
```

Pada `predict.py`, model dipanggil melalui variabel `MODEL_PATH`:

```python
MODEL_PATH = r"runs\detect\runs\train\kaganga_v1-4\weights\best.pt"
```

## Ringkasan Command

```bash
# Install dependency
pip install ultralytics

# Training model
python train.py

# Evaluasi model
python eval.py

# Prediksi folder/gambar
python predict.py

# Cek prediksi satu gambar
python cek.py
```

## Kesimpulan

Project ini membangun pipeline deteksi Aksara Kaganga/Ulu Rejang menggunakan YOLOv8, mulai dari dataset berformat YOLO, proses training, evaluasi performa, sampai prediksi gambar baru. Dengan 253 kelas aksara/suku kata dan struktur dataset train-validation-test, project ini merepresentasikan alur kerja lengkap sistem pengenalan aksara daerah berbasis computer vision.
