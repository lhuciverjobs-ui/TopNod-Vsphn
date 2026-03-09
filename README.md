<div align="center">

<img src="silent_logo.png" width="220" alt="Silent Private Community"/>

# TopNod Auto Wallet Bot

**Dibuat dengan ❤️ untuk Silent Private Community**

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-VSPhone-orange?style=flat-square)](https://vsphone.com)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)]()

</div>

---

## ⚡ Instalasi Cepat

**1. Install dependency**

```bash
pip install -r requirements.txt
```

**2. Jalankan bot**

```bash
python main.py
```

Selesai. Bot akan tampil dengan banner dan berjalan secara interaktif.

---

## 🛠️ Sebelum Jalankan — Isi Konfigurasi

Buka `main.py`, cari bagian **KONFIGURASI** di baris paling atas, lalu sesuaikan:

```python
EMAIL        = "email_vsphone_kamu@gmail.com"
PASSWORD_MD5 = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"   # password di-hash MD5
REFERRAL_CODE   = "KODEREF123"   # referral code default
WALLET_PASSWORD = "password123"  # password wallet yang akan dibuat
EXCLUDE_DEVICES = {"PADCODE_DEVICE"}  # padCode device yang dikecualikan (kosongkan = semua ikut)
OTP_TIMEOUT     = 180            # maks detik tunggu OTP (default 3 menit)
```

> 💡 **Cara dapat PASSWORD_MD5** — jalankan di terminal:
> ```bash
> echo -n "passwordkamu" | md5sum
> ```
> Salin hasilnya (tanpa spasi dan tanda `-` di akhir) ke `PASSWORD_MD5`.

---

## 🚀 Panduan Langkah demi Langkah

### Saat script pertama kali jalan, kamu akan diminta:

---

### `[1]` Masukkan Referral Code

```
Referral code saat ini: ISIREF
Masukkan referral baru (kosong = pakai default): █
```

✏️ Ketik referral code yang ingin dipakai, lalu Enter.
Kosongkan dan Enter jika ingin pakai default.

---

### `[2]` Pilih Device yang Dikecualikan

```
  1.  Device_A  (APP5BK4M191Z0R29)
  2.  Device_B  (APP5CI50JWFL91N4)
  3.  Device_C  (ACP5CM52M50ZWJYI)

Nomor device dikecualikan (pisah koma, kosong = semua): █
```

✏️ Contoh: ketik `2,3` untuk skip Device_B dan Device_C.
Kosongkan dan Enter jika semua device ingin dipakai.

---

### `[3]` Pilih APK TopNod

```
  1.  topnod_v1.3.5.apk  (45.2 MB)  id=1001
  2.  topnod_v1.3.4.apk  (44.8 MB)  id=1000

Pilih nomor APK TopNod (1-2): █
```

✏️ Ketik nomor APK yang ingin diinstall, lalu Enter.

> Jika hanya ada 1 APK, langkah ini dilewati otomatis.

---

### `[4]` Selesaikan CAPTCHA Secara Manual

Saat bot sedang mengirim OTP di semua device, terminal akan berhenti:

```
⚠   Buka VSPhone, verifikasi captcha di SEMUA device,
    lalu tekan ENTER satu kali untuk lanjut.

  → Tekan ENTER setelah semua captcha selesai...  █
```

**Yang perlu dilakukan:**
1. Buka VSPhone di browser atau aplikasi
2. Masuk ke setiap device, selesaikan captcha yang muncul
3. Setelah **semua device** selesai → kembali ke terminal dan tekan **Enter sekali**

Bot akan langsung melanjutkan semua device secara paralel.

---

### `[5]` Bot Berjalan Otomatis

Setelah Enter, bot bekerja sendiri:

```
  ✔  [Device_A] OTP: 482910
  ✔  [Device_A] Wallet berhasil dibuat!
  ✔  [Device_B] OTP: 751203
  ✔  [Device_B] Wallet berhasil dibuat!
```

Hasil disimpan otomatis ke **`wallet_sukses.txt`**.

---

### `[6]` Setiap 5 Device — Minta Referral Baru

```
  ✔  5 device selesai — minta referral baru

  Referral code saat ini: REFBARU123
  Masukkan referral baru (kosong = pakai default): █
```

Bot meminta referral code baru setiap 5 wallet berhasil, lalu loop otomatis ke siklus berikutnya.

---

### Hentikan Bot

Tekan `Ctrl + C` kapan saja. Bot akan menampilkan ringkasan:

```
╔══════════════════ Script Dihentikan ══════════════════╗
║  Total siklus  : 3                                    ║
║  Total wallet  : 14                                   ║
╚═══════════════════════════════════════════════════════╝
```

---

## 📁 File yang Dihasilkan

| File | Keterangan |
|------|------------|
| `wallet_sukses.txt` | Daftar wallet berhasil (Device, Email, Password, Referral) |
| `topnod_log_*.txt` | Log lengkap semua aktivitas — otomatis simpan 5 file terakhir |

**Contoh isi `wallet_sukses.txt`:**
```
Device=Device_A | Email=abc123@mail.tm | Pass=masuk123 | Ref=REFBARU123
Device=Device_B | Email=xyz789@mail.tm | Pass=masuk123 | Ref=REFBARU123
```

---

## ⚠️ Catatan Penting

- Jangan tutup terminal selama bot berjalan
- Pastikan koneksi internet stabil
- APK TopNod harus sudah diupload ke cloud storage VSPhone sebelum menjalankan bot
- Koordinat di `config_ui.py` dikalibrasi untuk resolusi **1080×1920 DPI 320**

---

<br>

<div align="center">

<img src="silent_logo.png" width="120" alt="Silent Private Community Logo"/>

<br>

## 🙏 Special Thanks

```
╔═══════════════════════════════════════════════════╗
║                                                   ║
║         Mr. Silent Private Community              ║
║                                                   ║
║    "Tools ini lahir dari komunitas,               ║
║           untuk komunitas."                       ║
║                                                   ║
╚═══════════════════════════════════════════════════╝
```

Terima kasih atas kepercayaan, dukungan, dan semangat berbagi ilmu
yang selalu mengalir di dalam komunitas **Silent Private Community**.

Tanpa arahan dan insight dari **Mr. Silent**,
project ini tidak akan pernah ada. 🔑

<br>

**Keep grinding. Stay silent. Move smart.**

<br>

---

*© Silent Private Community · All rights reserved*

</div>
