# Gunakan `python:3.11.4` sebagai base image
FROM python:3.11.4

# Menetapkan working directory di dalam container
WORKDIR /app

# Menyalin file requirements.txt dan menginstal dependensi
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin semua file ke dalam container
COPY . .

# Mengekspos port 6000 agar bisa diakses dari luar
EXPOSE 6000

# Menjalankan API dengan Uvicorn
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "6000"]