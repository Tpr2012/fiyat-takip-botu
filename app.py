import streamlit as st
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Sayfa Tasarımı
st.set_page_config(page_title="Akıllı Fiyat Takipçisi", page_icon="⌚", layout="wide")

st.title("🚀 Akıllı Fiyat & Ekonomi Analizörü")
st.info("Akakçe linkini yapıştır, gerisini yapay zekaya bırak.")

# --- FİYAT ÇEKME FONKSİYONU (GÜNCELLENDİ) ---
def fiyat_cek(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, "html.parser")
        
        # Akakçe'nin en ucuz fiyatını bulmaya çalışan 3 farklı yöntem
        fiyat_etiketi = soup.select_one("span.pt_v8") or soup.select_one(".v8p") or soup.find("span", {"class": "pt_v8"})
        
        if fiyat_etiketi:
            fiyat_text = fiyat_etiketi.text.strip()
            # "7.499,00 TL" -> 7499.0 temizliği
            temiz_fiyat = "".join(c for c in fiyat_text if c.isdigit() or c in ",.")
            if "," in temiz_fiyat and "." in temiz_fiyat:
                temiz_fiyat = temiz_fiyat.replace(".", "").replace(",", ".")
            elif "," in temiz_fiyat:
                temiz_fiyat = temiz_fiyat.replace(",", ".")
            return float(temiz_fiyat)
    except:
        return None
    return None

# --- EKONOMİ VERİSİ ---
def ekonomi_verisi():
    try:
        dolar = yf.download("USDTRY=X", period="7d", interval="1d")['Close']
        kur = float(dolar.iloc[-1])
        degisim = float(((dolar.iloc[-1] - dolar.iloc[0]) / dolar.iloc[0]) * 100)
        return kur, degisim, dolar
    except:
        return 32.50, 0.0, None # Hata olursa varsayılan değer

# --- ARAYÜZ ---
url_input = st.text_input("Akakçe Ürün Linki:", placeholder="https://www.akakce.com/...")

if st.button("Piyasayı Analiz Et"):
    if url_input:
        with st.spinner('Veriler toplanıyor...'):
            fiyat = fiyat_cek(url_input)
            kur, degisim, dolar_grafik = ekonomi_verisi()
            
            col1, col2, col3 = st.columns(3)
            
            if fiyat:
                col1.metric("Ürün Fiyatı", f"{fiyat:,.2f} TL")
            else:
                col1.error("Fiyat Çekilemedi! (Site engellemiş olabilir)")
                
            col2.metric("Güncel Dolar", f"{kur:.2f} TL", f"%{degisim:.2f}")
            col3.metric("Durum", "Analiz Edildi")

            st.divider()

            if fiyat:
                if degisim > 1.0:
                    st.warning(f"🚨 **KRİTİK UYARI:** Dolar %{degisim:.2f} yükselmiş. Bu ürünün fiyatı her an artabilir! Almayı düşünüyorsan elini çabuk tut.")
                elif degisim < -1.0:
                    st.success(f"✅ **FIRSAT:** Dolar düşüşte. Biraz daha beklersen indirim gelebilir.")
                else:
                    st.info("⚖️ **STABİL:** Piyasa sakin. Fiyat şu an normal seviyelerde görünüyor.")
                
                # Grafik
                st.subheader("📊 Doların Haftalık Seyri")
                st.line_chart(dolar_grafik)
            else:
                st.warning("⚠️ Akakçe bazen botları engelliyor. Lütfen sayfayı yenileyip tekrar dene veya linkin doğruluğunu kontrol et.")
    else:
        st.error("Lütfen bir link girin!")
