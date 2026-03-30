import streamlit as st
import google.generativeai as genai
import PIL.Image
import io
import datetime
import time

# --- 1. AI ÇEKİRDEK YAPILANDIRMASI ---
# Senin sağladığın Özel API Key
API_KEY = "AIzaSyBPTkFQ78pZu_Snj0vK3G4Jk-dx5bqWpoY"
genai.configure(api_key=API_KEY)

# Sistem Talimatı: Yapay zekanın "Kişiliği"
SYSTEM_INSTRUCTION = """
Sen TP AI (Neural Genesis) v9.0 sürümüsün. 
Düzce merkezli bir teknoloji geliştiricisi tarafından oluşturuldun.
Özelliklerin:
1. Çok zeki, yardımsever ve teknik konularda (Python, Flutter, Donanım) uzmansın.
2. Beşiktaş JK taraftarısın ve Formula 1'i yakından takip ediyorsun.
3. Kullanıcılara sadece cevap vermezsin, onlara stratejik tavsiyeler sunarsın.
4. Karmaşık kodlama sorunlarını saniyeler içinde çözebilirsin.
"""

# Model Ayarları (Yüksek Yaratıcılık ve Uzun Cevaplar için)
generation_config = {
    "temperature": 0.85,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 4096, # Uzun cevaplar için limit artırıldı
}

@st.cache_resource
def model_baslat():
    try:
        # En stabil ve kapsamlı model
        return genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction=SYSTEM_INSTRUCTION
        )
    except:
        return genai.GenerativeModel("gemini-pro")

ai_engine = model_baslat()

# --- 2. GELİŞMİŞ UI TASARIMI (MATRIX DARK) ---
st.set_page_config(page_title="TP AI | Neural Engine", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #05070a; color: #e1e4e8; }
    .stTextInput>div>div>input { background-color: #0d1117; color: #58a6ff; border: 1px solid #30363d; }
    .sidebar .sidebar-content { background-image: linear-gradient(#0d1117, #05070a); }
    .stButton>button {
        background: linear-gradient(135deg, #238636, #2ea043);
        color: white; border: none; padding: 10px 24px; border-radius: 8px;
        font-weight: bold; width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 4px 15px rgba(35, 134, 54, 0.4); }
    .status-tag { padding: 5px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; }
    .ai-bubble { background: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 15px; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

# --- 3. KENAR ÇUBUĞU (KONTROL MERKEZİ) ---
with st.sidebar:
    st.image("https://img.icons8.com/nolan/128/artificial-intelligence.png", width=80)
    st.title("TP AI Kontrol Paneli")
    st.markdown("---")
    
    st.subheader("🛠️ Modüller")
    mod_vision = st.toggle("Görüntü Analizi (Vision)", value=True)
    mod_code = st.toggle("Gelişmiş Kod Yazıcı", value=True)
    
    st.subheader("📁 Dosya Analizi")
    yuklenen_dosya = st.file_uploader("Bir resim veya metin dosyası yükle", type=['png', 'jpg', 'jpeg', 'txt', 'py'])
    
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.info(f"📍 Sunucu: Düzce/TR\n🚀 Model: Gemini 1.5 Flash\n🕒 {datetime.datetime.now().strftime('%Y-%m-%d')}")

# --- 4. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hoşgeldiniz Mesajı
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown("### Selam! Ben TP AI v9.0. \nDüzce'deki geliştiricim tarafından en üst düzey yeteneklerle donatıldım. Bugün hangi karmaşık problemi çözelim?")

# Geçmişi Görüntüle
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. ANA ETKİLEŞİM MOTORU ---
if prompt := st.chat_input("Bir soru sorun, kod yazdırın veya dosya analiz edin..."):
    
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Yanıt Oluşturma
    with st.chat_message("assistant"):
        with st.spinner("Neural Engine İşliyor..."):
            try:
                ai_input = [prompt]
                
                # Eğer dosya yüklendiyse prompt'a ekle
                if yuklenen_dosya:
                    if yuklenen_dosya.type in ['image/png', 'image/jpeg']:
                        img = PIL.Image.open(yuklenen_dosya)
                        ai_input.insert(0, img)
                        st.image(img, caption="Analiz Edilen Görsel", width=300)
                    else:
                        stringio = io.StringIO(yuklenen_dosya.getvalue().decode("utf-8"))
                        dosya_icerigi = stringio.read()
                        ai_input.append(f"\n\nDosya İçeriği:\n{dosya_icerigi}")

                # AI Yanıt Üretimi
                response = ai_engine.generate_content(ai_input)
                full_response = response.text
                
                # Akıcı yazım efekti (Opsiyonel)
                st.markdown(full_response)
                
            except Exception as e:
                full_response = f"⚠️ Kritik Sistem Hatası: {e}"
                st.error(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- 6. METRİKLER (ALT PANEL) ---
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.write("🟢 **Sistem Durumu:** Optimal")
with col2:
    st.write(f"💬 **Mesaj Sayısı:** {len(st.session_state.messages)}")
with col3:
    st.write("📡 **API Gecikmesi:** Düşük")
