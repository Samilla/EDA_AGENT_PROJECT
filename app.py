# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
from agents.data_agent import DataAgent
from agents.analyst_agent import AnalystAgent

st.set_page_config(page_title="Agente EDA com Gemini 2.5 Flash", layout="wide")

st.title("🤖 Agente de Análise Exploratória (EDA) com Gemini 2.5 Flash")
st.write("Faça upload de um arquivo CSV (ou ZIP) e pergunte ao agente o que deseja analisar.")

# Inicializa agentes
data_agent = DataAgent()
api_key = st.secrets["gcp"]["gemini_api_key"]
analyst_agent = AnalystAgent(api_key)

uploaded_file = st.file_uploader("📂 Envie um arquivo CSV ou ZIP", type=["csv", "zip"])

if uploaded_file:
    df, csv_path = data_agent.load_data(uploaded_file)
    st.success(f"Arquivo carregado com {df.shape[0]} linhas e {df.shape[1]} colunas.")
    st.dataframe(df.head())

    user_question = st.text_area("🧠 Faça sua pergunta sobre os dados:")

    if st.button("Analisar"):
        with st.spinner("Analisando com Gemini..."):
            response = analyst_agent.analyze(csv_path, user_question)

        # Verifica se é um gráfico JSON
        if "<PLOTLY_JSON>" in response:
            json_data = response.split("<PLOTLY_JSON>")[1].split("</PLOTLY_JSON>")[0]
            fig = go.Figure(json.loads(json_data))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown(response)

    if st.button("Gerar Relatório Automático"):
        report = analyst_agent.generate_report(df)
        st.markdown(report)
