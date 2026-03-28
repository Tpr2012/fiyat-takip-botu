import streamlit as st
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Sayfa Ayarları
st.set_page_config(page_title="Akıllı Fiyat Takipçisi", layout="centered")

st.title("🤖 Akıllı Fiyat & Ekonomi Analizörü")
st.markdown("Linkini yapıştır, yapay zeka senin için piyasayı analiz etsin.")

# --- FONKSİYONLAR ---
def ekonomi_verisi():
    dolar = yf.download("USDTRY=X", period="7d", interval="1d")['Close']
    kur = float(dolar.iloc[-1])
    degisim = float(((dolar.iloc[-1] - dolar.iloc[0]) / dolar.iloc[0]) * 100)
    return kur, degisim

def fiyat_cek(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, "html.parser")
        # Akakçe için fiyat etiketi
        fiyat_etiketi = soup.find("span", {"class": "pt_v8"})
        if fiyat_etiketi:
            metin = fiyat_etiketi.text
            return float(metin.replace(".", "").replace(",", ".").replace(" TL", ""))
    except:
        return None

# --- ARAYÜZ ---
url_input = st.text_input("Ürün Linkini Buraya Yapıştır:", placeholder="https://www.akakce.com/...")

if st.button("Analiz Et"):
    if url_input:
        with st.spinner('Piyasa verileri okunuyor...'):
            fiyat = fiyat_cek(url_input)
            kur, degisim = ekonomi_verisi()
            
            # Kartlar (Metric)
            col1, col2 = st.columns(2)
            col1.metric("Ürün Fiyatı", f"{fiyat} TL" if fiyat else "Bulunamadı")
            col2.metric("Güncel Dolar", f"{kur:.2f} TL", f"%{degisim:.2f}")

            st.divider()

            # Akıllı Yorum
            if fiyat:
                if degisim > 1.5:
                    st.error(f"🚨 **DİKKAT:** Dolar %{degisim:.2f} artışta! Fiyatlar her an yükselebilir. Almak için uygun zaman olabilir.")
                elif degisim < -1.0:
                    st.success(f"✅ **BEKLE:** Dolar %{abs(degisim):.2f} düşüşte. Fiyatlarda indirim görebilirsin.")
                else:
                    st.info("⚖️ **STABİL:** Ekonomi sakin seyrediyor. Fiyat şu an normal seviyelerde.")
            
            # Grafik (Örnek Dolar Grafiği)
            st.subheader("Haftalık Dolar Seyri")
            dolar_data = yf.download("USDTRY=X", period="7d")['Close']
            st.line_chart(dolar_data)
    else:
        st.warning("Lütfen bir link girin!")