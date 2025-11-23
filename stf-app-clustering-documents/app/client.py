import streamlit as st
from transform_data import TransformData

st.title("Pré-processamento Jurídico")

name_input = st.text_area("Cole o texto jurídico aqui:")

td = TransformData()

if st.button("Processar"):
    if name_input.strip():
        with st.spinner("Processando..."):
            resultado = td.preprocess(name_input)
            st.subheader("Resultado:")
            st.write(resultado)
    else:
        st.warning("Por favor, insira um texto.")
