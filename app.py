import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ExifTags, ImageOps
from datetime import datetime
import io
import os
import urllib.request
import re
from urllib.parse import urlparse, parse_qs

def ambil_waktu_exif(img):
    try:
        exif = img.getexif()
        if exif:
            for tag_id, value in exif.items():
                tag = ExifTags.TAGS.get(tag_id, tag_id)
                if tag == 'DateTime' or tag == 'DateTimeOriginal':
                    dt = datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                    return dt.strftime("%b %d, %Y %I:%M:%S %p")
    except Exception:
        pass
    return datetime.now().strftime("%b %d, %Y %I:%M:%S %p")

def parse_google_maps_url(input_text):
    """
    Parse Google Maps URL dan ekstrak informasi lokasi
    Support format:
    - https://maps.google.com/maps?q=...
    - https://www.google.com/maps/place/...
    - https://goo.gl/maps/...
    - https://maps.app.goo.gl/...
    - Koordinat manual: -2.9277,104.7461
    """
    
    if not input_text or not input_text.strip():
        return None, "Format tidak dikenali"
    
    input_text = input_text.strip()
    
    # ===== PATTERN 1: URL Google Maps dengan nama tempat =====
    if "google.com/maps" in input_text or "maps.app.goo.gl" in input_text:
        # Ekstrak teks dari URL jika ada nama tempat
        # Format: .../place/Nama+Tempat/data=...@lat,lng,z
        place_match = re.search(r'/place/([^/@]+)', input_text)
        if place_match:
            nama_tempat = urllib.parse.unquote(place_match.group(1)).replace('+', ' ')
            return nama_tempat, "success"
        
        # Ekstrak koordinat jika ada
        # Format: @-2.9277,104.7461,17z
        coord_match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', input_text)
        if coord_match:
            lat, lng = coord_match.groups()
            return f"{lat}, {lng}", "success"
        
        # Jika hanya URL tanpa info, ambil parameter q
        q_match = re.search(r'[?&]q=([^&]+)', input_text)
        if q_match:
            nama_tempat = urllib.parse.unquote(q_match.group(1))
            return nama_tempat, "success"
    
    # ===== PATTERN 2: Short URL (goo.gl/maps) =====
    if "goo.gl/maps" in input_text or "maps.app.goo.gl" in input_text:
        # Ekstrak kode short URL
        short_code = re.search(r'goo\.gl/maps/([A-Za-z0-9]+)', input_text)
        if short_code:
            return f"Lokasi [Kode: {short_code.group(1)}]", "needs_expansion"
    
    # ===== PATTERN 3: Koordinat Manual (lat, lng) =====
    coord_pattern = r'^(-?\d+\.?\d*)\s*[,/]\s*(-?\d+\.?\d*)$'
    coord_match = re.match(coord_pattern, input_text)
    if coord_match:
        lat, lng = coord_match.groups()
        try:
            lat_f, lng_f = float(lat), float(lng)
            # Validasi koordinat bumi
            if -90 <= lat_f <= 90 and -180 <= lng_f <= 180:
                return f"{lat}, {lng}", "coordinates"
        except ValueError:
            pass
    
    # ===== PATTERN 4: Plain text (nama lokasi) =====
    if len(input_text) > 5 and not input_text.startswith('http'):
        # Assume it's a location name
        return input_text, "location_name"
    
    return None, "Format tidak dikenali"

def dapatkan_font(ukuran_ideal):
    font_name = "Roboto-Regular.ttf"
    
    if not os.path.exists(font_name):
        try:
            url = "https://github.com/googlefonts/roboto/raw/main/src/hinted/Roboto-Regular.ttf"
            urllib.request.urlretrieve(url, font_name)
        except Exception:
            pass 
    
    try:
        return ImageFont.truetype(font_name, ukuran_ideal)
    except IOError:
        st.warning("⚠️ Font gagal dimuat, menggunakan font bawaan.")
        return ImageFont.load_default()

