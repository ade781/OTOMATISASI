# 📦 Sistem Otomatisasi Permohonan Informasi Publik

## Apa ini? (What is this?)

Sistem otomatisasi untuk mengirimkan permohonan informasi publik secara batch ke berbagai instansi pemerintah Indonesia melalui email. Aplikasi ini dibangun menggunakan Streamlit dan memudahkan proses pengiriman request informasi ke PPID (Pejabat Pengelola Data dan Informasi) berbagai badan publik.

## Fitur Utama

- ✉️ **Pengiriman Email Batch**: Mengirim permohonan informasi ke banyak instansi sekaligus
- 📊 **Manajemen Data**: Mengelola data penerima dalam format Excel (XLSX)
- 📎 **Lampiran Otomatis**: Melampirkan file KTP secara otomatis ke setiap email
- 📥 **Cek Balasan**: Memantau balasan email dari instansi pemerintah
- 🔄 **Status Tracking**: Melacak status pengiriman untuk setiap instansi
- ⏱️ **Rate Limiting**: Mengatur limit harian pengiriman email

## Struktur Proyek

```
OTOMATISASI/
├── main.py              # File utama aplikasi Streamlit
├── modules/             # Modul-modul pendukung
│   ├── __init__.py
│   ├── database.py      # Fungsi untuk load/save data Excel
│   └── mailer.py        # Fungsi untuk kirim/terima email
├── data.xlsx            # File data instansi penerima
├── ktp.pdf              # File KTP yang akan dilampirkan
└── requirements.txt     # Dependensi Python
```

## Persyaratan Sistem

- Python 3.7 atau lebih baru
- Akun Gmail dengan App Password aktif
- Akses internet

## Instalasi

1. **Clone repository** (jika belum):
   ```bash
   git clone <repository-url>
   cd OTOMATISASI
   ```

2. **Install dependensi**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Persiapkan file data**:
   - Pastikan file `data.xlsx` ada dengan kolom minimal:
     - `Nama Badan Publik`: Nama instansi penerima
     - `Email`: Alamat email instansi
     - `Pertanyaan`: Permohonan informasi yang diajukan
     - `Status`: (opsional, akan dibuat otomatis)

4. **Persiapkan file KTP**:
   - Simpan file KTP Anda sebagai `ktp.pdf` di folder utama

## Cara Menggunakan

### 1. Menjalankan Aplikasi

```bash
streamlit run main.py
```

Aplikasi akan terbuka di browser pada `http://localhost:8501`

### 2. Konfigurasi Email

Di sidebar, masukkan:
- **Email Gmail**: Alamat Gmail Anda
- **App Password**: Password aplikasi Gmail (bukan password biasa!)
- **Nama Pengirim**: Nama Anda
- **Tujuan Request**: Tujuan permohonan (contoh: "Tugas Akhir", "Penelitian")

### 3. Mengirim Email Batch

1. Buka tab **"🚀 KIRIM BATCH"**
2. Lihat statistik data yang ada
3. Atur **Limit Harian** sesuai kebutuhan (disarankan 10-20 per hari)
4. Klik tombol **"MULAI KIRIM"**
5. Pantau progress pengiriman

### 4. Cek Balasan Email

1. Buka tab **"📩 CEK BALASAN"**
2. Pastikan IMAP sudah diaktifkan di Gmail (lihat Troubleshooting)
3. Klik tombol **"🔄 Cek Inbox Sekarang"**
4. Lihat email balasan yang masuk

## Format Data Excel

File `data.xlsx` harus memiliki kolom berikut:

| Nama Badan Publik | Email | Pertanyaan | Status |
|-------------------|-------|------------|--------|
| Dinas Pendidikan | ppid@disdik.go.id | Permohonan data jumlah siswa tahun 2024 | (akan terisi otomatis) |
| Dinas Kesehatan | info@dinkes.go.id | Permohonan data faskes terdaftar | (akan terisi otomatis) |

**Catatan**: Kolom `Status` akan dibuat dan diisi otomatis oleh sistem.

## Cara Mendapatkan App Password Gmail

1. Buka [Akun Google](https://myaccount.google.com/)
2. Pilih **Security** → **2-Step Verification** (harus diaktifkan dulu)
3. Scroll ke bawah, pilih **App passwords**
4. Buat password baru untuk aplikasi "Mail" pada device "Other"
5. Copy password 16 karakter yang diberikan
6. Gunakan password tersebut di aplikasi ini (BUKAN password Gmail biasa!)

## Troubleshooting

### Error: "Login dulu di Sidebar!"
**Solusi**: Pastikan sudah mengisi Email Gmail dan App Password di sidebar.

### Error: "File KTP tidak ditemukan!"
**Solusi**: Pastikan file `ktp.pdf` ada di folder yang sama dengan `main.py`.

### Error IMAP saat cek inbox
**Solusi**: 
1. Buka [Gmail Settings](https://mail.google.com/mail/u/0/#settings/fwdandpop)
2. Pilih tab **"Forwarding and POP/IMAP"**
3. Aktifkan **"Enable IMAP"**
4. Klik **"Save Changes"**

### Email tidak terkirim / Error SMTP
**Kemungkinan penyebab**:
- App Password salah atau belum dibuat
- 2-Step Verification belum diaktifkan di Gmail
- Koneksi internet bermasalah
- Gmail membatasi pengiriman (terlalu banyak email dalam waktu singkat)

### Status tidak tersimpan
**Solusi**: Pastikan file `data.xlsx` tidak sedang dibuka di program lain (Excel, LibreOffice, dll)

## Catatan Penting

⚠️ **Batasan Pengiriman Gmail**: 
- Gmail membatasi pengiriman sekitar 500 email/hari untuk akun biasa
- Disarankan mengirim maksimal 20-50 email per batch
- Beri jeda antar batch untuk menghindari pembatasan

⚠️ **Keamanan**:
- JANGAN share App Password Anda ke siapapun
- JANGAN commit App Password ke repository
- Gunakan App Password, bukan password Gmail biasa

⚠️ **Legal**:
- Pastikan permohonan informasi Anda sesuai dengan UU Keterbukaan Informasi Publik
- Gunakan aplikasi ini dengan bijak dan bertanggung jawab

## Teknologi yang Digunakan

- **[Streamlit](https://streamlit.io/)**: Framework untuk web app
- **[Pandas](https://pandas.pydata.org/)**: Manipulasi data Excel
- **smtplib**: Pengiriman email via SMTP
- **imaplib**: Pembacaan email via IMAP

## Lisensi

Proyek ini dibuat untuk keperluan pendidikan dan penelitian.

## Kontribusi

Kontribusi sangat diterima! Silakan buat pull request atau issue untuk perbaikan dan penambahan fitur.

## Kontak

Jika ada pertanyaan atau masalah, silakan buat issue di repository ini.

---

**Dibuat dengan ❤️ untuk mempermudah akses informasi publik di Indonesia**
