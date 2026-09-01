import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ExifTags, ImageOps
import json
import os
from datetime import datetime
import io

# Konfigurasi Database JSON
JSON_FILE = 'data_foto.json'

def init_db():
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'w') as f:
            json.dump([], f)

def simpan_data(nama_file, waktu, lokasi):
    with open(JSON_FILE, 'r') as f:
        data = json.load(f)
    
    data.append({
        "waktu_unggah": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nama_file": nama_file,
        "waktu_foto": waktu,
        "link_lokasi": lokasi
    })
    
    with open(JSON_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def ambil_waktu_exif(img):
    try:
        exif = img.getexif()
        if exif:
            # Mencari tag DateTime (ID: 306) atau DateTimeOriginal (ID: 36867)
            for tag_id, value in exif.items():
                tag = ExifTags.TAGS.get(tag_id, tag_id)
                if tag == 'DateTime' or tag == 'DateTimeOriginal':
                    return value
    except Exception:
        pass
    return datetime.now().strftime("%Y:%m:%d %H:%M:%S")

def beri_watermark(img, teks_waktu, teks_lokasi):
    # Mengembalikan orientasi foto ke posisi aslinya (mencegah foto HP miring)
    img = ImageOps.exif_transpose(img)
    
    draw = ImageDraw.Draw(img)
    
    # Mencoba memuat font sistem, jika tidak ada pakai default bawaan
    try:
        # Anda bisa meletakkan file .ttf khusus di folder yang sama untuk font yang lebih bagus
        font = ImageFont.truetype("arial.ttf", int(img.height / 35))
    except IOError:
        font = ImageFont.load_default()
        
    teks = f"Waktu: {teks_waktu}\nLokasi: {teks_lokasi}"
    
    # Menentukan posisi teks (kiri bawah)
    margin_x = int(img.width * 0.03)
    margin_y = int(img.height * 0.03)
    
    # Menghitung ukuran teks secara kasar untuk default font
    bbox = draw.textbbox((0, 0), teks, font=font)
    text_height = bbox[3] - bbox[1]
    
    x = margin_x
    y = img.height - margin_y - text_height
    
    # Menggambar bayangan teks (Stroke) agar kontras dan mudah dibaca
    draw.multiline_text((x+3, y+3), teks, font=font, fill="black")
    draw.multiline_text((x, y), teks, font=font, fill="#FFD700") # Warna kuning emas
    
    return img

# ================= TAMPILAN ANTARMUKA STREAMLIT ================= #

st.set_page_config(page_title="Auto Tag Foto", layout="centered")
st.title("📸 Aplikasi Auto Tag Foto")
st.write("Unggah foto lapangan, masukkan link Google Maps, lalu unduh foto dengan watermark waktu & lokasi.")

init_db()

uploaded_file = st.file_uploader("1. Pilih Foto", type=["jpg", "jpeg", "png"])
link_gmaps = st.text_input("2. Link Google Maps Lokasi", placeholder="https://maps.app.goo.gl/...")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # Mengekstrak waktu dari metadata foto
    waktu_foto = ambil_waktu_exif(image)
    
    # Membiarkan pengguna mengedit waktu jika metadata tidak terbaca
    waktu_input = st.text_input("Konfirmasi Waktu (Bisa diedit)", value=waktu_foto)
    
    if st.button("Proses Foto & Simpan Data", type="primary"):
        with st.spinner("Memproses foto..."):
            # Proses watermark
            img_hasil = beri_watermark(image.copy(), waktu_input, link_gmaps)
            
            # Simpan log ke JSON
            simpan_data(uploaded_file.name, waktu_input, link_gmaps)
            
            st.success("✅ Foto berhasil diproses dan data log disimpan!")
            st.image(img_hasil, caption="Pratinjau Hasil Foto", use_column_width=True)
            
            # Konversi gambar ke format yang bisa diunduh
            buf = io.BytesIO()
            img_hasil.save(buf, format="JPEG", quality=95)
            byte_im = buf.getvalue()
            
            st.download_button(
                label="📥 Unduh Foto",
                data=byte_im,
                file_name=f"tagged_{uploaded_file.name}",
                mime="image/jpeg"
            )
