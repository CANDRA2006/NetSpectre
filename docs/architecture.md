# Arsitektur Sistem NetSpectre

## 1. Pendahuluan

Dokumen ini memaparkan arsitektur teknis perangkat lunak NetSpectre secara komprehensif, mencakup desain modular, alur pemrosesan data, serta hubungan antarkomponen sistem. Pemahaman terhadap arsitektur ini merupakan prasyarat penting bagi pengembang yang ingin berkontribusi, memperluas fungsionalitas, atau melakukan pemeliharaan terhadap basis kode (*codebase*) yang ada.

NetSpectre dirancang dengan menerapkan prinsip *Separation of Concerns* (SoC), di mana setiap komponen sistem memiliki tanggung jawab yang terdefinisi secara jelas dan terisolasi dari komponen lainnya. Pendekatan ini bertujuan untuk meningkatkan kemudahan pemeliharaan (*maintainability*), kemampuan pengujian (*testability*), serta fleksibilitas pengembangan lebih lanjut.

---

## 2. Gambaran Umum Arsitektur

NetSpectre menggunakan pola arsitektur **layered architecture** (arsitektur berlapis) yang terdiri atas empat lapisan utama:

```
┌─────────────────────────────────────────┐
│           Lapisan Antarmuka             │
│              (main.py)                  │
├─────────────────────────────────────────┤
│            Lapisan Inti                 │
│    (core/, detection/)                  │
├─────────────────────────────────────────┤
│           Lapisan Utilitas              │
│              (utils/)                   │
├─────────────────────────────────────────┤
│           Lapisan Keluaran              │
│    (reports/, logs, console)            │
└─────────────────────────────────────────┘
```

Setiap lapisan hanya berkomunikasi dengan lapisan di bawahnya secara langsung, sehingga menciptakan hierarki dependensi yang bersih dan terstruktur.

---

## 3. Komponen Utama

### 3.1 Titik Masuk Aplikasi (`main.py`)

Modul `main.py` berfungsi sebagai pengendali alur utama (*main controller*) aplikasi. Modul ini bertanggung jawab untuk:

- Menguraikan argumen baris perintah (*command-line argument parsing*) menggunakan pustaka `argparse`
- Mengorkestrasi urutan eksekusi antar modul inti
- Menggabungkan hasil dari pemindaian internal dan eksternal (Nmap)
- Memicu proses pembuatan laporan akhir

Modul ini tidak mengimplementasikan logika bisnis secara langsung, melainkan mendelegasikan setiap tugas spesifik kepada modul yang bersesuaian.

### 3.2 Lapisan Inti (`core/`)

Lapisan ini merupakan inti fungsional dari NetSpectre yang terdiri atas beberapa submodul:

#### 3.2.1 `port_scanner.py` — Mesin Pemindaian Port

Modul ini mengimplementasikan kelas `PortScanner` yang menjadi komponen sentral dalam proses pemindaian. Karakteristik teknisnya meliputi:

- **Mekanisme Konkurensi:** Menggunakan `concurrent.futures.ThreadPoolExecutor` untuk mengelola kumpulan thread (*thread pool*) secara efisien
- **Pemindaian TCP Connect:** Mengandalkan metode `socket.connect_ex()` untuk menentukan status port (terbuka/tertutup) tanpa memerlukan hak akses khusus
- **Pemantauan Progres:** Mengimplementasikan pelaporan progres berbasis persentase secara *real-time* ke antarmuka konsol
- **Konfigurabilitas:** Parameter thread dan *timeout* diambil dari berkas konfigurasi melalui `config_loader`

**Kompleksitas Waktu:** O(n/t) di mana n adalah jumlah port yang dipindai dan t adalah jumlah thread aktif.

#### 3.2.2 `host_discovery.py` — Penemuan Host Jaringan

Modul ini menyediakan fungsionalitas penemuan host aktif dalam suatu segmen jaringan dengan cara:

- Menerima masukan berupa notasi CIDR (Classless Inter-Domain Routing)
- Melakukan iterasi terhadap seluruh alamat IP host dalam rentang jaringan yang ditentukan
- Mengeksekusi perintah `ping` secara sekuensial untuk setiap alamat IP
- Mendukung kompatibilitas lintas platform (Windows dan Linux/Unix) melalui deteksi sistem operasi dinamis

#### 3.2.3 `banner_grabber.py` — Pengambil Banner Layanan

