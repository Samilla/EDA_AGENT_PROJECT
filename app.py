# app.py
import streamlit as st
import pandas as pd
from agents.data_agent import DataAgent
from agents.analyst_agent import AnalystAgent
from utils.file_handler import unzip_and_read_file

st.set_page_config(page_title="Agente EDA Cloud", layout="wide", page_icon="🧠")

st.title("🧠 Multi-Agente EDA e Fraudes - Streamlit Cloud")

# Inicializa histórico de chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------
# Upload de arquivo
# -------------------
st.sidebar.header("📂 Upload de Arquivo CSV ou ZIP")
uploaded_file = st.sidebar.file_uploader("Envie seu arquivo (.csv ou .zip)", type=["csv", "zip"])

if uploaded_file:
    csv_path, df = unzip_and_read_file(uploaded_file)
    if not csv_path or df is None:
        st.error("Erro ao processar arquivo. Certifique-se de ser CSV ou ZIP válido.")
        st.stop()

    st.success(f"✅ Arquivo carregado: {uploaded_file.name}")
    agent = DataAgent(csv_path)
    st.dataframe(agent.df.head())
    st.write(agent.describe_data())

    # -------------------
    # Pergunta ao Agente
    # -------------------
    st.subheader("💬 Pergunte ao Agente")
    question = st.text_area("Digite sua pergunta sobre os dados:")

    if st.button("🔎 Analisar"):
        if question.strip():
            analyst = AnalystAgent(csv_path)
            with st.spinner("A IA está analisando..."):
                # Reuso inteligente: cache de respostas para mesma pergunta
                cache_key = f"qa_{hash(question)}"
                if cache_key in st.session_state:
                    response = st.session_state[cache_key]
                else:
                    response = analyst.answer_question(question)
                    st.session_state[cache_key] = response

            # Histórico de chat
            st.session_state.chat_history.append(("user", question))
            st.session_state.chat_history.append(("agent", response["answer"]))

            # Exibe chat
            for role, msg in st.session_state.chat_history[-10:]:
                if role == "user":
                    st.chat_message("user").markdown(msg)
                else:
                    st.chat_message("assistant").markdown(msg)

            # Exibe gráfico se houver
            if response.get("plotly_json"):
                import plotly.io as pio
                fig = pio.from_json(response["plotly_json"])
                st.plotly_chart(fig, use_container_width=True)

            # Relatório Markdown
            st.markdown("### 🧾 Relatório Resumido (Markdown)")
            markdown_report = agent.generate_markdown_report(response["answer"])
            st.markdown(markdown_report)
            st.download_button(
                "⬇️ Baixar Relatório em Markdown",
                markdown_report,
                file_name="analise_relatorio.md",
            )
        else:
            st.warning("Digite uma pergunta antes de analisar.")

else:
    st.info("Envie um arquivo CSV ou ZIP para começar a análise.")