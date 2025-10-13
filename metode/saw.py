import pandas as pd
import numpy as np

def hitung_saw(df, bobot, tipe):
    if len(bobot) != df.shape[1] or len(tipe) != df.shape[1]:
        raise ValueError("Jumlah bobot dan tipe harus sama dengan jumlah kolom pada DataFrame.")

    matrix = df.values.astype(float)
    norm = np.zeros_like(matrix, dtype=float)

    for j in range(len(tipe)):
        if tipe[j].lower() == 'benefit':
            norm[:, j] = matrix[:, j] / np.max(matrix[:, j])
        else:
            col = np.where(matrix[:, j] == 0, 1e-9, matrix[:, j])
            norm[:, j] = np.min(col) / col

    w = np.array(bobot) / np.sum(bobot)
    skor = np.dot(norm, w)

    hasil = pd.DataFrame({
        "Alternatif": df.index,
        "Skor": skor
    })
    hasil["Ranking"] = hasil["Skor"].rank(ascending=False, method="dense").astype(int)
    hasil = hasil.sort_values("Ranking").reset_index(drop=True)

    return hasil