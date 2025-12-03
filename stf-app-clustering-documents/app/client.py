import streamlit as st
from transform_data import TransformData
from bertopic import BERTopic
from dotenv import load_dotenv
from openai import OpenAI
import prompts
import os


st.set_page_config(
    page_title="Pré-processamento Jurídico",
    layout="wide",
    page_icon="⚖️",
)

def load_css(file_name: str):
    with open(file_name, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# openai client
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

system_prompt = prompts.system_prompt
examples = prompts.examples

st.markdown("<h1>⚖️ Pré-processamento Jurídico</h1>", unsafe_allow_html=True)
st.write(
    "<p style='text-align:center; color:#3b5068;'>"
    "Gere a análise de FIRAC automaticamente com IA."
    "</p>",
    unsafe_allow_html=True
)


st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("Insira o texto jurídico:")
text = st.text_area(" ", height=200)
st.markdown('</div>', unsafe_allow_html=True)


if st.button("Processar"):
    if text.strip():
        with st.spinner("🔍 Processando o texto..."):

            resultado = TransformData.preprocess(text)

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{examples}\n\nTexto novo:\n{resultado}"}
            ]

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages
            )

            firac = response.choices[0].message.content

       
       # resultados
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🧹 Texto Pré-processado:")
        st.write(resultado)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📑 FIRAC:")
        st.write(firac)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.warning("⚠️ Por favor, insira um texto.")