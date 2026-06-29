import streamlit as st
import google.generativeai as genai
from openai import OpenAI

st.set_page_config(page_title="Luna: Senin Asistanın", page_icon="✨")

st.title("✨ Luna: Kişiselleştirilebilir Asistan")

with st.sidebar:
    st.header("⚙️ Ayarlar")
    st.markdown("Luna'yı kullanmak için lütfen anahtarlarınızı girin.")
    api_key_gemini = st.text_input("Gemini API Anahtarı:", type="password")
    api_key_openai = st.text_input("OpenAI (DALL-E) Anahtarı:", type="password")
    tarz = st.selectbox("Luna'nın Modu:", ["Bilge Hermione", "Eğlenceli ve Neşeli", "Gizemli"])
    isim = st.text_input("Luna'ya seslen:", "Luna")

if api_key_gemini and api_key_openai:
    genai.configure(api_key=api_key_gemini)
    client = OpenAI(api_key=api_key_openai)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input(f"{isim}'ya bir şey sor veya resim çizdir..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if "çiz" in prompt.lower() or "resim" in prompt.lower():
            with st.spinner(f"{isim} senin için büyülü bir resim çiziyor..."):
                try:
                    resim = client.images.generate(model="dall-e-3", prompt=prompt, n=1, size="1024x1024")
                    image_url = resim.data[0].url
                    st.image(image_url, caption=f"{isim}'nın çizimi")
                    st.session_state.messages.append({"role": "assistant", "content": f"![Resim]({image_url})"})
                except Exception as e:
                    st.error("Resim çizilirken bir hata oluştu.")
        else:
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                sistem_talimati = f"Sen {tarz} bir asistansın. İsmin {isim}."
                response = model.generate_content(f"{sistem_talimati}. Kullanıcı dedi ki: {prompt}")
                with st.chat_message("assistant"):
                    st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error("Hata oluştu, API anahtarını kontrol et.")
else:
    st.info("Başlamak için sol menüden API anahtarlarınızı girin.")
