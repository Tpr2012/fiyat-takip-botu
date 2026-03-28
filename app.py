import streamlit as st
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import pandas as pd
import datetime

# --- 1. AI SİNİR AĞI YAPILANDIRMASI ---
# Senin sağladığın güncel API Key
GEMINI_KEY = "AIzaSyDu7faagD6mtZugXhhJ3PiIEdqZ20kThlA" 
genai.configure(api_key=GEMINI_KEY)

# Yapay zekaya uzman bir karakter ve güncel model tanımlıyoruz
# Not: 404 hatasını önlemek için en güncel stabil model ismini kullanıyoruz.
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 1024,
}

try:
    # En hızlı ve güncel model: gemini-1.5-flash
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config
    )
except:
    # Hata durumunda alternatif (yedek) model
    model = genai.GenerativeModel(
        model_name="gemini-pro",
        generation_config=generation_config
    )

# --- 2. PREMIUM KARANLIK ARAYÜZ (NO-RGB STYLE) ---
st.set_page_config(page_title="TP AI | Intelligence", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #ffffff; }
    .stTextInput>div>div>input { background-color: #0d1117; color: white; border: 1px solid #30363d; border-radius: 10px; }
    .ai-report { 
        background: linear-gradient(145deg, #0d1117, #161b22);
        border: 1px solid #ab7df8; padding: 25px; border-radius: 20px;
        line-height: 1.7; font-size: 16px; box-shadow: 0 10px 30px rgba(171, 125, 248, 0.1);
    }
    .stButton>button {
        background: linear-gradient(90deg, #58a6ff, #ab7df8);
        color: white; border: none; padding: 15px; border-radius: 12px;
        font-weight: 800; font-size: 16px; width: 100%; transition: 0.4s;
    }
    .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(88, 166, 255, 0.3); }
    .metric-box { background: #0d1117; border: 1px solid #30363d; padding: 20px; border-radius: 15px; text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- 3. AKILLI VERİ TOPLAMA MOTORU ---
def interneti_tara(sorgu):
    """DuckDuckGo üzerinden engelsiz ve hızlı veri toplar."""
    url = f"https://duckduckgo.com/html/?q={sorgu}+satın+al+fiyat+türkiye"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    bulunanlar = []
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, "html.parser")
        # DuckDuckGo'nun HTML yapısına uygun link çekme
        for a in soup.find_all('a', class_='result__url', href=True):
            link = a['href']
            if "http" in link and not "duckduckgo" in link:
                bulunanlar.append(link)
            if len(bulunanlar) >= 7: break
    except:
        pass
    return bulunanlar

# --- 4. ANA KONTROL PANELİ ---
st.markdown("<h1 style='text-align: center;'>🧠 TP AI <span style='color:#ab7df8'>NEURAL</span> GENESIS v6.0</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8b949e;'>Düzce Çıkışlı Yerli Piyasa İstihbarat Ağı</p>", unsafe_allow_html=True)

with st.container():
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        urun_sorgu = st.text_input("", placeholder="Ürün ismi girin veya piyasa sorusu sorun...")
    with col_btn:
        st.write(" ") # Hizalama için
        baslat = st.button("ANALİZ ET 🚀")

    if baslat and urun_sorgu:
        with st.spinner('Neural Network Bağlantısı Kuruluyor...'):
            # Finansal Veri (Dolar/TRY)
            try:
                # yfinance bazen hata verebilir, bu yüzden garantiye alıyoruz
                kur_verisi = yf.download("USDTRY=X", period="1d", interval="1m")
                kur = float(kur_verisi['Close'].iloc[-1])
            except:
                kur = 33.15 # Hata durumunda varsayılan (yaklaşık) kur
            
            # İnternet Verisi (Yeni Radar)
            kaynaklar = interneti_tara(urun_sorgu)
            
            # YAPAY ZEKA STRATEJİ RAPORU
            st.divider()
            
            # Gemini'ye giden 'Süper Prompt'
            prompt = f"""
            Sen TP AI, Türkiye piyasasında uzman bir teknoloji ve ekonomi analistisin. 
            Ürün/Soru: {urun_sorgu}
            Güncel Dolar Kuru: {kur:.2f} TL
            Bulunan İnternet Kaynakları: {kaynaklar}
            
            Görevin: 
            1. Ürünün piyasa değerini dolar kuruyla karşılaştır. 
            2. Linklerdeki sitelere (varsa) bakarak bir fiyat analizi yap.
            3. Kullanıcıya net bir 'Al' veya 'Bekle' tavsiyesi ver. 
            4. Cevabını samimi, zeki ve profesyonel bir dille yaz.
            """
            
            try:
                response = model.generate_content(prompt)
                st.markdown("### 🤖 TP AI Stratejik Raporu")
                st.markdown(f'<div class="ai-report">{response.text}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"AI Modülünde bir hata oluştu. Lütfen API Key'i veya internet bağlantısını kontrol et. Hata: {e}")

            # Metrik Paneli
            st.write(" ")
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f'<div class="metric-box"><h4>Dolar</h4><h2 style="color:#58a6ff">{kur:.2f} TL</h2></div>', unsafe_allow_html=True)
            with m2:
                st.markdown(f'<div class="metric-box"><h4>Kaynak</h4><h2 style="color:#ab7df8">{len(kaynaklar)} Site</h2></div>', unsafe_allow_html=True)
            with m3:
                st.markdown(f'<div class="metric-box"><h4>Zeka</h4><h2 style="color:#238636">1.5 Flash</h2></div>', unsafe_allow_html=True)

            # Kaynaklar
            if kaynaklar:
                with st.expander("📍 İncelenen Web Kaynakları"):
                    for k in kaynaklar:
                        st.write(f"- [{k.split('/')[2] if '/' in k else 'Site'}]({k})")

# --- 5. ALT BİLGİ ---
st.markdown("---")
st.caption(f"TP AI v6.0 | Düzce Sistemleri | {datetime.datetime.now().strftime('%H:%M:%S')}")
