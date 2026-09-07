# 1. Cek arsitektur CPU Anda (untuk memilih binary yang tepat)
uname -m
# x86_64  -> pakai tailwindcss-linux-x64
# aarch64 -> pakai tailwindcss-linux-arm64

# 2. Unduh Tailwind Standalone CLI v3.4.17 (TANPA Node.js) ke root proyek
curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/download/v3.4.17/tailwindcss-linux-x64
mv tailwindcss-linux-x64 tailwindcss
chmod +x tailwindcss

# (Alternatif Windows PowerShell):
# Invoke-WebRequest https://github.com/tailwindlabs/tailwindcss/releases/download/v3.4.17/tailwindcss-windows-x64.exe -OutFile tailwindcss.exe

# 3. Siapkan folder sumber & output
mkdir -p static/src static/css

# 4. Build CSS produksi (minified) — jalankan SETIAP KALI ada perubahan class/template
./tailwindcss -i static/src/input.css -o static/css/app.css --minify

# 5. (Mode pengembangan) jalankan di terminal TERPISAH — rebuild otomatis saat file berubah
# ./tailwindcss -i static/src/input.css -o static/css/app.css --watch

# 6. Jalankan server
python manage.py runserver
