import streamlit as st
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import pandas as pd
import datetime

# --- 1. AI SİNİR AĞI VE GÜVENLİ MODEL YÜKLEME ---
GEMINI_KEY = "AIzaSyDu7faagD6mtZugXhhJ3PiIEdqZ20kThlA" 
genai.configure(api_key=GEMINI_KEY)

generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "max_output_tokens": 1024,
}

# HATA ALMAMAK İÇİN DİNAMİK MODEL SEÇİCİ
@st.cache_resource
def model_yukle():
    modeller = ["gemini-1.5-flash", "gemini-pro", "models/gemini-1.5-flash", "models/gemini-pro"]
    for m_ad in modeller:
        try:
            m = genai.GenerativeModel(model_name=m_ad, generation_config=generation_config)
            # Test amaçlı küçük bir çağrı (opsiyonel)
            return m, m_ad
        except:
            continue
    return None, "Hata"

model, aktif_model_adi = model_yukle()

# --- 2. PREMIUM KARANLIK ARAYÜZ ---
st.set_page_config(page_title="TP AI | Genesis", page_icon="🧠", layout="wide")

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

# --- 3. KESİNTİSİZ VERİ TOPLAMA ---
def interneti_tara(sorgu):
    url = f"https://duckduckgo.com/html/?q={sorgu}+fiyat+satın+al+türkiye"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    bulunanlar = []
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, "html.parser")
        for a in soup.find_all('a', class_='result__url', href=True):
            link = a['href']
            if "http" in link and not "duckduckgo" in link:
                bulunanlar.append(link)
            if len(bulunanlar) >= 6: break
    except: pass
    return bulunanlar

# --- 4. ANA PANEL ---
st.markdown("<h1 style='text-align: center;'>🧠 TP AI <span style='color:#ab7df8'>GENESIS</span> v6.5</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #8b949e;'>Aktif Modül: <b>{aktif_model_adi}</b></p>", unsafe_allow_html=True)

with st.container():
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        urun_sorgu = st.text_input("", placeholder="Analiz edilecek ürün veya piyasa sorusu...")
    with col_btn:
        st.write(" ")
        baslat = st.button("ANALİZ ET 🚀")

    if baslat and urun_sorgu:
        with st.spinner('TP AI Zihinsel Veri İşliyor...'):
            # Kur Verisi
            try:
                kur = float(yf.download("USDTRY=X", period="1d", interval="1m")['Close'].iloc[-1])
            except: kur = 33.20
            
            # Web Verisi
            kaynaklar = interneti_tara(urun_sorgu)
            
            # AI Analizi
            st.divider()
            if model:
                prompt = f"Ürün: {urun_sorgu}. Kur: {kur:.2f} TL. Kaynaklar: {kaynaklar}. Bu verileri analiz et, TL bazlı yorum yap ve samimi bir dille alım tavsiyesi ver."
                try:
                    response = model.generate_content(prompt)
                    st.markdown("### 🤖 TP AI Stratejik Raporu")
                    st.markdown(f'<div class="ai-report">{response.text}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Yapay Zeka yanıt veremedi. Detay: {e}")
            else:
                st.error("Üzgünüm, şu an hiçbir AI modeliyle bağlantı kurulamadı. Lütfen API anahtarını kontrol et.")

            # Metrikler
            st.write(" ")
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f'<div class="metric-box"><h4>Canlı Kur</h4><h2 style="color:#58a6ff">{kur:.2f} TL</h2></div>', unsafe_allow_html=True)
            with m2:
                st.markdown(f'<div class="metric-box"><h4>Kaynak</h4><h2 style="color:#ab7df8">{len(kaynaklar)} Site</h2></div>', unsafe_allow_html=True)
            with m3:
                st.markdown(f'<div class="metric-box"><h4>Zeka</h4><h2 style="color:#238636">Aktif</h2></div>', unsafe_allow_html=True)

            with st.expander("📍 İncelenen Kaynaklar"):
                for k in kaynaklar: st.write(f"- {k}")

st.markdown("---")
st.caption(f"TP AI v6.5 | Düzce | {datetime.datetime.now().strftime('%H:%M:%S')}")
