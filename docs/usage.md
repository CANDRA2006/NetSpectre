# Panduan Penggunaan NetSpectre

## 1. Pendahuluan

Dokumen ini menyajikan panduan penggunaan perangkat lunak NetSpectre secara komprehensif, mulai dari proses instalasi hingga interpretasi hasil pemindaian. Panduan ini ditujukan bagi pengguna dengan latar belakang teknis di bidang keamanan jaringan maupun bagi pelajar yang sedang mempelajari konsep-konsep dasar pemindaian port dan analisis keamanan jaringan.

> **Perhatian:** Seluruh aktivitas pemindaian yang dilakukan menggunakan NetSpectre harus mendapatkan otorisasi eksplisit dari pemilik atau administrator jaringan yang bersangkutan. Penggunaan tanpa izin merupakan pelanggaran hukum yang dapat dikenai sanksi pidana.

---

## 2. Prasyarat Instalasi

Sebelum memulai instalasi, pastikan lingkungan sistem telah memenuhi persyaratan berikut:

| Komponen | Versi Minimum | Keterangan |
|:--------:|:-------------:|:----------:|
| Python   | 3.8           | Wajib      |
| pip      | 21.0          | Wajib      |
| Nmap     | 7.0           | Opsional (untuk mode `--use-nmap`) |
| Hak Akses | Administrator/root | Direkomendasikan untuk pemindaian SYN |

---

## 3. Instalasi

### 3.1 Mengunduh Kode Sumber

Unduh repositori NetSpectre menggunakan Git:

```bash
git clone https://github.com/candra2006/NetSpectre.git
cd NetSpectre
```

Atau unduh arsip ZIP dari halaman rilis dan ekstrak ke direktori yang diinginkan.

### 3.2 Instalasi Dependensi Python

Instal seluruh pustaka Python yang diperlukan menggunakan perintah berikut:

```bash
pip install -r requirements.txt
```

Dependensi yang akan diinstal mencakup:

- **colorama** — Dukungan pewarnaan teks pada antarmuka konsol lintas platform
- **pyyaml** — Parser berkas konfigurasi berformat YAML
- **rich** — Pustaka pemformatan keluaran konsol yang lebih kaya

### 3.3 Konfigurasi Awal

Salin berkas konfigurasi contoh dan sesuaikan parameternya:

```bash
# Berkas config.yaml sudah tersedia, sesuaikan jika diperlukan
nano config.yaml
```

Parameter konfigurasi yang tersedia:

```yaml
max_threads: 100        # Jumlah thread maksimum untuk konkurensi pemindaian
default_timeout: 0.5    # Batas waktu koneksi per port (dalam detik)
```

### 3.4 Verifikasi Instalasi

Verifikasi keberhasilan instalasi dengan menampilkan bantuan penggunaan:

```bash
python main.py --help
```

Keluaran yang diharapkan:

```
usage: main.py [-h] --target TARGET [--ports PORTS] [--use-nmap]

NetSpectre - Advanced Port Scanner

options:
  -h, --help       show this help message and exit
  --target TARGET  Target IP or hostname
  --ports PORTS    Port range (e.g. 1-1000)
  --use-nmap       Enable Nmap fallback mode
```

---

## 4. Sintaksis Perintah

Sintaksis umum penggunaan NetSpectre adalah sebagai berikut:

```bash
python main.py --target <TARGET> [--ports <PORT_RANGE>] [--use-nmap]
```

### 4.1 Deskripsi Argumen

| Argumen | Tipe | Wajib | Nilai Default | Deskripsi |
|:-------:|:----:|:-----:|:-------------:|:---------:|
| `--target` | String | Ya | — | Alamat IP atau nama host target pemindaian |
| `--ports` | String | Tidak | `1-1024` | Rentang port yang akan dipindai dalam format `<awal>-<akhir>` |
| `--use-nmap` | Flag | Tidak | Nonaktif | Mengaktifkan mode validasi dan perbandingan dengan Nmap |

---

## 5. Contoh Penggunaan

### 5.1 Pemindaian Dasar

Melakukan pemindaian port standar (1–1024) pada sebuah alamat IP target:

