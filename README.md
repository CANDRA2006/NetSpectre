# NetSpectre

## Deskripsi

NetSpectre merupakan perangkat lunak pemindaian port (*port scanner*) berbasis Python yang dirancang untuk kebutuhan pembelajaran, penelitian keamanan jaringan, serta pengujian keamanan yang sah (*authorized security testing*). Perangkat lunak ini dikembangkan sebagai implementasi praktis dari konsep-konsep keamanan jaringan yang mencakup deteksi layanan, analisis risiko, serta validasi hasil pemindaian secara komparatif.

Aplikasi ini mengimplementasikan pendekatan *multithreading* untuk meningkatkan efisiensi pemindaian secara konkuren, serta menyediakan mekanisme validasi hasil menggunakan Nmap sebagai instrumen pembanding eksternal. Dengan demikian, NetSpectre dapat digunakan sebagai sarana verifikasi independen terhadap keakuratan hasil pemindaian port secara mandiri.

NetSpectre dikembangkan dengan arsitektur modular guna mendukung pengembangan lebih lanjut, pemeliharaan kode yang sistematis, serta kemudahan ekstensibilitas fungsional di masa mendatang.

---

## Fitur Utama

- Pemindaian port TCP berbasis *multithreading* dengan kontrol konkurensi adaptif
- Indikator progres pemindaian secara langsung (*live progress indicator*)
- Identifikasi layanan (*service fingerprinting*) berdasarkan nomor port dan analisis *banner*
- Deteksi sistem operasi berbasis heuristik sederhana (analisis TTL dan port terbuka)
- Sistem penilaian risiko (*risk scoring engine*) dengan klasifikasi tingkat keparahan
- Mode validasi menggunakan Nmap sebagai pembanding eksternal
- Perbandingan hasil pemindaian internal dengan output Nmap secara terstruktur
- Deteksi anomali jaringan berdasarkan jumlah dan jenis layanan yang terekspos
- Pemantauan laju pemindaian (*scan rate monitoring*) berbasis satuan waktu
- Pembuatan laporan dalam format JSON dan HTML dengan *timestamp* otomatis

---

## Struktur Proyek

```
NetSpectre/
│
├── main.py                     # Titik masuk utama aplikasi
├── requirements.txt            # Daftar dependensi Python
├── setup.py                    # Skrip instalasi paket
├── config.yaml                 # Berkas konfigurasi utama
├── LICENSE                     # Lisensi perangkat lunak
├── .gitignore                  # Pengecualian berkas Git
├── README.md                   # Dokumentasi utama proyek
├── netspectre.log              # Berkas log aktivitas pemindaian
├── .env                        # Variabel lingkungan (tidak dikomit)
│
├── core/                       # Modul inti pemindaian
│   ├── __init__.py
│   ├── port_scanner.py         # Mesin pemindaian port TCP multithreaded
│   ├── host_discovery.py       # Penemuan host aktif dalam jaringan
│   ├── banner_grabber.py       # Pengambil banner layanan
│   ├── service_fingerprint.py  # Identifikasi layanan berdasarkan port dan banner
│   ├── ttl_fingerprint.py      # Estimasi OS berbasis nilai TTL
│   ├── detector.py             # Deteksi OS berbasis port terbuka
│   ├── risk_engine.py          # Mesin penilaian dan klasifikasi risiko
│   └── reporter.py             # Generator laporan JSON dan HTML
│
├── detection/                  # Modul deteksi dan pemantauan
│   ├── __init__.py
│   ├── anomaly_detector.py     # Deteksi anomali berdasarkan profil port
│   └── rate_monitor.py         # Pemantauan laju pemindaian
│
├── utils/                      # Utilitas pendukung
│   ├── __init__.py
│   ├── logger.py               # Sistem pencatatan log
│   ├── output_formatter.py     # Pemformat keluaran konsol
│   ├── config_loader.py        # Pemuat konfigurasi YAML
│   └── helpers.py              # Fungsi-fungsi pembantu umum
│
|── reports/                    # Folder laporan (tidak dicommit disini)
|
├── wordlist/                   # Basis data referensi
│   └── common_ports.txt        # Daftar port umum yang sering dipindai
│
├── tests/                      # Pengujian unit dan integrasi
│   ├── test_scanner.py         # Pengujian modul pemindai port
│   ├── test_discovery.py       # Pengujian modul penemuan host
│   └── test_risk_engine.py     # Pengujian mesin penilaian risiko
│
└── docs/                       # Dokumentasi teknis
    ├── architecture.md         # Dokumentasi arsitektur sistem
    └── usage.md                # Panduan penggunaan aplikasi
```

---

## Prasyarat Sistem

Sebelum menjalankan NetSpectre, pastikan sistem telah memenuhi persyaratan berikut:

- Python 3.8 atau versi yang lebih baru
- pip (manajer paket Python)
- Nmap (opsional, diperlukan untuk mode validasi `--use-nmap`)
- Hak akses administrator/root (direkomendasikan untuk pemindaian SYN via Nmap)

---

## Instalasi

### 1. Kloning Repositori

```bash
git clone https://github.com/username/NetSpectre.git
cd NetSpectre
```

### 2. Instalasi Dependensi

```bash
pip install -r requirements.txt
```

### 3. Verifikasi Instalasi

```bash
python main.py --help
```

---

## Penggunaan Cepat

```bash
# Pemindaian dasar pada rentang port standar
python main.py --target 192.168.1.1 --ports 1-1024

# Pemindaian dengan validasi Nmap
python main.py --target 192.168.1.1 --ports 1-1024 --use-nmap
```

Untuk panduan penggunaan lengkap, silakan merujuk pada dokumen [`docs/usage.md`](docs/usage.md).

---

## Konfigurasi

Konfigurasi aplikasi dikelola melalui berkas `config.yaml`:

```yaml
max_threads: 100        # Jumlah maksimum thread konkuren
default_timeout: 0.5    # Batas waktu koneksi per port (dalam detik)
```

Parameter-parameter ini dapat disesuaikan berdasarkan kapasitas sistem dan kondisi jaringan target.

---

## Peringatan dan Etika Penggunaan

> **PERINGATAN:** NetSpectre dirancang **hanya** untuk digunakan pada sistem dan jaringan yang dimiliki sendiri atau yang telah mendapatkan izin eksplisit dari pemilik atau administrator yang berwenang.

---

## Lisensi

Proyek ini dilisensikan di bawah ketentuan yang tercantum dalam berkas [LICENSE](LICENSE). Silakan membaca lisensi tersebut sebelum menggunakan atau mendistribusikan ulang perangkat lunak ini.

---

## Kontribusi

Kontribusi terhadap pengembangan NetSpectre sangat dipersilakan. Untuk berkontribusi, lakukan *fork* repositori ini, buat *branch* fitur baru, dan ajukan *pull request* dengan deskripsi perubahan yang jelas dan terperinci. Pastikan setiap perubahan disertai dengan pengujian unit yang memadai.

## AUTHOR
CANDRA
