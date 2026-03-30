import streamlit as st
import google.generativeai as genai
import PIL.Image
import io
import datetime

# --- 1. AI ÇEKİRDEK YAPILANDIRMASI ---
# Yeni ve geçerli API Anahtarın başarıyla entegre edildi
API_KEY = "AIzaSyBPTkFQ78pZu_Snj0vK3G4Jk-dx5bqWpoY"
genai.configure(api_key=API_KEY)

# Sistem Talimatı: Yapay zekanın "Karakteri"
SYSTEM_INSTRUCTION = """
Sen TP AI (Neural Genesis) v9.5 sürümüsün. 
Düzce merkezli bir teknoloji dâhisi tarafından geliştirildin.
Kişilik Özelliklerin:
- Çok zeki, çözüm odaklı ve teknik konularda (Python, Flutter, PC Donanım) bir mastersın.
- Beşiktaş JK taraftarısın (Kara Kartal!), Formula 1 ve LEGO Technic tutkunusun.
- Kullanıcılara karşı samimi ama profesyonel bir "mühendis" diliyle konuşursun.
- Görsel analiz yeteneğin en üst düzeydedir.
"""

generation_config = {
    "temperature": 0.75,
    "top_p": 0.95,
    "max_output_tokens": 4096,
}

@st.cache_resource
def engine_baslat():
    # En kapsamlı model: 1.5 Flash (Resim + Metin + Hız)
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=SYSTEM_INSTRUCTION
    )

ai_engine = engine_baslat()

# --- 2. PREMIUM KARANLIK ARAYÜZ (MATRIX STYLE) ---
st.set_page_config(page_title="TP AI | Neural Engine", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #05070a; color: #e1e4e8; }
    .stTextInput>div>div>input { background-color: #0d1117; color: #58a6ff; border: 1px solid #30363d; border-radius: 10px; }
    .sidebar .sidebar-content { background-color: #0d1117; }
    .stButton>button {
        background: linear-gradient(135deg, #1f6feb, #ab7df8);
        color: white; border: none; padding: 12px; border-radius: 10px;
        font-weight: bold; width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(31, 111, 235, 0.4); }
    .chat-card { background: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 15px; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

# --- 3. YAN PANEL (KONTROL MERKEZİ) ---
with st.sidebar:
    st.image("https://img.icons8.com/nolan/128/brain.png", width=70)
    st.title("TP AI Kontrol")
    st.markdown("---")
    
    st.subheader("📁 Multimodal Analiz")
    yuklenen_dosya = st.file_uploader("Resim veya Kod dosyası yükle", type=['png', 'jpg', 'jpeg', 'txt', 'py'])
    
    if st.button("Hafızayı Temizle"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.success("🟢 Sistem: Çevrimiçi")
    st.info(f"🚀 Modül: Gemini 1.5 Flash\n🕒 {datetime.datetime.now().strftime('%H:%M')}")

# --- 4. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. ANA ETKİLEŞİM MOTORU ---
if prompt := st.chat_input("TP AI'ya bir görev ver..."):
    
    # Mesajı kaydet
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Yanıt Üretimi
    with st.chat_message("assistant"):
        with st.spinner("Neural Engine Analiz Ediyor..."):
            try:
                ai_input = [prompt]
                
                # Dosya analizi (Resim veya Metin)
                if yuklenen_dosya:
                    if yuklenen_dosya.type in ['image/png', 'image/jpeg']:
                        img = PIL.Image.open(yuklenen_dosya)
                        ai_input.insert(0, img)
                        st.image(img, caption="Görsel Giriş", width=250)
                    else:
                        icerik = yuklenen_dosya.getvalue().decode("utf-8")
                        ai_input.append(f"\n\nBelge İçeriği:\n{icerik}")

                # AI Yanıtı
                response = ai_engine.generate_content(ai_input)
                full_text = response.text
                st.markdown(full_text)
                
            except Exception as e:
                full_text = f"⚠️ Bağlantı Hatası: {e}"
                st.error(full_text)

    st.session_state.messages.append({"role": "assistant", "content": full_text})

# --- 6. ALT BİLGİ ---
st.markdown("---")
st.caption(f"TP AI v9.5 | Neural Genesis | Düzce | {datetime.datetime.now().year}")