```bash
python main.py --target 192.168.1.1
```

### 5.2 Pemindaian dengan Rentang Port Kustom

Menentukan rentang port yang lebih luas untuk cakupan pemindaian yang lebih komprehensif:

```bash
python main.py --target 192.168.1.1 --ports 1-65535
```

### 5.3 Pemindaian Port Spesifik

Memfokuskan pemindaian pada rentang port layanan web yang umum:

```bash
python main.py --target 192.168.1.100 --ports 80-443
```

### 5.4 Pemindaian dengan Validasi Nmap

Menjalankan pemindaian internal sekaligus melakukan validasi menggunakan Nmap sebagai instrumen pembanding:

```bash
python main.py --target 192.168.1.1 --ports 1-1024 --use-nmap
```

### 5.5 Pemindaian pada Nama Host

NetSpectre juga mendukung penggunaan nama host (*hostname*) sebagai target:

```bash
python main.py --target example.local --ports 1-1024
```

---

## 6. Interpretasi Keluaran

### 6.1 Keluaran Konsol

Selama proses pemindaian berlangsung, NetSpectre menampilkan informasi berikut pada konsol:

```
[+] Target: 192.168.1.1
[+] Port Range: 1-1024
[+] Using 100 threads
[+] Scanning ports...
Progress: 100.00%
[+] Scan complete.

[+] Scan Summary
    Open Ports (Internal): [22, 80, 443, 3306]
    OS Guess: Linux/Unix (Likely)
    Risk Score: {'score': 9, 'severity': 'Medium', 'exposed_ports': 4}
    Scan Time: 12.34 sec
[+] Reports generated successfully.
```

### 6.2 Interpretasi Skor Risiko

Sistem penilaian risiko NetSpectre menghasilkan nilai skor kumulatif berdasarkan bobot masing-masing port yang terbuka. Klasifikasi tingkat risiko adalah sebagai berikut:

| Tingkat Risiko | Rentang Skor | Rekomendasi Tindakan |
|:--------------:|:------------:|:--------------------:|
| **Rendah** | 0 – 5 | Pemantauan rutin yang berkelanjutan |
| **Sedang** | 6 – 15 | Evaluasi kebijakan keamanan dan pembatasan akses |
| **Tinggi** | > 15 | Tindakan mitigasi segera dan audit keamanan menyeluruh |

### 6.3 Deteksi Anomali

Kondisi-kondisi berikut akan ditandai sebagai anomali oleh sistem:

- Jumlah layanan terbuka melebihi 30 port
- Keberadaan layanan Telnet (port 23) yang tidak terenkripsi
- Keberadaan layanan RDP (port 3389) yang terekspos
- Keberadaan layanan FTP (port 21) yang tidak terenkripsi

### 6.4 Berkas Laporan

Setelah pemindaian selesai, NetSpectre secara otomatis menghasilkan dua berkas laporan yang disimpan di direktori `reports/`:

#### 6.4.1 Laporan JSON (`reports/report_YYYYMMDD_HHMMSS.json`)

```json
{
    "target": "192.168.1.1",
    "internal_scan": {
        "open_ports": [22, 80, 443, 3306],
        "services": {
            "22": "SSH",
            "80": "HTTP",
            "443": "HTTPS",
            "3306": "MySQL"
        },
        "os_guess": "Linux/Unix (Likely)",
        "risk_score": {
            "score": 9,
            "severity": "Medium",
            "exposed_ports": 4
        }
    },
    "nmap_scan": {
        "open_ports": [],
        "services": {}
    },
    "scan_time": 12.34
}
```

#### 6.4.2 Laporan HTML (`reports/report_YYYYMMDD_HHMMSS.html`)

Berkas HTML dapat dibuka langsung menggunakan peramban web dan menampilkan seluruh data hasil pemindaian dalam format yang terstruktur dan mudah dibaca secara visual.

---

## 7. Konfigurasi Lanjutan

### 7.1 Optimasi Performa

Untuk meningkatkan kecepatan pemindaian, nilai `max_threads` dapat ditingkatkan dalam berkas `config.yaml`. Namun, perlu diperhatikan bahwa nilai yang terlalu tinggi dapat:

