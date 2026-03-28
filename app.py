import streamlit as st
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import time

# --- SAYFA AYARLARI (Geniş Ekran ve İkon) ---
st.set_page_config(page_title="Kumru Piyasalar", page_icon="🦅", layout="wide", initial_sidebar_state="collapsed")

# --- MİNİMALİST VE ŞIK TASARIM (Özel CSS) ---
st.markdown("""
<style>
    /* Ana arka planı tam siyah/koyu gri arası yap */
    .stApp { background-color: #0E1117; }
    /* Metrik kutularını şıklaştır */
    div[data-testid="metric-container"] {
        background-color: #1E2127;
        border: 1px solid #2D3139;
        padding: 5% 10% 5% 10%;
        border-radius: 10px;
        border-left: 5px solid #00C853;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    /* Arama butonunu özelleştir */
    div.stButton > button:first-child {
        background-color: #2962FF;
        color: white;
        border-radius: 8px;
        border: none;
        width: 100%;
        font-weight: bold;
    }
    div.stButton > button:first-child:hover {
        background-color: #1565C0;
        border: 1px solid white;
    }
</style>
""", unsafe_allow_html=True)

# --- BAŞLIK ALANI ---
st.markdown("<h1 style='text-align: center; color: #FFFFFF;'>🦅 Kumru Fiyat İstihbaratı</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8B949E;'>Minimalist, hızlı ve yapay zeka destekli piyasa analizi.</p>", unsafe_allow_html=True)
st.divider()

# --- FONKSİYONLAR ---
def urun_linki_bul(urun_adi):
    sorgu = f"site:akakce.com {urun_adi}"
    try:
        for link in search(sorgu, num_results=1):
            if "akakce.com" in link:
                return link
    except:
        return None
    return None

def fiyat_cek(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, "html.parser")
        fiyat_etiketi = soup.select_one("span.pt_v8") or soup.select_one(".v8p")
        if fiyat_etiketi:
            fiyat_text = fiyat_etiketi.text.strip()
            temiz = "".join(c for c in fiyat_text if c.isdigit() or c in ",.")
            if "," in temiz and "." in temiz: temiz = temiz.replace(".", "").replace(",", ".")
            elif "," in temiz: temiz = temiz.replace(",", ".")
            return float(temiz)
    except:
        return None
    return None

@st.cache_data(ttl=3600) # Veriyi 1 saat hafızada tutarak hızı artırır
def ekonomi_verisi():
    dolar = yf.download("USDTRY=X", period="7d", interval="1d")['Close']
    kur = float(dolar.iloc[-1])
    return kur, dolar

# --- SEKME (TAB) SİSTEMİ ---
tab1, tab2, tab3 = st.tabs(["🔍 Akıllı Arama", "📈 Canlı Ekonomi", "⚙️ Sistem Durumu"])

with tab1:
    st.markdown("### Ne arıyoruz?")
    # Placeholder içine sana tanıdık gelecek test ürünleri koyduk
    urun_ismi = st.text_input("", placeholder="Örn: NVIDIA RTX 4060, LEGO Technic Mercedes, Beşiktaş Forması...")
    
    if st.button("🚀 Derin Aramayı Başlat"):
        if urun_ismi:
            with st.spinner('Kumru interneti tarıyor, lütfen bekle...'):
                time.sleep(1) # Animasyonun görünmesi için kısa bir es
                link = urun_linki_bul(urun_ismi)
                
                if link:
                    fiyat = fiyat_cek(link)
                    kur, _ = ekonomi_verisi()
                    
                    st.success("✅ Hedef tespit edildi!")
                    
                    # 3'lü Şık Metrik Paneli
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if fiyat:
                            st.metric(label="En Düşük Fiyat", value=f"{fiyat:,.2f} TL")
                        else:
                            st.metric(label="Durum", value="Fiyat Gizli")
                            
                    with col2:
                        if fiyat and kur:
                            st.metric(label="Dolar Karşılığı", value=f"${(fiyat/kur):,.2f}")
                        else:
                            st.metric(label="Dolar Karşılığı", value="Hesaplanamadı")
                            
                    with col3:
                        st.metric(label="Ürün Bağlantısı", value="Gitmek İçin Tıkla", help=link)
                        st.markdown(f"[🛒 Mağazaya Git]({link})")
                        
                else:
                    st.error("❌ Ürün bulunamadı. Lütfen daha belirgin bir isim yaz.")
        else:
            st.warning("Lütfen arama kutusuna bir şey yaz.")

with tab2:
    st.markdown("### 💵 Dolar/TL Son 7 Günlük Seyir")
    try:
        kur, dolar_grafik = ekonomi_verisi()
        st.metric("Anlık Dolar Kuru", f"{kur:.2f} TL")
        st.area_chart(dolar_grafik, color="#00C853") # İçi dolu, şık yeşil grafik
    except:
        st.error("Ekonomi verileri şu an çekilemiyor.")

with tab3:
    st.markdown("### 🖥️ Sunucu Bilgileri")
    st.info("Kumru AI Fiyat Modülü aktif olarak çalışıyor.")
    st.write("- **Geliştirici:** Düzce Merkezli Sistemler")
    st.write("- **Arayüz Tipi:** Minimalist, No-RGB")
    st.write("- **Durum:** %100 Çevrimiçi")