Modul ini mengimplementasikan teknik *banner grabbing* dengan mengirimkan permintaan HTTP HEAD ke port target, kemudian membaca respons yang dikembalikan oleh layanan yang berjalan. Data banner yang berhasil diperoleh selanjutnya digunakan sebagai masukan bagi modul identifikasi layanan.

#### 3.2.4 `service_fingerprint.py` — Identifikasi Layanan

Modul ini melakukan identifikasi layanan yang berjalan pada port tertentu menggunakan dua mekanisme:

1. **Pemetaan Statis:** Pencocokan langsung berdasarkan basis data port-layanan yang telah didefinisikan (mis. port 22 → SSH, port 80 → HTTP)
2. **Analisis Banner:** Pencarian kata kunci (*keyword matching*) pada string banner untuk mengidentifikasi perangkat lunak server yang spesifik (mis. Apache, Nginx, OpenSSH)

#### 3.2.5 `ttl_fingerprint.py` — Estimasi Sistem Operasi via TTL

Modul ini melakukan estimasi jenis sistem operasi target berdasarkan analisis nilai *Time-To-Live* (TTL) yang diperoleh dari respons ICMP. Dasar heuristik yang digunakan adalah:

| Rentang Nilai TTL | Estimasi Sistem Operasi |
|:-----------------:|:-----------------------:|
| ≤ 64              | Linux / Unix            |
| 65 – 128          | Microsoft Windows       |
| > 128             | Perangkat Jaringan      |

#### 3.2.6 `risk_engine.py` — Mesin Penilaian Risiko

Modul ini mengimplementasikan sistem skoring risiko berbasis pembobotan (*weighted scoring system*). Setiap port yang terbuka memiliki nilai bobot risiko yang mencerminkan potensi ancaman keamanannya:

| Port | Layanan | Bobot Risiko |
|:----:|:-------:|:------------:|
| 23   | Telnet  | 6            |
| 3389 | RDP     | 6            |
| 3306 | MySQL   | 5            |
| 21   | FTP     | 4            |
| 22   | SSH     | 2            |
| 80   | HTTP    | 1            |
| 443  | HTTPS   | 1            |
| Lainnya | —    | 1            |

Klasifikasi tingkat keparahan (*severity*) dilakukan berdasarkan akumulasi skor total:

- **Rendah (Low):** Skor ≤ 5
- **Sedang (Medium):** Skor 6 – 15
- **Tinggi (High):** Skor > 15

### 3.3 Lapisan Deteksi (`detection/`)

#### 3.3.1 `anomaly_detector.py` — Deteksi Anomali

Modul ini menganalisis profil port terbuka untuk mengidentifikasi kondisi anomali yang dapat mengindikasikan kerentanan keamanan, seperti keberadaan layanan Telnet, FTP, atau RDP yang terekspos ke publik, serta jumlah layanan terbuka yang melebihi ambang batas yang wajar.

#### 3.3.2 `rate_monitor.py` — Pemantauan Laju Pemindaian

Kelas `RateMonitor` mencatat waktu mulai pemindaian dan menghitung laju pemindaian (*scan rate*) dalam satuan port per detik, yang berguna untuk evaluasi performa dan optimasi konfigurasi thread.

### 3.4 Lapisan Utilitas (`utils/`)

#### 3.4.1 `config_loader.py` — Pemuat Konfigurasi

Modul ini memuat parameter konfigurasi dari berkas `config.yaml` menggunakan pustaka `PyYAML`. Jika berkas konfigurasi tidak ditemukan atau nilainya tidak valid, modul ini akan mengembalikan nilai *default* yang telah ditetapkan secara *hardcoded* sebagai mekanisme *fallback*.

#### 3.4.2 `logger.py` — Sistem Pencatatan Log

Modul ini mengonfigurasi sistem pencatatan log (*logging*) menggunakan modul bawaan Python (`logging`), dengan dua *handler* simultan: pencatatan ke berkas (`netspectre.log`) dan pencetakan ke konsol (*standard error*).

#### 3.4.3 `output_formatter.py` — Pemformat Keluaran

Modul ini menyediakan fungsi untuk memformat dan menampilkan ringkasan hasil pemindaian ke konsol dalam format yang terstruktur dan mudah dibaca.

### 3.5 Lapisan Pelaporan (`core/reporter.py`)

Modul `reporter.py` menyediakan dua fungsi generator laporan:

- **`generate_json_report()`:** Menghasilkan laporan terstruktur dalam format JSON yang dapat diproses lebih lanjut oleh sistem atau skrip otomatis lainnya
- **`generate_html_report()`:** Menghasilkan laporan visual berbasis HTML yang dapat dibuka langsung melalui peramban web (*web browser*)

