"""Interface Streamlit do Sentinela. Execute: streamlit run src/app.py"""
from datetime import date

import streamlit as st

from agent import Agente
from calculadora import INTERVALOS_MESES, proxima_manutencao
from prompts import AVISO_LEGAL

st.set_page_config(page_title="Sentinela", page_icon="🧯")


@st.cache_resource
def obter_agente() -> Agente:
    return Agente()


agente = obter_agente()

st.title("🧯 Sentinela")
st.caption("Assistente de manutenção preventiva contra incêndio")

with st.sidebar:
    st.header("Seu contexto")
    tipo = st.selectbox("Tipo de edificação", ["Não informado", "Comercial", "Industrial",
                                               "Residencial (condomínio)", "Escola/Hospital"])
    estado = st.text_input("Estado (UF)", max_chars=2).upper()
    perfil = f"edificação: {tipo}; estado: {estado or 'não informado'}"
    modo = "IA generativa (LLM)" if agente.usa_llm else "Offline (só base de conhecimento)"
    st.info(f"Modo atual: {modo}")
    if st.button("Limpar conversa"):
        st.session_state.mensagens = []
    st.caption(AVISO_LEGAL)

aba_chat, aba_calc = st.tabs(["💬 Conversa", "📅 Próxima manutenção"])

with aba_chat:
    if "mensagens" not in st.session_state:
        st.session_state.mensagens = []
    for m in st.session_state.mensagens:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
    if pergunta := st.chat_input("Ex.: O que verificar na inspeção mensal de extintores?"):
        st.session_state.mensagens.append({"role": "user", "content": pergunta})
        with st.chat_message("user"):
            st.markdown(pergunta)
        r = agente.responder(pergunta, st.session_state.mensagens[:-1], perfil)
        texto = r["resposta"]
        if r["fontes"]:
            texto += "\n\n*Fontes: " + "; ".join(r["fontes"]) + "*"
        with st.chat_message("assistant"):
            st.markdown(texto)
        st.session_state.mensagens.append({"role": "assistant", "content": texto})

with aba_calc:
    st.write("Simulação demonstrativa com intervalos de referência da base de conhecimento.")
    item = st.selectbox("Item", list(INTERVALOS_MESES))
    ultima = st.date_input("Data da última manutenção", value=date.today(), format="DD/MM/YYYY")
    if st.button("Calcular"):
        r = proxima_manutencao(item, ultima)
        st.success(f"Próxima: **{r['proxima']:%d/%m/%Y}** — {r['situacao']}")
        st.caption("Confirme prazos na norma vigente e com o responsável técnico.")
