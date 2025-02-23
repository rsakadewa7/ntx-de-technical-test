# Gunakan `python:3.11.4` sebagai base image
FROM python:3.11.4

# Menetapkan working directory di dalam container
WORKDIR /app

# Menyalin file requirements.txt dan menginstal dependensi
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin semua file ke dalam container
COPY . .

# Menjalankan script ETL secara otomatis ketika container berjalan
CMD ["python", "etl.py"]