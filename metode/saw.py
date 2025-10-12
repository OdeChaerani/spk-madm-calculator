import pandas as pd
import numpy as np

def hitung_saw(df, bobot, tipe):
    # --- Validasi input ---
    if len(bobot) != df.shape[1] or len(tipe) != df.shape[1]:
        raise ValueError("Jumlah bobot dan tipe harus sama dengan jumlah kolom pada DataFrame.")

    # --- Normalisasi matriks ---
    matrix = df.values.astype(float)
    norm = np.zeros_like(matrix, dtype=float)

    for j in range(len(tipe)):
        if tipe[j].lower() == 'benefit':
            norm[:, j] = matrix[:, j] / np.max(matrix[:, j])
        else:  # cost
            col = np.where(matrix[:, j] == 0, 1e-9, matrix[:, j])
            norm[:, j] = np.min(col) / col

    df_norm = pd.DataFrame(norm, columns=df.columns, index=df.index)

    # --- Normalisasi bobot ---
    w = np.array(bobot) / np.sum(bobot)

    # --- Hitung skor total ---
    skor = np.dot(norm, w)

    # --- Buat hasil ranking ---
    hasil = pd.DataFrame({
        "Alternatif": df.index,
        "Skor": skor
    })
    hasil["Ranking"] = hasil["Skor"].rank(ascending=False, method="dense").astype(int)
    hasil = hasil.sort_values("Ranking").reset_index(drop=True)

    return hasil, df_norm