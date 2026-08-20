# 📋 Laporan Penamaan Channel

Dibuat otomatis dari data **Juli 2026**. Dokumen ini untuk tim data — kalau perbaikan dilakukan langsung di sumbernya, penyeragaman otomatis tidak lagi diperlukan.

---

## Ringkasan

- **8,122 baris** perlu diseragamkan, dari **12 varian penulisan**
- Nama baku: **20 channel** (acuan: sheet `Content Youtube Studio`)
- Nama yang belum dikenali: **0**

---

## Varian yang diseragamkan

| Ditulis di Excel | Seharusnya | Baris terdampak |
|---|---|---|
| `SINDOnews` | **Sindonews** | 3,295 |
| `IDX CHANNEL` | **IDX Channel** | 2,133 |
| `iNews Sumut Official` | **iNews Sumut** | 1,003 |
| `iNews Jatim Official` | **iNews Jatim** | 990 |
| `RDI 97.1 FM Jakarta` | **Radio RDI** | 144 |
| `iNews Premium Sports` | **iNews Premium Sport** | 138 |
| `RAKYAT BERSUARA` | **Rakyat Bersuara** | 118 |
| `Radio RDI 97.1 FM` | **Radio RDI** | 105 |
| `Okezone Vibes` | **Okezone Vibes!** | 81 |
| `SINDO Kalam` | **Sindo Kalam** | 72 |
| `Oke Vibes` | **Okezone Vibes!** | 36 |
| `Radio RDI 97.1 FM Jakarta` | **Radio RDI** | 7 |

---

## 20 nama baku

1. Buletin iNews GTV
2. IDX Channel
3. IDX Channel Insight
4. Lintas iNews MNCTV
5. Official iNews
6. Okezone
7. Okezone Vibes!
8. Radio RDI
9. Rakyat Bersuara
10. Seputar iNews RCTI
11. Sindo Kalam
12. Sindo Podcast
13. Sindonews
14. Trijaya FM
15. iNews Bali Nusra
16. iNews Jabar
17. iNews Jateng
18. iNews Jatim
19. iNews Premium Sport
20. iNews Sumut

---

## Kalau ingin diperbaiki di sumbernya

Gunakan Find & Replace di Excel (centang **Match case**), lalu ganti sesuai tabel di atas. Sheet yang perlu dicek:

- `Recap Youtube` dan `Source Revenue Youtube` (di file Rekap Socmed)
- `Scraping Juli 2026` (di file Konten Scraping)
- `Facebook, Instagram, Tiktok, X` (di file Rekap Socmed)

Sheet `Content Youtube Studio` sudah benar — jadikan itu acuan.

---

## Catatan penting

Aplikasi **tidak** membutuhkan perbaikan ini. Penyeragaman dilakukan setiap kali data diolah, jadi file Excel boleh tetap seperti sekarang.

Yang perlu diperhatikan: kalau bulan depan muncul **varian penulisan baru** yang belum ada di tabel, aplikasi akan menampilkannya sebagai peringatan — di jendela proses `UPDATE DATA.html`, dan lewat pertanyaan **"Cek penamaan channel"** di aplikasi. Tambahkan varian itu ke `CHANNEL_ALIAS` (di `build_data.py` dan `updater_src.html`), atau perbaiki langsung di Excel.

Contoh nyata: saat pemeriksaan ini dibuat, ditemukan `Okezone Vibes` (tanpa tanda seru) di sheet Source Revenue yang sebelumnya lolos — 81 baris. Sekarang sudah ditangani.