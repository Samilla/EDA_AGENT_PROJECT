# -*- coding: utf-8 -*-
"""
Agente Analista de Dados (Analyst Agent)
-----------------------------------------
Responsável por interpretar os dados do CSV, realizar análises EDA (Exploratórias),
gerar gráficos com Plotly e retornar conclusões em texto ou relatório Markdown.

Versão otimizada:
✔ Usa Gemini 2.5 Flash
✔ Substitui .predict() → .invoke()
✔ Tolerante a timeouts e falhas temporárias
✔ Gera relatórios Markdown resumidos (sem gastar muita cota)
"""

import pandas as pd
import plotly.express as px
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import time


class AnalystAgent:
    def __init__(self, api_key: str):
        """Inicializa o analista com o modelo Gemini 2.5 Flash."""
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.3,
            google_api_key=api_key,
            max_output_tokens=2048,
        )

        self.analyst_prompt = PromptTemplate.from_template("""
        Você é um analista de dados especialista em detecção de fraudes e EDA.
        Use apenas o CSV {csv_path} para responder.
        Quando precisar gerar gráficos, use a biblioteca Plotly e retorne APENAS:
        <PLOTLY_JSON>{{fig.to_json()}}</PLOTLY_JSON>
        Não adicione explicações dentro das tags.

        Objetivo: gerar análises úteis, estatísticas e conclusões.
        Mostre médias, medianas, correlações, e destaque possíveis anomalias.

        Pergunta do usuário:
        {user_question}
        """)

    def analyze(self, csv_path: str, user_question: str):
        """
        Realiza a análise principal com Gemini.
        Retorna texto interpretado ou gráficos (Plotly JSON).
        """

        # Monta o prompt com base no CSV e pergunta do usuário
        prompt = self.analyst_prompt.format(csv_path=csv_path, user_question=user_question)

        # Tenta algumas vezes em caso de timeout (504)
        for attempt in range(3):
            try:
                response = self.llm.invoke(prompt)
                response_text = response.content if hasattr(response, "content") else str(response)
                return response_text
            except Exception as e:
                print(f"Tentativa {attempt + 1} falhou: {e}")
                if "DeadlineExceeded" in str(e) or "504" in str(e):
                    time.sleep(3)
                    continue
                raise e

        return "Ocorreu um erro ao processar a análise. Tente novamente com um arquivo menor ou uma pergunta mais específica."

    def generate_report(self, df: pd.DataFrame) -> str:
        """
        Gera automaticamente um relatório resumido em Markdown sobre o dataset,
        sem gastar cota da API (usa apenas pandas localmente).
        """
        report = []
        report.append("# 📊 Relatório de Análise Exploratória (EDA)\n")

        report.append("## 1️⃣ Estrutura dos Dados")
        report.append(f"- Total de linhas: **{df.shape[0]}**")
        report.append(f"- Total de colunas: **{df.shape[1]}**")
        report.append(f"- Colunas: {', '.join(df.columns)}\n")

        report.append("## 2️⃣ Tipos de Dados")
        report.append(str(df.dtypes.to_markdown()))

        report.append("\n## 3️⃣ Estatísticas Descritivas")
        report.append(df.describe(include='all').to_markdown())

        report.append("\n## 4️⃣ Dados Faltantes")
        missing = df.isnull().sum()
        report.append(missing.to_markdown())

        report.append("\n## 5️⃣ Possíveis Conclusões")
        if df.isnull().sum().sum() > 0:
            report.append("- Existem valores ausentes que devem ser tratados.")
        if any(df.nunique() == 1):
            report.append("- Algumas colunas têm valores únicos, sem variabilidade.")
        if df.shape[1] > 10:
            report.append("- O dataset é amplo, recomenda-se focar nas colunas mais relevantes.")

        report.append("\n_Gerado automaticamente pelo Analista EDA IA — versão otimizada._")

        return "\n".join(report)
