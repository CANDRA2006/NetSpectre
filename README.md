# NetSpectre

## Deskripsi

NetSpectre merupakan perangkat lunak pemindaian port (*port scanner*) berbasis Python yang dirancang untuk kebutuhan pembelajaran, penelitian keamanan jaringan, serta pengujian keamanan yang sah (*authorized security testing*).

Aplikasi ini mengimplementasikan pendekatan multithreading untuk meningkatkan efisiensi pemindaian serta menyediakan mekanisme validasi hasil menggunakan Nmap sebagai pembanding.

NetSpectre dikembangkan dengan arsitektur modular guna mendukung pengembangan lebih lanjut dan pemeliharaan kode yang sistematis.

---

## Fitur Utama

- Pemindaian port TCP berbasis multithreading  
- Indikator progres pemindaian secara langsung (*live progress*)  
- Identifikasi layanan (*service fingerprinting*)  
- Deteksi sistem operasi berbasis heuristik sederhana  
- Sistem penilaian risiko (*risk scoring engine*)  
- Mode validasi menggunakan Nmap  
- Perbandingan hasil pemindaian internal dengan Nmap  
- Pembuatan laporan dalam format JSON dan HTML  
- Penyimpanan laporan dengan timestamp otomatis  

---

## Struktur Proyek
```
NetSpectre/
│
├── main.py
├── requirements.txt
├── setup.py
├── config.yaml
├── LICENSE
├── .gitignore
├── README.md
├──.env
├── core/
│   ├── __init__.py
│   ├── port_scanner.py
│   ├── host_discovery.py
│   ├── banner_grabber.py
│   ├── ttl_fingerprint.py
│   └── risk_engine.py
│
├── detection/
│   ├── __init__.py
│   ├── anomaly_detector.py
│   └── rate_monitor.py
│
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   ├── output_formatter.py
│   ├── config_loader.py
│   └── helpers.py
│
├── reports/
│   ├── html_report.py
│   └── json_report.py
│
├── wordlists/
│   └── common_ports.txt
│
├── tests/
│   ├── test_scanner.py
│   ├── test_discovery.py
│   └── test_risk_engine.py
│
└── docs/
    ├── architecture.md
    └── usage.md

