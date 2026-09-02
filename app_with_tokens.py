"""
PhotoTag Pro - Production-ready with Design Tokens
Reads color tokens from JSON for maintainability
"""

import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ExifTags, ImageOps
from datetime import datetime
import io
import os
import urllib.request
import json
import sys

# ================= DESIGN TOKENS ================= #

def load_design_tokens():
    """
    Load design tokens from JSON file.
    Supports both local dev and production environments.
    """
    token_paths = [
        'design-system/tokens/colors.json',  # Local dev
        '../design-system/tokens/colors.json',  # Subdirectory
        './tokens/colors.json',  # Alternative
    ]
    
    # Default tokens (fallback if file not found)
    default_tokens = {
        "colors": {
            "primary": {"600": "#2563eb", "800": "#1e40af"},
            "success": "#10b981",
            "text": {
                "primary": "#0f172a",
                "secondary": "#64748b",
                "muted": "#94a3b8"
            },
            "background": {
                "light": "#f8fafc",
                "lighter": "#f1f5f9",
                "card": "#ffffff"
            },
            "border": {
                "light": "#e2e8f0",
                "strong": "#cbd5e1"
            }
        }
    }
    
    # Try to load from file
    for path in token_paths:
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    loaded = json.load(f)
                    print(f"✅ Tokens loaded from {path}")
                    return loaded
        except Exception as e:
            print(f"⚠️ Could not load from {path}: {e}")
            continue
    
    print("ℹ️ Using default tokens (file not found)")
    return default_tokens

# Load tokens once at startup
TOKENS = load_design_tokens()

# Extract commonly used colors
PRIMARY = TOKENS['colors']['primary']['600']
PRIMARY_DARK = TOKENS['colors']['primary']['800']
TEXT_PRIMARY = TOKENS['colors']['text']['primary']
TEXT_SECONDARY = TOKENS['colors']['text']['secondary']
TEXT_MUTED = TOKENS['colors']['text']['muted']
BG_LIGHT = TOKENS['colors']['background']['light']
BG_LIGHTER = TOKENS['colors']['background'].get('lighter', '#f1f5f9')
BG_CARD = TOKENS['colors']['background']['card']
BORDER_LIGHT = TOKENS['colors']['border']['light']
BORDER_STRONG = TOKENS['colors']['border']['strong']
SUCCESS = TOKENS['colors']['success']

# ================= CONFIGURATION ================= #

def setup_page_config():
    st.set_page_config(
        page_title="PhotoTag Pro",
        layout="wide",
        initial_sidebar_state="collapsed",
        menu_items=None
    )
    
    # Dynamic CSS based on loaded tokens
    st.markdown(f"""
    <style>
    /* ===== Design Tokens (Loaded from tokens.json) ===== */
    :root {{
        --primary: {PRIMARY};
        --primary-dark: {PRIMARY_DARK};
        --text-primary: {TEXT_PRIMARY};
        --text-secondary: {TEXT_SECONDARY};
        --text-muted: {TEXT_MUTED};
        --bg-light: {BG_LIGHT};
        --bg-lighter: {BG_LIGHTER};
        --bg-card: {BG_CARD};
        --border: {BORDER_LIGHT};
        --border-strong: {BORDER_STRONG};
        --success: {SUCCESS};
    }}
    
    * {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
    }}
    
    /* ===== Main Container ===== */
    .main {{
        background: linear-gradient(135deg, {BG_LIGHT} 0%, {BG_LIGHTER} 100%);
        padding: 40px 20px !important;
    }}
    
    /* ===== Header Section ===== */
    .header-section {{
        text-align: center;
        margin-bottom: 50px;
        animation: fadeInDown 0.6s ease-out;
    }}
    
    .header-section h1 {{
        font-size: 2.5rem;
        font-weight: 800;
        color: {TEXT_PRIMARY};
        margin-bottom: 8px;
        letter-spacing: -0.5px;
    }}
    
    .header-section p {{
        font-size: 1.1rem;
        color: {TEXT_SECONDARY};
        margin: 0;
        font-weight: 400;
    }}
    
    /* ===== Card Styling ===== */
    .card {{
        background: {BG_CARD};
        border-radius: 12px;
        padding: 32px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        border: 1px solid {BORDER_LIGHT};
        margin-bottom: 24px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    .card:hover {{
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }}
    
    .card-title {{
        font-size: 1.3rem;
        font-weight: 700;
        color: {TEXT_PRIMARY};
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    
    /* ===== Step Indicator ===== */
    .step-indicator {{
        display: inline-block;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: {PRIMARY};
        color: white;
        font-weight: 700;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    
    /* ===== Form Elements ===== */
    .stTextArea textarea,
    .stTextInput input {{
        border-radius: 8px !important;
        border: 1.5px solid {BORDER_LIGHT} !important;
        padding: 12px 14px !important;
        font-size: 0.95rem !important;
        transition: all 0.2s !important;
    }}
    
    .stTextArea textarea:focus,
    .stTextInput input:focus {{
        border-color: {PRIMARY} !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
    }}
    
    /* ===== Button Styling ===== */
    .stButton > button {{
        background: linear-gradient(135deg, {PRIMARY} 0%, {PRIMARY_DARK} 100%);
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.2s !important;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3) !important;
    }}
    
    .stButton > button:hover {{
        box-shadow: 0 4px 16px rgba(37, 99, 235, 0.4) !important;
        transform: translateY(-1px);
    }}
    
    .stButton > button:active {{
        transform: translateY(0);
    }}
    
    /* ===== Alerts ===== */
    .stSuccess {{
        background: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        color: {SUCCESS} !important;
        border-radius: 8px !important;
    }}
    
    .stWarning {{
        background: rgba(245, 158, 11, 0.1) !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        color: #92400e !important;
        border-radius: 8px !important;
    }}
    
    /* ===== Preview Section ===== */
    .preview-container {{
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        background: {BG_CARD};
    }}
    
    .preview-label {{
        display: block;
        font-size: 0.85rem;
        font-weight: 600;
        color: {TEXT_SECONDARY};
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    /* ===== Layout Grid ===== */
    .two-column {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 32px;
        margin-bottom: 32px;
    }}
    
    @media (max-width: 1200px) {{
        .two-column {{
            grid-template-columns: 1fr;
        }}
    }}
    
    /* ===== Animations ===== */
    @keyframes fadeInDown {{
        from {{
            opacity: 0;
            transform: translateY(-20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    @keyframes slideUp {{
        from {{
            opacity: 0;
            transform: translateY(20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    .animate-in {{
        animation: slideUp 0.5s ease-out forwards;
    }}
    
    /* ===== Info Box ===== */
    .info-box {{
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.05) 0%, rgba(99, 102, 241, 0.05) 100%);
        border-left: 3px solid {PRIMARY};
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 24px;
    }}
    
    .info-box p {{
        margin: 0;
        color: {TEXT_PRIMARY};
        font-size: 0.95rem;
        line-height: 1.5;
    }}
    
    /* ===== Divider ===== */
    hr {{
        border: none;
        height: 1px;
        background: {BORDER_LIGHT};
        margin: 32px 0;
    }}
    </style>
    """, unsafe_allow_html=True)

