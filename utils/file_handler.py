# -*- coding: utf-8 -*-
"""
Gerencia arquivos temporários (upload, limpeza etc.)
"""

import os
import tempfile


def save_uploaded_file(uploaded_file):
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())
    return file_path
