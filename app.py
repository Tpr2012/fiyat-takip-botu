import streamlit as st
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import pandas as pd
import datetime

# --- 1. AI BEYİN AYARI ---
# Buraya Google AI Studio'dan aldığın Key'i yapıştır (Eğer yoksa tırnak içi boş kalsın)
GEMINI_KEY = "AIzaSyDu7faagD6mtZugXhhJ3PiIEdqZ20kThlA" 
if GEMINI_KEY != "AIzaSyDu7faagD6mtZugXhhJ3PiIEdqZ20kThlA":
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    model = None

# --- 2. GÖRSEL TASARIM (ULTRA MODERN) ---
st.set_page_config(page_title="TP AI | Genesis", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #ffffff; }
    .ai-card { 
        background: linear-gradient(145deg, #0d1117, #161b22);
        border: 1px solid #30363d; padding: 25px; border-radius: 20px;
        border-top: 3px solid #58a6ff;
    }
    .stButton>button {
        background: linear-gradient(90deg, #238636, #2ea043);
        border: none; color: white; padding: 12px; border-radius: 10px;
        font-weight: 900; width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px #238636; }
</style>
""", unsafe_allow_html=True)

# --- 3. YIKILMAZ ARAMA MOTORU (DUCKDUCKGO TABANLI) ---
def hizli_radar(urun):
    """Google engeline takılmayan alternatif arama motoru."""
    # DuckDuckGo HTML arama linki
    url = f"https://duckduckgo.com/html/?q={urun}+fiyat+satın+al+site:com.tr"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    bulunan_linkler = []
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, "html.parser")
        
        # Sayfadaki tüm linkleri tara
        for a in soup.find_all('a', class_='result__url', href=True):
            link = a['href']
            # Reklam olmayan ve alışveriş sitelerine benzeyenleri al
            if "http" in link and not "duckduckgo" in link:
                bulunan_linkler.append(link)
                if len(bulunan_linkler) >= 7: break # İlk 7 sonucu al
    except Exception as e:
        st.error(f"Bağlantı Hatası: {e}")
    
    return bulunan_linkler

# --- 4. ANA PANEL ---
st.markdown("<h1 style='text-align: center;'>🧠 TP AI <span style='color:#58a6ff'>GENESIS</span> v5.1</h1>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="ai-card">', unsafe_allow_html=True)
    
    urun_input = st.text_input("Hangi ürünü analiz edelim?", placeholder="Örn: Samsung Galaxy Watch 7")
    
    if st.button("ANALİZİ BAŞLAT 🚀"):
        if urun_input:
            with st.spinner('TP AI Piyasaya Sızıyor...'):
                # 1. Kur Çek
                try:
                    kur_data = yf.download("USDTRY=X", period="1d", interval="1m")
                    kur = float(kur_data['Close'].iloc[-1])
                except: kur = 32.85
                
                # 2. Ürünleri Bul (YENİ SİSTEM)
                linkler = hizli_radar(urun_input)
                
                # 3. Sonuçları Göster
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("### 🛰️ Tespit Edilen Kaynaklar")
                    if linkler:
                        for l in linkler:
                            st.markdown(f"- [Mağaza Linki]({l})")
                    else:
                        st.warning("⚠️ İnternet korumaları çok sıkı. Lütfen 1 dakika sonra tekrar dene veya farklı bir isim yaz.")
                
                with col2:
                    st.metric("Canlı Dolar", f"{kur:.2f} TL")
                    st.info(f"**TP AI Notu:** {urun_input} için global tarama yapıldı. Şu anki kurla alım stratejini belirleyebilirsin.")
                    
                    if model:
                        try:
                            res = model.generate_content(f"{urun_input} ürünü ve {kur} TL kur hakkında kısa bir yorum yap.")
                            st.success(f"🤖 Yapay Zeka: {res.text}")
                        except: pass
        else:
            st.warning("Lütfen bir isim yaz.")
    st.markdown('</div>', unsafe_allow_html=True)
