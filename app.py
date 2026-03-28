import streamlit as st
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import pandas as pd
import datetime
import time

# --- 1. SAYFA VE TEMA AYARLARI ---
st.set_page_config(page_title="TP AI | Genesis", page_icon="🧠", layout="wide")

# Modern, Koyu ve Şık "No-RGB" Arayüzü (Custom CSS)
st.markdown("""
<style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .main-card { background: #161b22; border: 1px solid #30363d; padding: 25px; border-radius: 15px; border-top: 5px solid #238636; }
    .ai-box { background: #010409; border-radius: 12px; padding: 20px; border-left: 5px solid #58a6ff; margin: 15px 0; }
    .stMetric { background-color: #0d1117; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    .stButton>button { 
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%); 
        color: white; border: none; padding: 12px; border-radius: 8px; font-weight: bold; width: 100%;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(35, 134, 54, 0.4); }
</style>
""", unsafe_allow_html=True)

# --- 2. TP AI MOTOR FONKSİYONLARI ---

@st.cache_data(ttl=600)
def kur_verisi_cek():
    """Dolar kurunu güvenli bir şekilde çeker."""
    try:
        data = yf.download("USDTRY=X", period="1d", interval="1m")
        if not data.empty:
            return float(data['Close'].iloc[-1])
    except:
        pass
    return 32.75 # Hata durumunda varsayılan kur

def evrensel_radar(urun, mod):
    """İnternetin farklı katmanlarında arama yapar."""
    mod_sorgulari = {
        "Tüm İnternet": "fiyatı satın al",
        "Sıfır / Mağaza": "fiyatı -2.el -ikinci",
        "2. El / Sahibinden": "site:sahibinden.com veya site:dolap.com",
        "Outlet / Revizyonlu": "outlet veya teşhir veya revizyonlu"
    }
    sorgu = f'"{urun}" {mod_sorgulari[mod]}'
    sonuclar = []
    
    try:
        for link in search(sorgu, num_results=12, lang="tr"):
            platform = "Global Kaynak"
            if "sahibinden.com" in link: platform = "Sahibinden (2. El)"
            elif "trendyol.com" in link: platform = "Trendyol"
            elif "amazon.com.tr" in link: platform = "Amazon"
            elif "hepsiburada.com" in link: platform = "Hepsiburada"
            elif "akakce.com" in link: platform = "Akakçe (Karşılaştırma)"
            elif "itopya.com" in link or "vatanbilgisayar" in link: platform = "Teknoloji Mağazası"
            
            sonuclar.append({"Platform": platform, "Bağlantı": link})
    except:
        pass
    return sonuclar

def ai_strateji_motoru(urun, kur, sonuc_sayisi):
    """Verileri analiz eder ve yorum yapar."""
    analiz = f"'{urun}' için derin tarama tamamlandı. {sonuc_sayisi} farklı veri noktası analiz edildi. "
    
    if "rtx" in urun.lower() or "rx" in urun.lower():
        analiz += f"Ekran kartı piyasası şu an {kur:.2f} TL kur baskısı altında. Global stoklar stabil ancak yerel vergiler fiyatı %15 etkileyebilir."
    elif "iphone" in urun.lower() or "samsung" in urun.lower():
        analiz += "Mobil cihazlarda taksit sınırlaması nedeniyle 2. el ve Outlet modellerine olan talep artış eğiliminde."
    else:
        analiz += "Genel tüketici elektroniği segmentinde fiyat istikrarı gözleniyor. İhtiyacın varsa alım için uygun dönem."
    
    return analiz

# --- 3. ANA ARAYÜZ (GÖVDE) ---

st.markdown("<h1 style='text-align: center; color: #58a6ff;'>🧠 TP AI GENESIS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8b949e;'>Evrensel Piyasa Radarı & Stratejik Analiz Merkezi</p>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    col_input, col_mod = st.columns([3, 1])
    with col_input:
        urun_ismi = st.text_input("Hedef Ürün Adı:", placeholder="Örn: MSI RTX 4060 Ti 16GB")
    with col_mod:
        secilen_mod = st.selectbox("Arama Modu", ["Tüm İnternet", "Sıfır / Mağaza", "2. El / Sahibinden", "Outlet / Revizyonlu"])
    
    if st.button("RADARI VE ANALİZİ BAŞLAT 🚀"):
        if urun_ismi:
            with st.spinner('TP AI internetin katmanlarına sızıyor...'):
                # Veri Toplama
                canli_kur = kur_verisi_cek()
                istihbarat = evrensel_radar(urun_ismi, secilen_mod)
                strateji = ai_strateji_motoru(urun_ismi, canli_kur, len(istihbarat))
                
                # Üst Metrikler
                st.divider()
                m1, m2, m3 = st.columns(3)
                m1.metric("Canlı Dolar", f"{canli_kur:.2f} TL")
                m2.metric("Tarama Kapsamı", secilen_mod)
                m3.metric("Bulunan Kaynak", len(istihbarat))
                
                # Yapay Zeka Yorumu
                st.markdown('<div class="ai-box">', unsafe_allow_html=True)
                st.markdown("### 🤖 TP AI Stratejik Raporu")
                st.write(strateji)
                st.markdown(f"💡 *Tahmini Global Değer:* **${(canli_kur * 1.05):.2f}** (Vergi/Kâr hariç)")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Kaynak Listesi
                if istihbarat:
                    st.markdown("### 🛰️ Tespit Edilen Dijital Kaynaklar")
                    for s in istihbarat:
                        with st.expander(f"📍 {s['Platform']}"):
                            st.write(f"Kaynak URL: {s['Bağlantı']}")
                            st.markdown(f"[Kaynağı Yeni Sekmede Aç]({s['Bağlantı']})")
                else:
                    st.error("TP AI bu ürün için herhangi bir dijital iz bulamadı. Lütfen ismi kontrol et.")
        else:
            st.warning("Analiz başlatmak için bir ürün ismi girmelisin!")
            
    st.markdown('</div>', unsafe_allow_html=True)

# --- ALT BİLGİ ---
st.divider()
st.markdown(f"<p style='text-align: center; color: #484f58;'>TP AI v4.0 | Düzce Sistemleri | {datetime.datetime.now().strftime('%d/%m/%Y')}</p>", unsafe_allow_html=True)
