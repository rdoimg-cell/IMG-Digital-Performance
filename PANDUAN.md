# 📘 Panduan Ask IMG Analytics

---

# BAGIAN 1 — Cara Memakai Aplikasinya

**Tidak perlu Python. Tidak perlu install apa pun.**

Kamu cuma butuh **1 file**: `ask_img_analytics.html`

### Caranya:

1. Klik dua kali file `ask_img_analytics.html`
2. Terbuka di browser (Chrome/Edge/Firefox — apa saja)
3. Selesai. Langsung bisa dipakai.

Tidak butuh internet. Tidak butuh login. Semua data sudah ada di dalam file itu.

### Membagikan ke tim

Kirim file `ask_img_analytics.html` lewat email / WhatsApp / Teams. Penerima tinggal klik dua kali.

Kalau mau berupa **link** (tim tidak perlu download), lihat Bagian 4.

---
---

# BAGIAN 2 — Cara Update Data Bulanan

Setiap bulan ada Excel baru. Ada **dua cara** — pilih salah satu.

## ⭐ Cara A: Lewat Browser (tanpa Python) — DISARANKAN

File yang dipakai: **`UPDATE DATA.html`**

### Langkah 1
Klik dua kali `UPDATE DATA.html` → terbuka di browser.

### Langkah 2
Klik kotak besar bertuliskan *"Klik di sini atau seret 4 file Excel"*, lalu pilih **4 file Excel** terbaru sekaligus.

### Langkah 3
Tunggu sampai keempatnya bertanda **hijau "siap"**.

⏳ File Scraping berukuran ±20 MB, jadi butuh **sekitar 1 menit**. Selama itu tandanya oranye *"membaca…"*. **Ini normal, jangan ditutup.**

### Langkah 4
Klik tombol **Mulai Proses**. Perlu 2–5 detik.

### Langkah 5
Klik **⬇ Download ask_img_analytics.html**.

File yang baru masuk ke folder Download. **Timpa** file lama dengan yang ini.

*(Kalau pakai GitHub Pages, unduh juga `index.html` lewat tombol abu-abu di bawahnya.)*

**Selesai.** Sekitar 2 menit, tanpa install apa pun.

---

## Cara B: Lewat Python (kalau Python sudah ada)

File yang dipakai: **`UPDATE DATA.bat`**

1. Taruh 4 file Excel terbaru di folder yang sama
2. Klik dua kali `UPDATE DATA.bat`
3. Tunggu 1–2 menit → aplikasi terbuka sendiri

Hasilnya **persis sama** dengan Cara A — sudah dites berdampingan, angkanya identik sampai dua desimal.

Kalau Python belum ada, file .bat akan memberi tahu cara memasangnya. Tapi kalau tidak mau repot, **pakai Cara A saja** — hasilnya sama.

---
---

# BAGIAN 3 — Kalau Ada Masalah

## Ada file bertanda merah "belum ada"

File dicari lewat **kata kunci di nama file**, jadi nama boleh berubah tiap bulan asal kata kuncinya ada.

| Harus mengandung kata | Contoh nama yang cocok |
|---|---|
| `konten` + `img` | Database **Konten IMG** Agustus 2026.xlsx |
| `scraping` | Database Konten **Scraping** Agustus 2026.xlsx |
| `socmed` | Database Rekap **Socmed** IMG 2026.xlsx |
| `portal` | Database **Portal** Performance IMG 2026.xlsx |

**Solusi:** rename file Excel-nya supaya mengandung kata kunci itu, lalu masukkan ulang.

⚠️ Jangan ada dua file dengan kata kunci sama — hapus dulu yang lama.

---

## Muncul: `Tidak ada sheet yang mengandung "recap + youtube"`

Nama tab di dalam Excel berubah. Layar akan menampilkan daftar tab yang ada.

Tab yang dibutuhkan:

| Harus mengandung kata | Nama tab saat ini |
|---|---|
| `youtube` + `studio` | Content Youtube Studio |
| `scraping` | Scraping Juli 2026 |
| `facebook` | Facebook, Instagram, Tiktok, X |
| `recap` + `youtube` | Recap Youtube |
| `revenue` + `youtube` | Source Revenue Youtube |
| `similar` | Competitor - Similar Web |
| `revenue` + `portal` | Revenue Direct Sales Portal |

