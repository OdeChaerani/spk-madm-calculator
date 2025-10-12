import pandas as pd
import numpy as np

def normalisasi_matrix(df, tipe):  # Normalisasi matriks sesuai tipe kriteria (benefit/cost)
    matrix = df.values.astype(float)
    norm = np.zeros_like(matrix, dtype=float)

    for j in range(len(tipe)):
        if tipe[j] == "benefit":
            norm[:, j] = matrix[:, j] / np.max(matrix[:, j])
        else:
            col = np.where(matrix[:, j] == 0, 1e-9, matrix[:, j])
            norm[:, j] = np.min(col) / col
    return norm


def normalisasi_bobot(bobot):  # Menormalisasi bobot agar total = 1
    w = np.array(bobot)
    return w / np.sum(w)


def hitung_saw(df, bobot, tipe):
    """Fungsi utama untuk menghitung SAW."""
    if len(bobot) != df.shape[1] or len(tipe) != df.shape[1]:
        raise ValueError("Jumlah bobot dan tipe harus sama dengan jumlah kolom di dataframe")

    norm = normalisasi_matrix(df, tipe)
    w = normalisasi_bobot(bobot)
    skor = np.dot(norm, w)

    hasil = pd.DataFrame({
        "Alternatif": df.index,
        "Skor": skor,
        "Ranking": pd.Series(skor).rank(ascending=False, method='dense').astype(int)
    }).sort_values("Ranking").reset_index(drop=True)

    return hasil