setup_page_config()

# ================= UTILITY FUNCTIONS ================= #

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

# ================= MAIN APP ================= #

# Header
st.markdown("""
<div class="header-section">
    <h1>📸 PhotoTag Pro</h1>
    <p>Watermark foto lapangan dengan timestamp & lokasi secara otomatis</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <p><strong>💡 Tip:</strong> Foto diproses langsung di browser Anda. Data tidak tersimpan di server apa pun.</p>
</div>
""", unsafe_allow_html=True)

# Main Layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="step-indicator">1</span>Pilih Foto</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    
    if uploaded_file is not None:
        st.success("✅ Foto berhasil diunggah")
        st.image(Image.open(uploaded_file), use_container_width=True, caption="File Anda")
    else:
        st.info("📤 Seret & lepas foto atau klik untuk memilih")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="step-indicator">2</span>Detail Lokasi</div>', unsafe_allow_html=True)
    
    detail_lokasi = st.text_area(
        "Paste dari Google Maps atau tulis koordinat:", 
        placeholder="0.92584614S 100.36096574E\nNo. 1 Jalan Khatib Sulaiman\nFlamboyan Baru\nKecamatan Padang Barat\nKota Padang\nSumatera Barat",
        height=140,
        label_visibility="collapsed"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="step-indicator">3</span>Konfirmasi Detail</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        waktu_foto = ambil_waktu_exif(image)
        
        st.markdown("**Waktu Pengambilan**", help="Diambil otomatis dari EXIF, bisa diedit")
        waktu_input = st.text_input(
            "Waktu",
            value=waktu_foto,
            label_visibility="collapsed"
        )
        
        # Preview Info
        st.markdown("---")
        
        col_res, col_size = st.columns(2)
        with col_res:
            st.metric("Resolusi", f"{image.width}×{image.height}px")
        with col_size:
            size_mb = uploaded_file.size / (1024 * 1024)
            st.metric("Ukuran File", f"{size_mb:.2f}MB")
        
        # Action Button
        st.markdown("<br>", unsafe_allow_html=True)
        process_button = st.button(
            "🚀 Proses & Buat Watermark",
            use_container_width=True,
            type="primary"
        )
        
        if process_button and detail_lokasi.strip():
            with st.spinner("⏳ Sedang memproses foto..."):
                img_hasil = beri_watermark(image.copy(), waktu_input, detail_lokasi)
                st.session_state.img_processed = img_hasil
                st.rerun()
        elif process_button and not detail_lokasi.strip():
            st.error("⚠️ Masukkan detail lokasi terlebih dahulu")
    else:
        st.info("📸 Unggah foto terlebih dahulu untuk melanjutkan")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Preview & Download Section
if "img_processed" in st.session_state:
    st.markdown('<div class="card" style="margin-top: 40px;">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">✅ Hasil Akhir</div>', unsafe_allow_html=True)
    
    st.markdown('<span class="preview-label">Pratinjau</span>', unsafe_allow_html=True)
    st.image(st.session_state.img_processed, use_container_width=True)
    
    st.markdown("---")
    
    buf = io.BytesIO()
    st.session_state.img_processed.save(buf, format="JPEG", quality=95)
    byte_im = buf.getvalue()
    
    col_download, col_reset = st.columns(2)
    with col_download:
        st.download_button(
            label="📥 Unduh Foto (JPEG)",
            data=byte_im,
            file_name=f"tagged_{uploaded_file.name.replace(uploaded_file.name.split('.')[-1], 'jpg')}",
            mime="image/jpeg",
            use_container_width=True
        )
    
    with col_reset:
        if st.button("🔄 Buat Ulang", use_container_width=True):
            del st.session_state.img_processed
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ================= DEBUG INFO (Remove in production) ================= #
if st.checkbox("🔧 Debug: Show Loaded Tokens"):
    st.json(TOKENS, expanded=False)
    st.info(f"✅ Tokens loaded successfully from source")