**Solusi:** rename tab di Excel supaya mengandung kata kuncinya.

---

## Browser terasa macet saat membaca file

Normal. File Scraping berisi ±50.000 baris. Tunggu sampai 1 menit. Jangan klik apa-apa.

Kalau lewat 3 menit masih belum hijau: tutup tab, buka lagi `UPDATE DATA.html`, masukkan file **satu per satu** (yang paling besar terakhir).

---

## Tombol "Mulai Proses" tetap abu-abu

Belum semua 4 file hijau. Lihat daftar di bawah kotak — yang merah berarti belum ada, yang oranye berarti masih dibaca.

---

## Angka di aplikasi terlihat nol semua

Lihat jumlah baris di layar proses. Kalau tertulis 0 baris, berarti tab Excel-nya kosong atau salah tab.

---

## `UPDATE DATA.html` tidak mau terbuka

Klik kanan file → **Open with** → pilih Chrome / Edge / Firefox.

---
---

# BAGIAN 4 — Bikin Link Online (opsional, sekali setup)

Supaya tim cukup klik link, tanpa download file. Gratis.

### Setup pertama kali

1. Buka https://github.com/rdoimg-cell/IMG-Digital-Performance
2. Klik **Add file** → **Upload files**
3. Seret `ask_img_analytics.html` dan `index.html` ke situ
4. Klik **Commit changes**
5. Klik tab **Settings** (kanan atas)
6. Menu kiri → **Pages**
7. Bagian *Branch*: pilih **main**, folder **/ (root)** → **Save**
8. Tunggu 1–2 menit

Link jadi:

```
https://rdoimg-cell.github.io/IMG-Digital-Performance/
```

Bagikan ke siapa pun. Gratis, tanpa batas pengunjung, tanpa perlu akun.

### Update bulan berikutnya

Setelah dapat file baru dari `UPDATE DATA.html`:

1. Buka repo di atas → **Add file** → **Upload files**
2. Seret `ask_img_analytics.html` dan `index.html` (menimpa yang lama)
3. **Commit changes** → tunggu ±1 menit

---
---

# BAGIAN 5 — Daftar File

| File | Fungsi | Wajib? |
|---|---|---|
| **`ask_img_analytics.html`** | **Aplikasinya** — ini yang dipakai & dibagikan | ✅ |
| **`UPDATE DATA.html`** | Update data lewat browser, tanpa Python | ✅ untuk update |
| `index.html` | Salinan untuk GitHub Pages | opsional |
| `UPDATE DATA.bat` | Update lewat Python (alternatif) | opsional |
| `template.html` | Tampilan + logika chatbot | hanya kalau ubah UI |
| `build_data.py` | Excel → data ringkas (dipakai .bat) | hanya untuk Cara B |
| `build_app.py` | Gabung template + data (dipakai .bat) | hanya untuk Cara B |
| `build_updater.py` | Membuat ulang `UPDATE DATA.html` | hanya kalau `template.html` diubah |
| `updater_src.html` | Sumber `UPDATE DATA.html` | hanya kalau ubah updater |
| 4 file `.xlsx` | Data mentah | ✅ untuk update |

**Minimal yang perlu disimpan: `ask_img_analytics.html` + `UPDATE DATA.html`.** Sisanya cadangan.

---
---

# BAGIAN 6 — Referensi Teknis

## Cara kerja

```
4 file Excel  ──►  diringkas  ──►  data ringkas  ──►  digabung  ──►  ask_img_analytics.html
 (70.000+ baris)                      (41 KB)         ke template      (1 file siap pakai)
```

Peringkasan bisa dilakukan **di browser** (`UPDATE DATA.html`, pakai SheetJS) atau **lewat Python** (`build_data.py`, pakai pandas). Keduanya menghasilkan angka yang identik — sudah diuji berdampingan.

**Kenapa diringkas dulu?** Kalau 70.000 baris ditempel mentah ke HTML, filenya jadi puluhan MB dan lambat. Yang dibutuhkan chatbot hanya hasil hitungannya (total, rata-rata, ranking) — itu muat di 41 KB dan buka instan.

**Kenapa tidak baca Google Sheets langsung?** Sudah dicoba dan gagal: server hosting memblokir akses ke Google Sheets (`403 Forbidden`). Pendekatan sekarang tidak butuh koneksi ke mana pun, jadi tidak bisa gagal.

