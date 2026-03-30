import streamlit as st
import google.generativeai as genai
import datetime

# --- 1. YAPAY ZEKA AYARLARI ---
# Kendi API Key'ini buraya yaz
API_KEY = "AIzaSyDu7faagD6mtZugXhhJ3PiIEdqZ20kThlA"
genai.configure(api_key=API_KEY)

# Modeli başlat (Hata almamak için güvenli yöntem)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. SAYFA TASARIMI (MODERN DARK) ---
st.set_page_config(page_title="TP AI | Chat", page_icon="🤖")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .chat-bubble { padding: 15px; border-radius: 15px; margin-bottom: 10px; }
    .user-bubble { background-color: #1f6feb; text-align: right; }
    .ai-bubble { background-color: #238636; text-align: left; }
</style>
""", unsafe_allow_html=True)

st.title("🤖 TP AI: Neural Assistant")
st.caption("Düzce'den Dünyaya | Yapay Zeka Sohbet Arayüzü")

# --- 3. SOHBET HAFIZASI (SESSION STATE) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajları ekrana bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. SOHBET MOTORU ---
if prompt := st.chat_input("TP AI'ya bir şeyler sor..."):
    # Kullanıcı mesajını kaydet ve göster
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI yanıtını oluştur
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Sohbet geçmişini AI'ya gönder (Böylece önceki dediklerini hatırlar)
            response = model.generate_content(prompt)
            full_response = response.text
            message_placeholder.markdown(full_response)
        except Exception as e:
            full_response = f"Bir hata oluştu: {e}"
            message_placeholder.markdown(full_response)
            
    # AI yanıtını hafızaya kaydet
    st.session_state.messages.append({"role": "assistant", "content": full_response})
