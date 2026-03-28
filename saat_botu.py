import yfinance as yf
import requests
from bs4 import BeautifulSoup
import pandas as pd

def ekonomi_verisi_al():
    # Son 5 günlük dolar hareketine bakıyoruz
    dolar = yf.download("USDTRY=X", period="5d", interval="1d")['Close']
    kur = float(dolar.iloc[-1])
    degisim = float(((dolar.iloc[-1] - dolar.iloc[0]) / dolar.iloc[0]) * 100)
    return kur, degisim

def akakce_fiyat_oku(url):
    # Tarayıcı gibi görünmek için gerekli başlık
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"}
    
    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, "html.parser")
        
        # Akakçe fiyatını bulalım
        fiyat_etiketi = soup.find("span", {"class": "pt_v8"})
        if fiyat_etiketi:
            metin = fiyat_etiketi.text
            # Temizlik: "7.499,00 TL" -> 7499.0
            rakam = float(metin.replace(".", "").replace(",", ".").replace(" TL", ""))
            return rakam
    except:
        return None
    return None

# --- ANA PROGRAM ---
urun_url = "https://www.akakce.com/akilli-saat/en-ucuz-samsung-galaxy-watch-7-44mm-fiyati,708620942.html"

print("\n--- 🤖 Akıllı Fiyat Asistanı Çalışıyor ---")
fiyat = akakce_fiyat_oku(urun_url)
kur, artis = ekonomi_verisi_al()

if fiyat:
    print(f"📦 Ürün Fiyatı: {fiyat:,.2f} TL")
    print(f"💵 Dolar Kuru: {kur:.2f} TL (Haftalık Değişim: %{artis:.2f})")
    print("-" * 35)

    # Basit Akıllı Karar Mekanizması
    if artis > 1.2:
        print("💡 TAVSİYE: Dolar %1.2'den fazla artmış! Fiyatlar yükselmeden ALMAK mantıklı.")
    elif artis < -1.0:
        print("💡 TAVSİYE: Dolar düşüyor, birkaç gün bekleyip fiyatı tekrar kontrol et.")
    else:
        print("💡 TAVSİYE: Piyasa stabil. Eğer fiyat senin için uygunsa alabilirsin.")
else:
    print("❌ Fiyat verisi çekilemedi. Lütfen internet bağlantını veya linki kontrol et.")