**Apakah data terkirim ke internet saat update?** Tidak. `UPDATE DATA.html` memproses semuanya di dalam browser. File Excel tidak pernah meninggalkan komputermu.

## Kolom yang dibaca

**Content Youtube Studio** — `Unit`, `Channel`, `Video title`, `Video publish time`, `Views`, `Engaged views`, `Watch time (hours)`, `Subscribers`, `Impressions`, `Impressions click-through rate (%)`, `Average percentage viewed (%)`

**Scraping** — `Cluster`, `Channel`, `Title`, `Category`, `Views`, `Likes`, `Comments`, `ER (%)`

**Facebook, Instagram, Tiktok, X** — `Platform`, `Unit`, `Channel`, `Videos Published`, `Lifetime Subscriber/Followers`, `New Subscribers/Followers`, `Views (Cumulative)`, `Revenue (USD)`, `Revenue (IDR)`, `Engagement`, `Reach`

**Recap Youtube** — `Unit`, `Channel`, `Year`, `Month` (nama bulan: January, February, …), `Views Cummulative`, `Watch time (hours)`, `Subscribers`, `Videos published`, `Impressions click-through rate (%)`, `Lifetime Subscriber/Followers`, `Revenue Cummulative (IDR)`

**Source Revenue Youtube** — `Unit`, `Channel`, `Revenue source`, `Estimated revenue (IDR)`

**Competitor - Similar Web** — `Group`, `Portal`, `Total Visits`, `Page Views`, `Unique Visitors`, `Bounce Rate`, `Page per Visit`

**Revenue Direct Sales Portal** — `CHANNEL`, `VALUE`

Kalau nama kolom berubah, angka terkait akan jadi 0. Samakan header di Excel.

## Batas kemampuan — dan bagaimana bot mengakuinya

Mesin chatbot ini bekerja dengan **pencocokan kata kunci**, bukan pemahaman bahasa. Supaya tidak ada angka yang salah ditafsirkan, ada dua lapis pengaman.

### Lapis 1 — ditolak terang-terangan

Untuk maksud yang memang belum didukung, bot **tidak menampilkan tabel sama sekali** dan menjelaskan alternatifnya:

| Jenis pertanyaan | Contoh |
|---|---|
| Sebab-akibat | "Kenapa views Official iNews turun?" |
| Prediksi | "Perkiraan revenue Agustus 2026" |
| Rekomendasi | "Kategori apa yang sebaiknya diperbanyak?" |
| Peringkat bersyarat | "Channel mana yang tren-nya menurun?" |
| Korelasi | "Korelasi followers socmed dengan views YouTube" |
| Deteksi anomali | "Ada anomali di data bulan ini?" |
| Percakapan bersambung | "Bagaimana dengan bulan sebelumnya?" |
| Ekspor / kirim / grafik | "Export hasil ini ke Excel" |
| Target / RKAP | "Berapa target revenue tahun ini?" |

### Lapis 2 — dijawab, tapi diberi peringatan

Kalau bot mengenali topiknya tapi **mengabaikan sebagian pertanyaan**, jawabannya tetap muncul disertai kotak kuning:

> ⚠️ **Sebagian pertanyaan Anda belum saya proses**
> Saya mengabaikan nama channel: **Official iNews**. Angka di atas adalah keseluruhan data, belum disaring sesuai itu.

Yang dideteksi: nama channel/program/kategori/cluster/portal, syarat angka ("di atas 2%", "di bawah rata-rata"), dan syarat majemuk ("naik **tapi** turun").

### Kemampuan analisis lanjutan

| Jenis | Contoh | Cara kerjanya |
|---|---|---|
| **Peringkat bersyarat** | "Channel mana yang revenue-nya naik?" | Bandingkan dua periode per channel, tampilkan yang naik/turun beserta selisihnya |
| **Penguraian perubahan** | "Kenapa views turun?" | Uraikan perubahan total menjadi andil tiap channel. **Menunjukkan di mana, bukan mengapa** |
| **Deteksi anomali** | "Ada anomali di data bulan ini?" | Tandai hari yang menyimpang lebih dari 1,8 simpangan baku dari rata-rata |
| **Korelasi** | "Korelasi views dengan revenue" | Pearson antar channel dan antar bulan. Antar bulan lebih informatif |
| **Proyeksi** | "Perkiraan revenue bulan depan" | Garis tren lurus atas 6 bulan terakhir. **Patokan kasar, bukan ramalan** |

