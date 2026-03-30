import streamlit as st
import google.generativeai as genai
import datetime

# --- 1. EN STABİL MODEL YAPILANDIRMASI ---
# Senin API Anahtarın
API_KEY = "AIzaSyDu7faagD6mtZugXhhJ3PiIEdqZ20kThlA"
genai.configure(api_key=API_KEY)

# Hız ve Kararlılık Şampiyonu: 1.5 Flash
# 'models/' ön eki en güvenli yoldur.
STABIL_MODEL_ADI = "models/gemini-1.5-flash"

try:
    model = genai.GenerativeModel(STABIL_MODEL_ADI)
except:
    # Eğer Flash'ta bir sorun olursa en eski/stabil Pro sürümüne düşer
    model = genai.GenerativeModel("models/gemini-pro")

# --- 2. PREMIUM KARANLIK ARAYÜZ ---
st.set_page_config(page_title="TP AI | Neural", page_icon="🧠", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .stTextInput>div>div>input { background-color: #161b22; color: white; border: 1px solid #30363d; border-radius: 10px; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; border: 1px solid #30363d; }
    /* Kullanıcı mesajı rengi */
    [data-testid="stChatMessage"]:nth-child(even) { background-color: #1f6feb22; border-left: 5px solid #1f6feb; }
    /* AI mesajı rengi */
    [data-testid="stChatMessage"]:nth-child(odd) { background-color: #23863622; border-left: 5px solid #238636; }
</style>
""", unsafe_allow_html=True)

st.title("🧠 TP AI <span style='color:#58a6ff'>NEURAL</span>", unsafe_allow_html=True)
st.caption("Düzce Veri Merkezi Üzerinden Aktif | v8.0 Stabil")

# --- 3. SOHBET HAFIZASI (SESSION STATE) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajları ekrana bas (Sohbet geçmişi görünür kalır)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. AKILLI YANIT MOTORU ---
if prompt := st.chat_input("TP AI'ya bir mesaj gönder..."):
    # 1. Kullanıcı mesajını kaydet ve göster
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. AI Yanıtını oluştur
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        try:
            # Modeli çağırıyoruz
            # Not: Daha gelişmiş olması için tüm geçmişi de gönderebiliriz ama 
            # şu an en stabil hali tekli sorgudur.
            response = model.generate_content(prompt)
            full_response = response.text
            response_placeholder.markdown(full_response)
        except Exception as e:
            full_response = f"⚠️ Sistem meşgul veya bir hata oluştu. Lütfen tekrar dene.\n(Hata: {e})"
            response_placeholder.markdown(full_response)
            
    # 3. AI yanıtını hafızaya kaydet
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- ALT BİLGİ ---
st.markdown("---")
st.markdown(f"<p style='text-align: center; color: #8b949e;'>Bağlı Modül: {STABIL_MODEL_ADI}</p>", unsafe_allow_html=True)
