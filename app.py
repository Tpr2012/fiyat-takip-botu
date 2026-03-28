import streamlit as st
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import google.generativeai as genai
import pandas as pd
import datetime

# --- 1. AI BEYİN AYARI ---
# Buraya Google AI Studio'dan aldığın keyi yapıştır
GEMINI_KEY = "AIzaSyDu7faagD6mtZugXhhJ3PiIEdqZ20kThlA" 
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

# --- 2. GÖRSEL TASARIM (PREMIUM) ---
st.set_page_config(page_title="TP AI | Neural Genesis", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #ffffff; }
    .ai-card { 
        background: linear-gradient(145deg, #0d1117, #161b22);
        border: 1px solid #30363d; padding: 30px; border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5); border-top: 2px solid #58a6ff;
    }
    .chat-bubble { 
        background: #1c2128; border-radius: 15px; padding: 20px;
        border-left: 5px solid #ab7df8; font-style: italic; margin-bottom: 20px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #58a6ff, #ab7df8);
        border: none; color: white; padding: 15px; border-radius: 12px;
        font-weight: 900; font-size: 18px; transition: 0.5s;
    }
    .stButton>button:hover { letter-spacing: 2px; box-shadow: 0 0 20px #58a6ff; }
</style>
""", unsafe_allow_html=True)

# --- 3. ZEKA FONKSİYONLARI ---

def ai_sohbet_motoru(urun, fiyatlar, kur):
    """Gerçek Yapay Zeka Analizi yapar."""
    prompt = f"""
    Sen TP AI isimli gelişmiş bir piyasa analiz yapay zekasısın. 
    Kullanıcı '{urun}' ürününü aratıyor. Güncel Dolar Kuru: {kur} TL. 
    İnternette bulunan kaynaklar: {fiyatlar}.
    Lütfen bu verileri analiz et ve kullanıcıya (Düzce'deki bir öğrenci dostun gibi) 
    stratejik bir alım tavsiyesi ver. Doların etkisini ve ürünün değerini yorumla.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return "Yapay zeka modülü şu an meşgul, ama veriler aşağıda listelendi."

def radar_taramasi(urun):
    """Tüm interneti tarar."""
    sorgu = f"{urun} fiyat satın al"
    linkler = []
    try:
        for link in search(sorgu, num_results=8, lang="tr", sleep_interval=1):
            linkler.append(link)
    except: pass
    return linkler

# --- 4. ANA PANEL ---
st.markdown("<h1 style='text-align: center;'>🧠 TP AI <span style='color:#58a6ff'>NEURAL</span> GENESIS</h1>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="ai-card">', unsafe_allow_html=True)
    
    urun_input = st.text_input("Yapay Zekaya Ne Sormak İstersin?", placeholder="Örn: En ucuz RTX 4060 nerede ve şimdi almalı mıyım?")
    
    if st.button("SİSTEMİ ANALİZE GÖNDER 🚀"):
        if urun_input:
            with st.spinner('Neural Network Bağlanıyor...'):
                # Verileri Topla
                kur_data = yf.download("USDTRY=X", period="1d", interval="1m")
                kur = float(kur_data['Close'].iloc[-1]) if not kur_data.empty else 32.80
                
                bulunan_linkler = radar_taramasi(urun_input)
                
                # Yapay Zeka Yorumu
                st.markdown("### 🤖 TP AI Karar Mekanizması")
                ai_cevap = ai_sohbet_motoru(urun_input, bulunan_linkler, kur)
                st.markdown(f'<div class="chat-bubble">{ai_cevap}</div>', unsafe_allow_html=True)
                
                # Veri Tablosu
                col1, col2 = st.columns(2)
                col1.metric("Anlık Kur", f"{kur:.2f} TL")
                col2.metric("Tarama Verisi", f"{len(bulunan_linkler)} Kaynak")
                
                st.divider()
                st.markdown("### 🛰️ İnternet İzleri")
                for l in bulunan_linkler:
                    st.markdown(f"- [Kaynağa Git]({l})")
        else:
            st.warning("Lütfen bir ürün veya soru gir.")
    st.markdown('</div>', unsafe_allow_html=True)
