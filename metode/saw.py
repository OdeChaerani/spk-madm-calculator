import pandas as pd
import numpy as np

def hitung_saw(df, bobot, tipe):
    matrix = df.values.astype(float)
    norm = np.zeros_like(matrix, dtype=float)

    for j in range(len(tipe)):
        if tipe[j] == "benefit":
            norm[:, j] = matrix[:, j] / np.max(matrix[:, j])
        else:
            # Hindari pembagian dengan nol
            col = np.where(matrix[:, j] == 0, 1e-9, matrix[:, j])
            norm[:, j] = np.min(col) / col

    # Normalisasi bobot
    w = np.array(bobot) / np.sum(bobot)

    # Skor akhir
    skor = np.dot(norm, w)

    hasil = pd.DataFrame({
        "Alternatif": df.index,
        "Skor": skor,
        "Ranking": pd.Series(skor).rank(ascending=False, method='dense').astype(int)
    }).sort_values("Ranking")

    return hasil