Kalau arah perubahan ternyata berlawanan dengan dugaan di pertanyaan ("kenapa turun?" padahal naik), bot mengatakannya lebih dulu sebelum menampilkan tabel.

### Penyaringan per entitas

Nama channel, unit, program, dan kategori yang disebut di pertanyaan kini benar-benar dipakai menyaring:

- "Kategori apa paling bagus **di Official iNews**?" → hanya channel itu
- "Program terbaik **di Sindonews**" → seluruh channel di unit Sindonews
- "**Program Rakyat Bersuara**" → rincian satu program, lengkap dengan sebaran per channel
- "Program dengan **ER di atas 2%**" → hanya yang memenuhi syarat
- "Channel dengan **RPM di bawah rata-rata**" → ambang dihitung otomatis

### Pertanyaan lanjutan

Bot mengingat pertanyaan terakhir. "Bagaimana dengan bulan sebelumnya?" dan "Kalau di Okezone?" disusun ulang memakai konteks itu, dan jejaknya ditampilkan: *↩️ Saya melanjutkan "Revenue Juli 2026" untuk Juni 2026*.

Konteks hanya dipakai kalau pertanyaannya sendiri tidak dikenali — pertanyaan lengkap tidak akan pernah tertimpa konteks lama.

### Salin & unduh

Di bawah setiap jawaban ada tombol **📋 Salin tabel** dan **⬇ Unduh CSV**. CSV memakai pemisah titik-koma dan penanda BOM, jadi langsung rapi di Excel Indonesia.

### Hasil pengujian

Dari 45 pertanyaan yang mewakili pemakaian nyata:

| Status | Awal | Setelah penjaga | Sekarang |
|---|---|---|---|
| Dijawab bersih (bisa dipercaya apa adanya) | 15 | 15 | **29** |
| Dijawab + peringatan bagian yang diabaikan | 0 | 12 | 8 |
| Ditolak terang-terangan | 0 | 18 | 8 |
| Tidak dikenali | 0 | 0 | 0 |
| **Salah tanpa peringatan** | **30** | **0** | **0** |

Yang masih ditolak: rekomendasi (3), pengiriman email/PDF (1), perincian jawaban sebelumnya (1), dan sisanya pertanyaan lintas sumber yang belum bisa digabung.

---

## Penyeragaman nama channel

Sheet yang berbeda menulis channel yang sama dengan cara berbeda. Kalau tidak diseragamkan, satu channel muncul sebagai beberapa baris terpisah di ranking. Penyeragaman dilakukan tiga lapis:

1. **Tabel `CHANNEL_ALIAS`** (di `build_data.py` dan `updater_src.html`) — untuk varian yang katanya beda:

   | Ditulis di Excel | Jadi |
   |---|---|
   | `Radio RDI 97.1 FM Jakarta`, `Radio RDI 97.1 FM`, `RDI 97.1 FM Jakarta` | Radio RDI |
   | `iNews Premium Sports` | iNews Premium Sport |
   | `iNews Jatim Official` | iNews Jatim |
   | `iNews Sumut Official` | iNews Sumut |
   | `Oke Vibes` | Okezone Vibes! |

2. **Nama baku dari sheet `Content Youtube Studio`** — 20 channel IMG. Nama di sheet lain yang sama persis kecuali huruf besar/kecil (`IDX CHANNEL`, `RAKYAT BERSUARA`, `SINDOnews`) otomatis diseragamkan ke ejaan Studio.

3. **Sisa duplikat beda kapital di dalam satu sheet** — dipakai ejaan yang paling sering muncul.

**Kalau bulan depan ada channel baru dengan nama tidak konsisten:** tambahkan barisnya ke `CHANNEL_ALIAS` (kunci ditulis huruf kecil semua). Jendela proses akan menampilkan berapa nama yang digabung, jadi perubahan mencurigakan mudah terlihat.

---

## Dimensi analisis dari sheet Youtube Studio

Sheet ini menyimpan satu baris per video beserta label editorialnya. Semua sudah dipakai chatbot:

| Kolom | Isi | Contoh pertanyaan |
|---|---|---|
| `Kategori` | 14 kategori (Buletin, Breaking News, Talkshow, …) | "kategori apa paling bagus?" |
| `Program` | 107 nama program | "program terbaik" |
| `Part` | TV Content, Digital Content, Radio Content, Rakyat Bersuara | "performa per Part" |
| `Sub Part` | Regular / Exclusive IP / Extended Program | (ikut jawaban Part) |
| `Original` | Original vs Repack | "original atau repack?" |
| `Type Content` | Video / Short / Live | "format konten" |
| `8 Menit` | <3 menit, 3-8 menit, >8 menit | "performa per durasi video" |
| `Video publish time` | tanggal (per hari) | "performa harian" |

Metrik yang ikut dihitung: revenue, RPM, CPM, likes, shares, comments, subscriber gained/lost, new vs returning viewers, CTR, dan persentase ditonton.

Dari sheet lain: jam unggah (Scraping), demografi gender & umur (Socmed), durasi kunjungan & bounce rate (Portal), revenue per jenis penjualan (Portal).

---

## Catatan arti angka (penting saat presentasi)

- **`Views Cummulative` sebenarnya views per bulan**, bukan akumulatif berjalan. Jadi penjumlahan antar bulan sudah benar.
- **`Subscribers` di Recap Youtube = pertambahan subscriber per bulan**, bukan total. Di aplikasi diberi label **"Subscriber Gained"**.
- **Cakupan waktu tiap sumber berbeda.** Recap YouTube, Source Revenue, dan Socmed: Januari 2024–Juli 2026. Portal: Januari 2025–Juli 2026. **Scraping dan YouTube Studio hanya Juli 2026** — Studio rinci per tanggal (1–31 Juli), Scraping per video. Jadi analisis berperiode tidak berlaku untuk engagement rate, ranking cluster, top video, kategori, program, dan CTR.
- **Jumlah channel:** 20 channel IMG (konsisten di semua sheet) dan **35 channel kompetitor** di file Scraping Juli 2026 — KompasTV 15, MetroTV 12, TV One 6, CNBC Indonesia 1, Liputan6 1. Kalau targetnya 60, berarti ada channel kompetitor yang belum masuk hasil scraping.
- **Perbandingan antar tahun memakai rata-rata per bulan**, bukan total — karena tahun berjalan belum lengkap. Baris bulan kosong otomatis dibuang.
- **Spasi di ujung nama channel dirapikan otomatis** (mis. `tvOneNews ` → `tvOneNews`), supaya nama yang sama tidak terhitung dua kelompok.
- **Label periode diambil dari nama file Excel.** Kalau nama file tidak menyebut bulan (mis. `Database Konten IMG.xlsx`), periode otomatis diambil dari bulan terakhir yang ada datanya — bukan lagi ditulis "Terbaru".
- **Kartu KPI di bagian atas memakai bulan terakhir yang ada datanya** (saat ini Juli 2026), diambil dari sheet `Recap Youtube`. Bulan ini berpindah sendiri begitu Excel diperbarui.
- **Total followers diambil dari `Lifetime Subscriber/Followers` pada bulan terakhir**, dijumlah antar channel — berlaku untuk YouTube maupun socmed. Sengaja tidak memakai nilai tertinggi lintas bulan, karena penurunan follower akan tertutupi angka puncak bulan sebelumnya (contoh nyata: X turun 430 rb dari puncaknya).
- **Kartu "Total Followers Socmed" sudah termasuk YouTube** — YouTube + Facebook + Instagram + TikTok + X.
- **Nama channel yang hanya beda huruf besar/kecil digabung otomatis.** Contoh nyata: `Sindonews` (29 bulan) dan `SINDOnews` (7 bulan) sebenarnya channel yang sama, tapi kalau dibiarkan muncul sebagai dua baris terpisah di ranking. Ejaan yang dipakai adalah yang paling sering muncul.
- **Revenue per channel diambil dari kolom `Revenue Cummulative (IDR)` di sheet Recap Youtube.** Sheet `Source Revenue Youtube` dipakai khusus untuk rincian sumber revenue. Total keduanya berbeda ±0,4% (23,65 vs 23,54 miliar) — perbedaan yang ada di sumbernya, bukan akibat pengolahan.
- **Cluster IMG** = iNews, Sindonews, Okezone, IDX Channel. Sisanya dihitung kompetitor. Kalau berubah, edit `IMG_UNITS` di `template.html`.
- **Bounce rate portal** ada yang di atas 1 (mis. 5.87) — kemungkinan beda satuan di sumbernya. Perlu dicek tim data.