Kedua format laporan disimpan dalam direktori `reports/` dengan penamaan berdasarkan *timestamp* untuk menghindari penimpaan berkas (*file overwrite*).

---

## 4. Alur Pemrosesan Data

Diagram berikut menggambarkan alur pemrosesan data dari masukan pengguna hingga keluaran laporan akhir:

```
Masukan Pengguna (CLI)
        │
        ▼
  Parsing Argumen (main.py)
        │
        ├──────────────────────────────────┐
        ▼                                  ▼
 Pemindaian Internal                Pemindaian Nmap (opsional)
 (PortScanner)                      (subprocess)
        │                                  │
        ▼                                  ▼
 Banner Grabbing              Parse Output JSON Nmap
 (banner_grabber)                          │
        │                                  │
        ▼                                  ▼
 Identifikasi Layanan         ◄── Komparasi Hasil ──►
 (service_fingerprint)
        │
        ├─────────────────────┐
        ▼                     ▼
 Estimasi OS            Penilaian Risiko
 (detector / ttl)       (risk_engine)
        │                     │
        └──────────┬──────────┘
                   ▼
          Deteksi Anomali
          (anomaly_detector)
                   │
                   ▼
         Perakitan Data Laporan
                   │
          ┌────────┴────────┐
          ▼                 ▼
   Laporan JSON       Laporan HTML
```

---

## 5. Pola Desain yang Diterapkan

NetSpectre mengadopsi beberapa pola desain (*design patterns*) yang umum digunakan dalam pengembangan perangkat lunak berorientasi objek:

- **Strategy Pattern:** Pemilihan metode pemindaian (internal vs. Nmap) berdasarkan argumen yang diberikan pengguna
- **Factory Pattern (implisit):** Pembuatan objek laporan (JSON/HTML) berdasarkan tipe keluaran yang diinginkan
- **Facade Pattern:** `main.py` berfungsi sebagai fasad yang menyederhanakan antarmuka terhadap subsistem yang kompleks
- **Template Method Pattern:** Struktur umum alur pemindaian yang konsisten dengan variasi pada tahap-tahap spesifik

---

## 6. Pertimbangan Performa

Performa NetSpectre sangat dipengaruhi oleh dua parameter konfigurasi utama:

- **`max_threads`:** Meningkatkan nilai ini dapat mempercepat pemindaian, namun berisiko memicu mekanisme *rate limiting* atau sistem deteksi intrusi (*IDS*) pada jaringan target. Nilai yang sangat tinggi juga dapat menyebabkan kelelahan sumber daya (*resource exhaustion*) pada sistem pemindai itu sendiri.
- **`default_timeout`:** Nilai *timeout* yang terlalu rendah dapat mengakibatkan kesalahan identifikasi (*false negatives*), di mana port yang sebenarnya terbuka dilaporkan sebagai tertutup akibat latensi jaringan yang tinggi.

Rekomendasi nilai optimal bergantung pada karakteristik jaringan dan sistem target.

---

## 7. Keterbatasan Teknis

Terdapat beberapa keterbatasan teknis yang perlu diperhatikan dalam penggunaan NetSpectre:

1. **Hanya mendukung TCP:** Implementasi saat ini tidak mencakup pemindaian protokol UDP maupun ICMP secara langsung
2. **Deteksi OS bersifat heuristik:** Estimasi sistem operasi tidak dijamin akurasinya karena bergantung pada perilaku jaringan yang dapat dimanipulasi
3. **Penemuan host bersifat sekuensial:** Modul `host_discovery.py` tidak menggunakan konkurensi, sehingga dapat menjadi *bottleneck* pada jaringan berukuran besar
4. **Banner grabbing terbatas:** Hanya mengirimkan permintaan HTTP HEAD, yang mungkin tidak efektif untuk layanan non-HTTP

---

## 8. Pengembangan Lebih Lanjut

Berdasarkan arsitektur modular yang telah ada, beberapa arah pengembangan yang direkomendasikan meliputi:

- Implementasi pemindaian UDP untuk cakupan yang lebih komprehensif
- Penambahan konkurensi pada modul penemuan host menggunakan `asyncio` atau `ThreadPoolExecutor`
- Integrasi basis data CVE (*Common Vulnerabilities and Exposures*) untuk korelasi kerentanan
- Pengembangan antarmuka pengguna grafis (*Graphical User Interface*) berbasis web
- Implementasi mekanisme *rate limiting* adaptif untuk menghindari deteksi oleh sistem IDS