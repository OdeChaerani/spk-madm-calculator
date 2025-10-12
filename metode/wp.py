import pandas as pd
import numpy as np

def hitung_wp(df, bobot, tipe):
    matrix = df.values.astype(float)
    w = np.array(bobot) / sum(bobot)
    
    s = np.ones(len(matrix))
    for i in range(len(matrix)):
        for j in range(len(w)):
            if tipe[j] == "benefit":
                s[i] *= matrix[i, j] ** w[j]
            else:
                s[i] *= (1 / matrix[i, j]) ** w[j]
    
    v = s / np.sum(s)
    hasil = pd.DataFrame({
        "Alternatif": df.index,
        "Skor": v,
        "Ranking": pd.Series(v).rank(ascending=False).astype(int)
    }).sort_values("Ranking")
    return hasil