## Pertanyaan berperiode

Bot mengenali periode dalam pertanyaan dan memfilter angkanya. Format yang dipahami:

| Ditulis | Diartikan |
|---|---|
| `Jan-Juli 2026`, `januari sampai juli 2026`, `jan s/d jul 2026` | Januari–Juli 2026 |
| `Januari 2025 - Maret 2026` | lintas tahun |
| `Q1 2026`, `kuartal 2 2026`, `triwulan 3` | per kuartal |
| `Semester 1 2026`, `H1 2026` | per semester |
| `Juli 2026`, `bulan Juli` | satu bulan |
| `2025`, `tahun 2025` | satu tahun penuh |
| `6 bulan terakhir`, `3 bulan terakhir` | dihitung mundur dari bulan terakhir |
| `bulan lalu`, `bulan ini`, `YTD`, `tahun lalu` | relatif |

**Membandingkan dua periode.** Tulis `vs` di antara keduanya:

- `Revenue Q1 vs Q2 2026`
- `Berapa revenue IMG periode Q1 vs Q2?`
- `Revenue 2025 vs 2026`
- `Traffic portal Q1 vs Q2 2026`
- `Followers socmed 2025 vs 2026`

Hasilnya tabel berdampingan lengkap dengan persentase selisih. Kalau sisi kiri tidak menyebut tahun, tahunnya diambil dari sisi kanan.

**Pemilih periode di panel kiri.** Ada dropdown "Periode data" untuk mengunci periode tanpa perlu mengetikkannya tiap kali. Periode yang ditulis langsung di pertanyaan selalu mengalahkan pilihan dropdown.

**Yang bisa difilter periode:** revenue, views, watch time, subscriber, followers socmed, traffic portal.

**Cakupan tiap sumber berbeda, dan bot menyesuaikan sendiri:**

| Sumber | Rentang | Dipakai untuk |
|---|---|---|
| Recap YouTube | Jan 2024 – Jul 2026 (bulanan) | revenue, views, watch time, subscriber |
| Social Media | Jan 2024 – Jul 2026 (bulanan) | followers, engagement, demografi |
| Portal Similarweb | Jan 2025 – Jul 2026 (bulanan) | visits, bounce, durasi kunjungan |
| Revenue Direct Sales | Jan 2026 – Jun 2026 (bulanan) | revenue per jenis penjualan |
| YouTube Studio | Jul 2026 (**per tanggal**, 31 hari) | kategori, program, Part, Original, durasi, RPM, harian |
| Scraping | Jul 2026 (**per tanggal**) | jam unggah, ER cluster, top video |

Kalau periode yang diminta di luar rentang sumbernya, bot **bilang terus terang** dan menyebutkan rentang yang tersedia — bukan menampilkan angka periode lain.

**Yang belum bisa difilter periode:** ranking cluster, top video, dan ER per cluster. Data mentahnya ada per tanggal, tapi agregatnya belum dipecah per hari.

**Keterangan periode selalu muncul di bawah setiap jawaban**, lengkap dengan sumber data dan rentang yang tersedia — supaya tidak ada angka yang salah ditafsirkan saat presentasi.

Kalau periode di luar rentang data, bot bilang terus terang dan menyebutkan rentang yang tersedia (YouTube & socmed: Jan 2024–Jul 2026, portal: Jan 2025–Jul 2026).

---

## Mengubah tampilan atau menambah pertanyaan

Semua ada di `template.html`. Cari `function answer(qRaw)` — tiap jenis pertanyaan adalah satu blok `if`:

```javascript
if(has('kata-kunci','sinonim','keyword lain')){
  return card('📊 Judul Jawaban',
    table(['Kolom A','Kolom B'], baris),
    'Kalimat insight di bawah tabel');
}
```

Taruh blok baru **sebelum** komentar `/* --- fallback --- */`.

Untuk mengubah daftar pertanyaan di panel kiri, edit variabel `SUG` di bagian bawah file.

⚠️ **Setelah mengubah `template.html`**, `UPDATE DATA.html` harus dibuat ulang supaya ikut perubahan itu — jalankan `python3 build_updater.py`. Kalau tidak ada Python, minta bantuan yang punya, atau kirim `template.html`-nya untuk dibuatkan ulang.
