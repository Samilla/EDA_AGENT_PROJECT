import tempfile
import zipfile
import pandas as pd

def unzip_and_read_file(uploaded_file):
    file_ext = uploaded_file.name.lower().split('.')[-1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp_path = tmp.name

    try:
        if file_ext == "zip":
            with zipfile.ZipFile(uploaded_file, 'r') as zf:
                csv_files = [f for f in zf.namelist() if f.endswith(".csv")]
                if not csv_files:
                    return None, None
                with zf.open(csv_files[0]) as f:
                    df = pd.read_csv(f)
                    df.to_csv(tmp_path, index=False)
        else:
            df = pd.read_csv(uploaded_file)
            df.to_csv(tmp_path, index=False)

        return tmp_path, df
    except Exception as e:
        print(f"Erro ao processar arquivo: {e}")
        return None, None