- Memicu sistem deteksi intrusi (*Intrusion Detection System* / IDS) pada jaringan target
- Menyebabkan kelelahan sumber daya pada sistem pemindai
- Mengakibatkan penurunan akurasi hasil akibat beban sistem yang berlebih

Rekomendasi nilai `max_threads` berdasarkan skenario penggunaan:

| Skenario | Nilai Rekomendasi |
|:--------:|:-----------------:|
| Jaringan lokal dengan kontrol penuh | 100 – 500 |
| Pengujian terhadap sistem eksternal | 50 – 100 |
| Pemindaian stealthy / low-profile | 10 – 20 |

### 7.2 Penyesuaian Timeout

Nilai `default_timeout` menentukan durasi menunggu respons dari setiap port. Panduan penyesuaian:

- **Jaringan lokal dengan latensi rendah:** 0.3 – 0.5 detik
- **Jaringan WAN dengan latensi menengah:** 1.0 – 2.0 detik
- **Jaringan dengan latensi tinggi:** 3.0 – 5.0 detik

---

## 8. Pemecahan Masalah

### 8.1 Nmap Tidak Ditemukan

```
[!] Nmap not found in system PATH.
```

**Solusi:** Instal Nmap dari situs resmi (https://nmap.org) dan pastikan direktori instalasi Nmap telah ditambahkan ke variabel lingkungan `PATH` sistem operasi.

### 8.2 Izin Akses Tidak Mencukupi

Jika pemindaian menggunakan mode Nmap dengan flag `-sS` (SYN scan) gagal, hal ini biasanya disebabkan oleh kurangnya hak akses.

**Solusi (Linux/macOS):**

```bash
sudo python main.py --target 192.168.1.1 --use-nmap
```

### 8.3 Laju Pemindaian Sangat Lambat

Jika pemindaian memerlukan waktu yang terlalu lama, pertimbangkan langkah-langkah berikut:

1. Kurangi rentang port yang dipindai
2. Tingkatkan nilai `max_threads` dalam `config.yaml`
3. Kurangi nilai `default_timeout` jika jaringan target memiliki latensi rendah

### 8.4 Banyak False Negative (Port Terbuka Tidak Terdeteksi)

Jika NetSpectre tidak mendeteksi port yang seharusnya terbuka, kemungkinan penyebabnya adalah:

1. Nilai `default_timeout` terlalu rendah — tingkatkan ke 1.0 atau lebih
2. Firewall melakukan *rate limiting* terhadap koneksi masuk — kurangi nilai `max_threads`
3. Port memerlukan protokol handshake khusus yang tidak didukung oleh TCP Connect scan

---

## 9. Catatan Keamanan dan Etika

Penggunaan NetSpectre harus selalu memperhatikan aspek-aspek etika dan legalitas berikut:

1. **Otorisasi Tertulis:** Pastikan selalu memiliki izin tertulis dari pemilik atau administrator sistem sebelum melakukan pemindaian
2. **Lingkup yang Jelas:** Batasi pemindaian hanya pada alamat IP atau rentang jaringan yang secara eksplisit disebutkan dalam perjanjian pengujian (*Rules of Engagement*)
3. **Dokumentasi:** Catat seluruh aktivitas pemindaian beserta konteks dan tujuannya untuk keperluan audit dan pertanggungjawaban
4. **Pengungkapan Bertanggung Jawab:** Jika menemukan kerentanan selama pengujian yang sah, ikuti prosedur *responsible disclosure* yang berlaku
5. **Kerahasiaan Data:** Jaga kerahasiaan data hasil pemindaian dan hindari penyebarannya kepada pihak yang tidak berkepentingan

---

## 10. Referensi

- Gordon, L., & Loeb, M. (2002). *The economics of information security investment*. ACM Transactions on Information and System Security, 5(4), 438–457.
- Nmap Network Scanning Documentation: https://nmap.org/book/
- Python `socket` Module Documentation: https://docs.python.org/3/library/socket.html
- Python `concurrent.futures` Documentation: https://docs.python.org/3/library/concurrent.futures.html
- OWASP Testing Guide v4.2: https://owasp.org/www-project-web-security-testing-guide/
