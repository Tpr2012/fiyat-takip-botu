import streamlit as st
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import pandas as pd
import datetime

# --- 1. AI SİNİR AĞI YAPILANDIRMASI ---
# Anahtarın başarıyla entegre edildi
GEMINI_KEY = "AIzaSyDu7faagD6mtZugXhhJ3PiIEdqZ20kThlA" 
genai.configure(api_key=GEMINI_KEY)

# Yapay zekaya uzman bir karakter tanımlıyoruz
generation_config = {
    "temperature": 0.75,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 1000,
}
# 'gemini-1.5-flash' hem daha hızlıdır hem de şu an en güncel stabil sürümdür.
model = genai.GenerativeModel('gemini-1.5-flash', generation_config=generation_config)

# --- 2. PREMIUM KARANLIK ARAYÜZ (NO-RGB STYLE) ---
st.set_page_config(page_title="TP AI | Intelligence", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #ffffff; }
    .stTextInput>div>div>input { background-color: #0d1117; color: white; border: 1px solid #30363d; }
    .ai-report { 
        background: linear-gradient(145deg, #0d1117, #161b22);
        border: 1px solid #ab7df8; padding: 25px; border-radius: 20px;
        line-height: 1.7; font-size: 16px; box-shadow: 0 10px 30px rgba(171, 125, 248, 0.1);
    }
    .stButton>button {
        background: linear-gradient(90deg, #58a6ff, #ab7df8);
        color: white; border: none; padding: 15px; border-radius: 10px;
        font-weight: 800; font-size: 16px; width: 100%; transition: 0.4s;
    }
    .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(88, 166, 255, 0.3); }
    .metric-box { background: #0d1117; border: 1px solid #30363d; padding: 15px; border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# --- 3. AKILLI VERİ TOPLAMA ---
def interneti_tara(sorgu):
    """DuckDuckGo üzerinden engelsiz veri toplar."""
    url = f"https://duckduckgo.com/html/?q={sorgu}+satın+al+fiyat"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    bulunanlar = []
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, "html.parser")
        for a in soup.find_all('a', class_='result__url', href=True):
            if "http" in a['href'] and not "duckduckgo" in a['href']:
                bulunanlar.append(a['href'])
            if len(bulunanlar) >= 6: break
    except: pass
    return bulunanlar

# --- 4. ANA KONTROL PANELİ ---
st.markdown("<h1 style='text-align: center;'>🧠 TP AI <span style='color:#ab7df8'>NEURAL</span> GENESIS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8b949e;'>Yapay Zeka Destekli Stratejik Piyasa Analizi</p>", unsafe_allow_html=True)

with st.container():
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        urun_sorgu = st.text_input("", placeholder="Analiz edilecek ürün veya sorunuzu yazın...")
    with col_btn:
        st.write(" ") # Boşluk
        baslat = st.button("ANALİZ ET 🚀")

    if baslat and urun_sorgu:
        with st.spinner('TP AI Zihinsel Bağlantı Kuruyor...'):
            # Finansal Veri (Dolar)
            try:
                kur = float(yf.download("USDTRY=X", period="1d", interval="1m")['Close'].iloc[-1])
            except: kur = 32.95
            
            # İnternet Verisi
            kaynaklar = interneti_tara(urun_sorgu)
            
            # YAPAY ZEKA STRATEJİ RAPORU
            st.divider()
            
            # Gemini'ye giden 'Süper Prompt'
            prompt = f"""
            Sen TP AI, uzman bir piyasa analistisin. 
            Kullanıcı sorusu: {urun_sorgu}
            Güncel Kur: {kur:.2f} TL
            Tespit Edilen Linkler: {kaynaklar}
            
            Görevin: Kullanıcıya bu ürünün piyasa durumunu, dolar bazlı değerini ve 
            'şimdi mi almalı yoksa beklemeli mi' sorusunun cevabını içeren, 
            samimi ama profesyonel bir rapor sunmak. 
            Eğer linklerde fiyatlar varsa bunları yorumla. 
            Türkiye ekonomisindeki kur risklerini de göz önüne al.
            """
            
            try:
                response = model.generate_content(prompt)
                st.markdown("### 🤖 TP AI Stratejik Raporu")
                st.markdown(f'<div class="ai-report">{response.text}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"AI Modülünde bir hata oluştu: {e}")

            # Metrik Paneli
            st.write(" ")
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown('<div class="metric-box">', unsafe_allow_html=True)
                st.metric("Canlı Kur", f"{kur:.2f} TL")
                st.markdown('</div>', unsafe_allow_html=True)
            with m2:
                st.markdown('<div class="metric-box">', unsafe_allow_html=True)
                st.metric("Kaynak Sayısı", len(kaynaklar))
                st.markdown('</div>', unsafe_allow_html=True)
            with m3:
                st.markdown('<div class="metric-box">', unsafe_allow_html=True)
                st.metric("Zeka Durumu", "Optimal")
                st.markdown('</div>', unsafe_allow_html=True)

            # Kaynaklar
            with st.expander("📍 İncelenen Dijital Kaynaklar"):
                for k in kaynaklar:
                    st.write(f"- [{k.split('/')[2]}]({k})")

# --- 5. ALT BİLGİ ---
st.markdown("---")
st.caption(f"TP AI v5.5 | Neural Engine Aktif | {datetime.datetime.now().strftime('%H:%M:%S')}")
