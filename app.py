import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Luna: Senin Asistanın", page_icon="✨")
st.title("✨ Luna: Senin Asistanın")

# Yan panelde sadece Gemini anahtarı var
with st.sidebar:
    st.header("⚙️ Ayarlar")
    api_key_gemini = st.text_input("Gemini API Anahtarı:", type="password")
    tarz = st.selectbox("Luna'nın Modu:", ["Bilge Hermione", "Eğlenceli ve Neşeli", "Gizemli"])
    isim = st.text_input("Luna'ya seslen:", "Luna")

# Eğer anahtar girilmişse asistan başlar
if api_key_gemini:
    genai.configure(api_key=api_key_gemini)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input(f"{isim}'ya bir şey sor..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                sistem_talimati = f"Sen {tarz} bir asistansın. İsmin {isim}."
                response = model.generate_content(f"{sistem_talimati}. Kullanıcı dedi ki: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error("API anahtarında bir sorun var, lütfen kontrol et.")
else:
    st.info("Başlamak için sol menüden Gemini API anahtarınızı girin.")
