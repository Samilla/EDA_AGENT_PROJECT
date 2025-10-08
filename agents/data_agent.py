import pandas as pd
import io

class DataAgent:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path)

    def describe_data(self):
        """Estatísticas básicas"""
        return self.df.describe(include='all')

    def generate_markdown_report(self, analysis_text: str) -> str:
        buf = io.StringIO()
        buf.write("# 🧾 Relatório de Análise de Dados\n\n")
        buf.write(f"- Linhas: {self.df.shape[0]}\n")
        buf.write(f"- Colunas: {self.df.shape[1]}\n\n")
        buf.write("## 📊 Estatísticas Descritivas\n\n")
        buf.write(self.df.describe(include='all').to_markdown() + "\n\n")
        buf.write("## 💡 Conclusões da IA\n\n")
        buf.write(analysis_text + "\n\n")
        buf.write("_Relatório gerado automaticamente pelo Agente EDA._")
        return buf.getvalue()