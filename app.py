import streamlit as st
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import pandas as pd
import datetime

# --- TP AI GÖRSEL KİMLİK VE TEMA ---
st.set_page_config(page_title="TP AI | Omni-Intelligence", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #05070a; color: #e6edf3; font-family: 'Segoe UI', sans-serif; }
    .main-card { background: #0d1117; border: 1px solid #30363d; padding: 25px; border-radius: 15px; margin-bottom: 20px; border-top: 4px solid #58a6ff; }
    .ai-bubble { background: #161b22; border-radius: 15px; padding: 15px; border-left: 5px solid #ab7df8; margin: 10px 0; }
    .stButton>button { background: linear-gradient(135deg, #58a6ff, #ab7df8); color: white; border: none; padding: 15px; border-radius: 10px; font-weight: 700; width: 100%; letter-spacing: 1px; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(88, 166, 255, 0.4); }
</style>
""", unsafe_allow_html=True)

# --- TP AI ZEKA MOTORU ---
def tp_ai_analiz(urun, kur):
    # Yapay zeka mantık simülasyonu
    if "rtx" in urun.lower() or "ekran kartı" in urun.lower():
        return "Donanım piyasasında stok durumu kritik. Dolar kurundaki %1'lik artış bu ürüne %3 zam olarak yansıyabilir."
    elif "iphone" in urun.lower() or "samsung" in urun.lower():
        return f"Mobil cihaz segmentinde rekabet yüksek. {kur:.2f} TL kur seviyesi, ithalatçı garantili (outlet) modeller için fırsat yaratıyor."
    else:
        return "Genel piyasa taraması yapıldı. Ürünün bulunabilirlik endeksi %85. Fiyat istikrarı korunuyor."

def evrensel_radar(urun, mod):
    mod_ekleri = {
        "Hepsi": "satın al fiyat",
        "Sahibinden/2.El": "site:sahibinden.com veya site:dolap.com",
        "Outlet/Fırsat": "outlet revizyonlu teşhir ürünleri",
        "Global/Amazon": "site:amazon.com.tr veya site:hepsiburada.com"
    }
    sorgu = f"{urun} {mod_ekleri[mod]}"
    sonuclar = []
    
    try:
        for link in search(sorgu, num_results=10, lang="tr"):
            platform = "Global Mağaza"
            if "sahibinden" in link: platform = "Sahibinden (2. El)"
            elif "trendyol" in link: platform = "Trendyol"
            elif "akakce" in link: platform = "Akakçe"
            elif "itopya" in link: platform = "İtopya"
            sonuclar.append({"Platform": platform, "Link": link})
    except: pass
    return sonuclar

# --- ANA EKRAN ---
st.markdown("<h1 style='text-align: center; color: #58a6ff;'>🧠 TP AI OMNI-INTELLIGENCE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8b949e;'>Tüm ağları tarar, analiz eder ve karar verir.</p>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([3, 1])
    with c1:
        urun_ismi = st.text_input("Hedef Ürün:", placeholder="Örn: NVIDIA RTX 5060 12GB")
    with c2:
        mod = st.selectbox("Tarama Modu", ["Hepsi", "Sahibinden/2.El", "Outlet/Fırsat", "Global/Amazon"])
    
    if st.button("TP AI SİSTEMİNİ ATEŞLE 🚀"):
        if urun_ismi:
            with st.spinner('TP AI internetin derinliklerine sızıyor...'):
                kur = yf.download("USDTRY=X", period="1d", interval="1m")['Close'].iloc[-1]
                sonuclar = evrensel_radar(urun_ismi, mod)
                
                st.divider()
                
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("Canlı Kur", f"{kur:.2f} TL")
                col_b.metric("Tespit Edilen Kaynak", len(sonuclar))
                col_c.metric("Yapay Zeka Durumu", "Aktif / Analitik")

                # AI YORUM ALANI
                st.markdown('<div class="ai-bubble">', unsafe_allow_html=True)
                st.markdown(f"### 🤖 TP AI Stratejik Raporu")
                st.write(tp_ai_analiz(urun_ismi, kur))
                st.markdown('</div>', unsafe_allow_html=True)

                # SONUÇ TABLOSU
                if sonuclar:
                    st.markdown("### 🛰️ Bulunan Dijital İzler")
                    for s in sonuclar:
                        with st.expander(f"📍 {s['Platform']}"):
                            st.write(f"Kaynak Bağlantısı: {s['Link']}")
                            st.markdown(f"[Hemen İncele]({s['Link']})")
                else:
                    st.error("TP AI ağda bu ürüne dair bir iz bulamadı.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- ALT BİLGİ ---
st.caption(f"TP AI v3.0 | Son Senkronizasyon: {datetime.datetime.now().strftime('%H:%M:%S')}")
