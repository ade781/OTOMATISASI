import pandas as pd
import os


def load_data(filepath):
    """Membaca file Excel dan memastikan kolom Status ada."""
    if os.path.exists(filepath):
        df = pd.read_excel(filepath)
        # Bersihkan nama kolom header biar standar (Title Case)
        df.columns = [c.strip().title() for c in df.columns]

        if 'Status' not in df.columns:
            df['Status'] = ''
        return df
    return None


def save_data(df, filepath):
    """Menyimpan perubahan ke Excel."""
    try:
        df.to_excel(filepath, index=False)
        return True
    except Exception as e:
        print(f"Gagal save Excel: {e}")
        return False
