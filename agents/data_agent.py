# -*- coding: utf-8 -*-
"""
Agente de Dados
---------------
Responsável por carregar e validar os dados enviados pelo usuário.
Aceita arquivos CSV normais ou ZIP contendo CSVs.
"""

import pandas as pd
import zipfile
import tempfile
import os


class DataAgent:
    def load_data(self, uploaded_file):
        """
        Lê o arquivo CSV ou ZIP e retorna o DataFrame carregado e o caminho salvo.
        """
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        if uploaded_file.name.endswith(".zip"):
            with zipfile.ZipFile(file_path, "r") as zip_ref:
                zip_ref.extractall(temp_dir)
                csv_files = [f for f in os.listdir(temp_dir) if f.endswith(".csv")]
                if not csv_files:
                    raise ValueError("Nenhum arquivo CSV encontrado dentro do ZIP.")
                file_path = os.path.join(temp_dir, csv_files[0])

        df = pd.read_csv(file_path, encoding="utf-8", low_memory=False)
        return df, file_path
