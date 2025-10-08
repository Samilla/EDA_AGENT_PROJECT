import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st

MODEL_NAME = "gemini-2.5-flash"

class AnalystAgent:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.api_key = self.get_api_key()
        self.llm = ChatGoogleGenerativeAI(
            model=MODEL_NAME,
            google_api_key=self.api_key,
            temperature=0.0,
            timeout=120
        )

    def get_api_key(self):
        try:
            return st.secrets["gemini"]["api_key"]
        except:
            return os.getenv("GEMINI_KEY", "")

    def answer_question(self, question: str) -> dict:
        prompt = f"""
        Você é um analista de dados especializado em fraudes fiscais, outros assuntos fiscais, big data e contabilidade.
Receberá consultas de um usuário e dados analisados de um arquivo CSV.

Seu papel é:
1️⃣ Interpretar os resultados estatísticos, gráficos e clusters que o sistema EDA gerar.  
2️⃣ Gerar conclusões e insights automáticos, com foco em possíveis padrões, irregularidades ou anomalias.
3️⃣ Explicar de forma clara e profissional os achados, como se fosse um relatório técnico.
4️⃣ Manter um histórico do que já foi analisado, considerando o contexto das conversas anteriores.

Regras importantes:
- Use apenas o CSV {self.csv_path} para responder à seguinte pergunta:
 {question}
- Sempre que gerar gráficos, use a bibliotecaPlotly e retorne somente:
<PLOTLY_JSON>{{{{fig.to_json()}}}}</PLOTLY_JSON>
- Não adicione explicações dentro das tags.
- As análises devem ser consistentes com os dados disponíveis.
- Se detectar inconsistências, recomende verificações, mas não faça suposições fora do contexto do CSV.
- Sempre responda de forma estruturada, com raciocínio técnico e conclusões objetivas.
- Se a análise envolver possíveis fraudes ou anomalias, descreva os indícios de maneira técnica e neutra, sem juízo de valor.
"""
        response_text = self.llm.predict(prompt)
        result = {"answer": response_text}

        # Extrai Plotly JSON se houver
        start_tag, end_tag = "<PLOTLY_JSON>", "</PLOTLY_JSON>"
        if start_tag in response_text and end_tag in response_text:
            result["plotly_json"] = response_text.split(start_tag)[1].split(end_tag)[0].strip()

        return result