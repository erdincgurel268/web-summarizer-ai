import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

st.set_page_config(page_title="AI Web Özetleyici", page_icon="🔎", layout="centered")

st.title("🔎 AI Web Sitesi Özetleyici")
st.caption("Bir URL gir, Gemini AI sana kısa ve net bir özet çıkarsın.")

url = st.text_input("Web sitesi URL'si", placeholder="https://example.com")

if st.button("Özetle"):
    if not url:
        st.warning("Lütfen bir URL gir.")
    else:
        try:
            with st.spinner("Sayfa çekiliyor..."):
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(url, headers=headers, timeout=10)
                soup = BeautifulSoup(response.text, "html.parser")

                paragraphs = soup.find_all("p")
                text = " ".join([p.get_text() for p in paragraphs])
                text = text[:5000]  # çok uzun olmasın

            if not text.strip():
                st.error("Sayfadan metin çekilemedi.")
            else:
                with st.spinner("AI özetliyor..."):
                    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                    model = genai.GenerativeModel("gemini-2.0-flash")
                    prompt = f"Aşağıdaki web sitesi içeriğini 3-4 cümlede, Türkçe ve net şekilde özetle:\n\n{text}"
                    result = model.generate_content(prompt)

                st.subheader("📄 Özet")
                st.write(result.text)

        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")

st.divider()
st.caption("⚠️ Bazı siteler otomatik veri çekmeyi engelleyebilir.")