def beri_watermark(img, teks_waktu, teks_lokasi):
    img = ImageOps.exif_transpose(img)
    draw = ImageDraw.Draw(img)
    
    dimensi_terkecil = min(img.width, img.height)
    ukuran_font_ideal = max(int(dimensi_terkecil / 35), 14) 
    font = dapatkan_font(ukuran_font_ideal)
        
    teks_lengkap = f"{teks_waktu}\n{teks_lokasi}"
    
    bbox = draw.textbbox((0, 0), teks_lengkap, font=font, align="left")
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    margin_x = int(img.width * 0.03)
    margin_y = int(img.height * 0.03)
    
    x = margin_x
    y = img.height - margin_y - text_height
    
    ketebalan_outline = max(1, int(ukuran_font_ideal / 15))
    
    draw.multiline_text(
        (x, y), 
        teks_lengkap, 
        font=font, 
        fill="white", 
        align="left", 
        stroke_width=ketebalan_outline,
        stroke_fill="black"
    )
    
    return img

# ================= TAMPILAN ANTARMUKA STREAMLIT ================= #
st.set_page_config(page_title="Auto Tag Foto", layout="centered")
st.title("📸 Aplikasi Auto Tag Foto")
st.write("Unggah foto, paste Google Maps link atau koordinat, unduh hasilnya.")

col1, col2 = st.columns([2, 1])
with col1:
    uploaded_file = st.file_uploader("1. Pilih Foto", type=["jpg", "jpeg", "png"])
with col2:
    st.empty()

# ===== INPUT LOKASI DENGAN AUTO-PARSING =====
detail_lokasi_input = st.text_input(
    "2. Paste Google Maps Link atau Ketik Nama Lokasi",
    placeholder="https://maps.google.com/... atau Koordinat: -2.9277, 104.7461",
)

# State untuk menyimpan hasil parsing
lokasi_parsed = None
parsing_status = None

if detail_lokasi_input:
    lokasi_parsed, parsing_status = parse_google_maps_url(detail_lokasi_input)
    
    if parsing_status == "success":
        st.success(f"✅ Lokasi terdeteksi: **{lokasi_parsed}**")
    elif parsing_status == "coordinates":
        st.info(f"📍 Koordinat terdeteksi: **{lokasi_parsed}**")
    elif parsing_status == "location_name":
        st.info(f"📝 Nama lokasi: **{lokasi_parsed}**")
    elif parsing_status == "needs_expansion":
        st.warning(f"⚠️ {lokasi_parsed} - Gunakan URL penuh dari Google Maps untuk hasil lebih akurat")
    else:
        st.error("❌ Format tidak dikenali. Gunakan: Google Maps link, koordinat (lat, lng), atau nama lokasi.")
        lokasi_parsed = None

# ===== PROSES FOTO =====
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    waktu_foto = ambil_waktu_exif(image)
    
    col1, col2 = st.columns(2)
    with col1:
        waktu_input = st.text_input("Konfirmasi Waktu", value=waktu_foto)
    with col2:
        st.empty()
    
    # Gunakan lokasi yang sudah di-parse, atau gunakan input manual
    lokasi_final = lokasi_parsed if lokasi_parsed else detail_lokasi_input
    
    if st.button("✨ Proses Foto", type="primary", use_container_width=True):
        if not lokasi_final:
            st.error("⚠️ Masukkan lokasi terlebih dahulu!")
        else:
            with st.spinner("Memproses foto..."):
                img_hasil = beri_watermark(image.copy(), waktu_input, lokasi_final)
                
                st.success("✅ Foto berhasil diproses!")
                st.image(img_hasil, caption="Pratinjau Hasil", use_container_width=True)
                
                buf = io.BytesIO()
                img_hasil.save(buf, format="JPEG", quality=95)
                byte_im = buf.getvalue()
                
                st.download_button(
                    label="📥 Unduh Foto",
                    data=byte_im,
                    file_name=f"tagged_{uploaded_file.name}",
                    mime="image/jpeg",
                    use_container_width=True
                )
