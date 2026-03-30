import streamlit as st
import google.generativeai as genai
import PIL.Image

# --- 1. GÜVENLİ API YAPILANDIRMASI ---
# Güvenlik kuralı: API anahtarını asla açıkça koda yazmamalısın.
# Şimdilik buraya kendi anahtarını (AIzaSy...) yapıştır, 
# ama GitHub'a yüklerken st.secrets kullanmayı unutma!
API_KEY = "AIzaSyBPTkFQ78pZu_Snj0vK3G4Jk-dx5bqWpoY" 
genai.configure(api_key=API_KEY)

# --- 2. AKILLI VE DİNAMİK MODEL SEÇİCİ (404 HATASINA KESİN ÇÖZÜM) ---
@st.cache_resource
def kumru_motorunu_baslat():
    """Google'a bağlanır, sana açık olan modelleri listeler ve en iyisini seçer."""
    try:
        kullanilabilir_modeller = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                kullanilabilir_modeller.append(m.name)
        
        if not kullanilabilir_modeller:
            return None, "API Anahtarı Geçersiz veya Yetkisiz"

        # Listeden en gelişmiş olanı (1.5 serisini) bulmaya çalışıyoruz
        secilen_model_adi = kullanilabilir_modeller[0] # Varsayılan olarak ilkini al
        for m_adi in kullanilabilir_modeller:
            if "1.5-flash" in m_adi:
                secilen_model_adi = m_adi
                break
            elif "1.5-pro" in m_adi:
                secilen_model_adi = m_adi

        # Kumru AI'ın Karakteri ve Uzmanlık Alanları
        # Sistem talimatları sadece 1.5 modellerinde desteklenir
        if "1.5" in secilen_model_adi:
            sistem_kimligi = """
            Sen Düzce'de geliştirilen Kumru AI isimli gelişmiş bir yapay zekasın.
            Uzmanlık alanların: Python, Flutter, RTX serisi PC donanımları.
            Hobilerin: Beşiktaş JK, Formula 1 yarışları ve LEGO Technic setleri.
            Kullanıcıyla saygılı, net ve teknik bir dille konuşursun.
            """
            model = genai.GenerativeModel(
                model_name=secilen_model_adi,
                system_instruction=sistem_kimligi
            )
        else:
            # Eski modeller için (gemini-pro) düz kurulum
            model = genai.GenerativeModel(model_name=secilen_model_adi)

        return model, secilen_model_adi
    
    except Exception as e:
        return None, f"Bağlantı Hatası: {str(e)}"

# Motoru çalıştır
ai_motoru, aktif_model = kumru_motorunu_baslat()

# --- 3. ARAYÜZ TASARIMI (DARK DEV MODE) ---
st.set_page_config(page_title="Kumru AI | Core", page_icon="🦅", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0d1117; color: #c9d1d9; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .stTextInput>div>div>input { background-color: #161b22; color: #58a6ff; border: 1px solid #30363d; border-radius: 8px; }
    .chat-container { border-left: 3px solid #ab7df8; padding-left: 15px; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# Başlık Paneli
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🦅 Kumru AI: Neural Core")
    st.caption("Gelişmiş Veri ve Görüntü İşleme Terminali")
with col2:
    if ai_motoru:
        st.success(f"🟢 Çevrimiçi\n\nMotor: {aktif_model.split('/')[-1]}")
    else:
        st.error(f"🔴 Çevrimdışı\n\n{aktif_model}")

st.markdown("---")

# --- 4. SOHBET VE HAFIZA YÖNETİMİ ---
if "mesajlar" not in st.session_state:
    st.session_state.mesajlar = []

# Geçmiş mesajları ekranda tut
for mesaj in st.session_state.mesajlar:
    with st.chat_message(mesaj["rol"]):
        st.markdown(mesaj["icerik"])

# --- 5. ETKİLEŞİM ALANI (METİN + GÖRSEL) ---
with st.sidebar:
    st.header("⚙️ Veri Girişi")
    yuklenen_gorsel = st.file_uploader("Görsel Analizi İçin Yükle", type=["jpg", "jpeg", "png"])
    if st.button("Hafızayı Sıfırla"):
        st.session_state.mesajlar = []
        st.rerun()

if kullanici_girdisi := st.chat_input("Sisteme bir komut veya soru girin..."):
    if not ai_motoru:
        st.error("AI Motoru başlatılamadı. Lütfen API anahtarınızı kontrol edin.")
    else:
        # Kullanıcı mesajını ekle
        st.session_state.mesajlar.append({"rol": "user", "icerik": kullanici_girdisi})
        with st.chat_message("user"):
            st.markdown(kullanici_girdisi)

        # AI Yanıtını Oluştur
        with st.chat_message("assistant"):
            yanit_alani = st.empty()
            with st.spinner("Kumru AI İşlem Yapıyor..."):
                try:
                    veri_paketi = [kullanici_girdisi]
                    
                    if yuklenen_gorsel:
                        gorsel = PIL.Image.open(yuklenen_gorsel)
                        veri_paketi.insert(0, gorsel)
                        st.image(gorsel, caption="İşlenen Görsel", width=250)
                    
                    # API'ye İstek At
                    yanit = ai_motoru.generate_content(veri_paketi)
                    tam_metin = yanit.text
                    yanit_alani.markdown(tam_metin)
                    
                    st.session_state.mesajlar.append({"rol": "assistant", "icerik": tam_metin})
                    
                except Exception as e:
                    hata_mesaji = f"**İşlem Başarısız:** {str(e)}"
                    yanit_alani.error(hata_mesaji)
