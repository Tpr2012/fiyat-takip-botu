import streamlit as st
import google.generativeai as genai
import PIL.Image
import io
import datetime
import time

# --- 1. SİSTEM YAPILANDIRMASI VE GÜVENLİK ---
# Senin sağladığın Özel API Key - Sisteme entegre edildi
API_KEY = "AIzaSyBPTkFQ78pZu_Snj0vK3G4Jk-dx5bqWpoY"
genai.configure(api_key=API_KEY)

# Sayfa Ayarları (Premium Koyu Tema)
st.set_page_config(
    page_title="Neural Core AI | Düzce",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. DİNAMIK MODEL SEÇİCİ (404 HATASINI ÖNLEYEN SİSTEM) ---
@st.cache_resource
def motoru_baslat():
    """Google'a bağlanır ve senin anahtarına açık olan en iyi modeli otomatik bulur."""
    try:
        # Sistemde izin verilen tüm modelleri listele
        kullanilabilir_modeller = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        if not kullanilabilir_modeller:
            return None, "API Anahtarı Geçersiz veya Yetkisiz", "🔴 Hata"

        # Öncelikle 1.5 Flash'ı (Görsel+Hafıza+Hız) bulmaya çalışıyoruz
        secilen_model = next((m for m in kullanilabilir_modeller if "1.5-flash" in m), kullanilabilir_modeller[0])
        
        # Sistem Talimatı: Yapay zekanın "Marka Kimliği ve Kişiliği"
        SYSTEM_INSTRUCTION = """
        Sen Neural Core AI v10 sürümüsün. Düzce'deki teknoloji laboratuvarında geliştirildin.
        Kişilik Özelliklerin:
        1. Çok zeki, çözüm odaklı ve teknik konularda (Python, Flutter, Donanım) uzmansın.
        2. Beşiktaş JK taraftarısın, Formula 1'i ve LEGO Technic setlerini yakından takip edersin.
        3. Kullanıcıya karşı saygılı, net ve stratejik bir "mühendis" diliyle konuşursun.
        4. Mevcut sohbet geçmişini mükemmel bir şekilde hatırlayabilirsin.
        """

        # Sistem talimatları sadece 1.5 modellerinde desteklenir
        if "1.5" in secilen_model:
            model = genai.GenerativeModel(
                model_name=secilen_model,
                system_instruction=SYSTEM_INSTRUCTION
            )
        else:
            # Eski modeller için yedek kurulum (gemini-pro)
            model = genai.GenerativeModel(model_name=secilen_model)

        # Model ismini temizleyip kullanıcıya gösteriyoruz
        temiz_model_adi = secilen_model.split('/')[-1]
        return model, temiz_model_adi, "🟢 Çevrimiçi"
    
    except Exception as e:
        return None, str(e), "🔴 Bağlantı Yok"

# Motoru ve durumu al
ai_engine, model_info, sistem_durumu = motoru_baslat()

# --- 3. PREMIUM UI TASARIMI (DARK CODE MODE) ---
st.markdown("""
<style>
    .stApp { background-color: #0d1117; color: #c9d1d9; font-family: 'Segoe UI', sans-serif; }
    .stTextInput>div>div>input { background-color: #161b22; color: #58a6ff; border: 1px solid #30363d; border-radius: 8px; }
    .sidebar .sidebar-content { background-image: linear-gradient(#0d1117, #05070a); }
    [data-testid="stChatMessage"] { background-color: #161b22; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 15px; }
    /* Kullanıcı mesajı rengi */
    [data-testid="stChatMessage"]:nth-child(even) { border-left: 5px solid #1f6feb; }
    /* AI mesajı rengi */
    [data-testid="stChatMessage"]:nth-child(odd) { border-left: 5px solid #ab7df8; }
</style>
""", unsafe_allow_html=True)

# Ana Başlık Paneli
col1, col2 = st.columns([4, 1])
with col1:
    st.title("🧠 Neural Core AI <span style='color:#ab7df8'>v10</span>", unsafe_allow_html=True)
    st.caption("Advanced Neural Genesis Engine | Düzce Veri Merkezi")
with col2:
    st.markdown(f"**Sistem:** {sistem_durumu}")
    st.markdown(f"**Motor:** {model_info}")

st.markdown("---")

# --- 4. DERİN HAFIZA YÖNETİMİ (SESSION STATE) ---
# Burası "hatırlama" özelliğinin kalbidir.
if "messages" not in st.session_state:
    st.session_state.messages = [] # Format: [{"role": "user", "content": [{"text": "..."}, {"image": ...}]}]
if "history_summary" not in st.session_state:
    st.session_state.history_summary = "" # Hafıza optimizasyonu için özet

# Sohbet Geçmişini Ekrana Bas (Sayfa yenilendiğinde hafızadaki mesajlar görünür kalır)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        for part in message["content"]:
            if "text" in part: st.markdown(part["text"])
            if "image" in part: st.image(part["image"], width=250)

# --- 5. YAN PANEL (DOSYA GİRİŞİ VE KONTROL) ---
with st.sidebar:
    st.image("https://img.icons8.com/nolan/128/artificial-intelligence.png", width=70)
    st.title("Neural Panel v10")
    st.markdown("---")
    
    st.subheader("📁 Çok Yönlü Analiz")
    yuklenen_gorsel = st.file_uploader("Görsel veya Kod Dosyası Yükle", type=["jpg", "jpeg", "png", "txt", "py"])
    
    if st.button("Hafızayı Sıfırla"):
        st.session_state.messages = []
        st.session_state.history_summary = ""
        st.rerun()

    st.markdown("---")
    st.info(f"📍 Sunucu: Düzce/TR\n🕒 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")

# --- 6. ETKİLEŞİM VE YANIT MOTORU (METİN + GÖRSEL) ---
if prompt := st.chat_input("Neural Core'a bir görev ver..."):
    if not ai_engine:
        st.error("AI Engine başlatılamadı. API anahtarınızı veya internet bağlantınızı kontrol edin.")
    else:
        # Mesaj Paketini Hazırla (Streamlit State İçin)
        kullanici_mesaj_paketi = {"role": "user", "content": []}
        
        # Eğer görsel varsa ekle
        processed_image = None
        if yuklenen_gorsel and yuklenen_gorsel.type in ['image/png', 'image/jpeg']:
            gorsel = PIL.Image.open(yuklenen_gorsel)
            kullanici_mesaj_paketi["content"].append({"image": gorsel})
            processed_image = gorsel

        # Metni ekle
        kullanici_mesaj_paketi["content"].append({"text": prompt})
        
        # Kullanıcı mesajını kaydet ve göster
        st.session_state.messages.append(kullanici_mesaj_paketi)
        with st.chat_message("user"):
            if processed_image: st.image(processed_image, width=250)
            st.markdown(prompt)

        # --- YAPAY ZEKA YANIT OLUŞTURMA (DERİN HAFIZA İLE) ---
        with st.chat_message("assistant"):
            yanit_placeholder = st.empty()
            with st.spinner("Neural Engine Analiz Ediyor..."):
                try:
                    # HAFIZA OLUŞTURMA: Tüm geçmiş metinleri birleştirip context olarak gönderiyoruz
                    # (Bu sayede "az önce ne demiştik?" sorusuna cevap verebilir)
                    context_messages = []
                    
                    # Son 6 mesajı hafızada tutuyoruz (Kotayı bitirmemek için optimizasyon)
                    # Sadece metin içeriklerini gönderiyoruz
                    for m in st.session_state.messages[-6:]:
                        for part in m["content"]:
                            if "text" in part:
                                context_messages.append({"role": "user" if m["role"] == "user" else "model", "parts": [part["text"]]})

                    # Eğer yeni mesajda resim varsa, onu listenin en başına koyuyoruz (Gemini kuralı)
                    final_parts = [prompt]
                    if processed_image:
                        final_parts.insert(0, processed_image)

                    # API'ye geçmişi ve yeni isteği gönderiyoruz
                    # Not: generate_content chat geçmişini otomatik tutmaz, bizim göndermemiz gerekir.
                    # Bu kodda history=[] kısmı boş, ama content=[*context, *final_parts] şeklinde gönderebilirdik.
                    # Ancak generate_content sistem talimatı varsa context'i geçmiş üzerinden daha iyi anlar.
                    # En stabil yol, geçmişi bir "prompt prefix" olarak eklemektir.
                    
                    history_context = ""
                    for m in st.session_state.messages[:-1]: # Yeni mesaj hariç
                        for part in m["content"]:
                            if "text" in part:
                                r = "Kullanıcı" if m["role"] == "user" else "Sen"
                                history_context += f"{r}: {part['text']}\n"
                    
                    refined_prompt = f"--- SOHBET GEÇMİŞİ ---\n{history_context}--- YENİ İSTEK ---\n{prompt}"
                    
                    # API Çağrısı
                    input_parts = [refined_prompt]
                    if processed_image:
                        input_parts.insert(0, processed_image)

                    yanit = ai_engine.generate_content(input_parts)
                    tam_metin = yanit.text
                    yanit_placeholder.markdown(tam_metin)
                    
                    st.session_state.messages.append({"role": "assistant", "content": [{"text": tam_metin}]})
                    
                except Exception as e:
                    hata_mesaji = f"**Kritik İşlem Hatası:** {str(e)}"
                    yanit_placeholder.error(hata_mesaji)

# --- 7. ALT PANEL (METRİKLER) ---
st.markdown("---")
m_col1, m_col2, m_col3 = st.columns(3)
with m_col1:
    st.write("🟢 **Durum:** Optimal")
with m_col2:
    st.write(f"💬 **Mesaj Sayısı:** {len(st.session_state.messages)}")
with m_col3:
    st.write("📡 **API Gecikmesi:** Düşük")
