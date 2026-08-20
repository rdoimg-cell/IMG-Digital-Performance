@echo off
chcp 65001 >nul
title Update Ask IMG Analytics
cd /d "%~dp0"

echo.
echo ==========================================
echo   UPDATE ASK IMG ANALYTICS
echo ==========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
  echo [GAGAL] Python belum terpasang di komputer ini.
  echo.
  echo Cara pasang:
  echo   1. Buka https://www.python.org/downloads/
  echo   2. Download dan install
  echo   3. PENTING: centang "Add Python to PATH" saat install
  echo   4. Tutup jendela ini, lalu jalankan lagi file ini
  echo.
  pause
  exit /b 1
)

echo [1/3] Memeriksa library yang dibutuhkan...
python -c "import pandas, openpyxl" >nul 2>&1
if errorlevel 1 (
  echo       Belum ada. Memasang pandas dan openpyxl...
  python -m pip install --quiet pandas openpyxl
  if errorlevel 1 (
    echo.
    echo [GAGAL] Gagal memasang library. Cek koneksi internet.
    pause
    exit /b 1
  )
)
echo       OK
echo.

echo [2/3] Membaca file Excel dan meringkas data...
python build_data.py
if errorlevel 1 (
  echo.
  echo [GAGAL] Baca pesan error di atas.
  echo         Biasanya: file Excel belum ada di folder ini,
  echo         atau nama sheet di dalam Excel berubah.
  echo.
  pause
  exit /b 1
)
echo.

echo [3/3] Membuat aplikasi HTML...
python build_app.py
if errorlevel 1 (
  echo.
  echo [GAGAL] Baca pesan error di atas.
  pause
  exit /b 1
)

echo.
echo ==========================================
echo   SELESAI
echo ==========================================
echo.
echo File yang siap dipakai: ask_img_analytics.html
echo.
echo Tekan tombol apa saja untuk membuka aplikasinya...
pause >nul
start "" "ask_img_analytics.html"
