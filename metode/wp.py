import numpy as np
import pandas as pd

def hitung_wp(df, bobot, tipe):
    matrix = df.values.astype(float)
    w = np.array(bobot) / np.sum(bobot)

    log_s = np.zeros(len(matrix))
    for i in range(len(matrix)):
        for j in range(len(w)):
            x = matrix[i, j]
            if x <= 0:
                x = 1e-9 
            if tipe[j].lower() == "benefit":
                log_s[i] += w[j] * np.log(x)
            else:  
                log_s[i] += w[j] * np.log(1.0 / x)

    s = np.exp(log_s)
    v = s / np.sum(s)

    hasil = pd.DataFrame({
        "Alternatif": df.index,
        "Skor": v
    })
    hasil["Ranking"] = hasil["Skor"].rank(ascending=False, method="dense").astype(int)
    hasil = hasil.sort_values("Ranking").reset_index(drop=True)
    return hasil
