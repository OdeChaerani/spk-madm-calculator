import pandas as pd
import numpy as np

def hitung_topsis(df, bobot, tipe):
    df = df.apply(pd.to_numeric, errors='coerce').fillna(0)
    
    matrix = df.values.astype(float)
    
    col_sums = np.sqrt((matrix ** 2).sum(axis=0))
    col_sums[col_sums == 0] = 1
    norm = matrix / col_sums
    
    w = np.array(bobot)
    y = norm * w

    ideal_plus = np.max(y, axis=0)
    ideal_minus = np.min(y, axis=0)

    for j in range(len(tipe)):
        if tipe[j].lower() == "cost":
            ideal_plus[j], ideal_minus[j] = ideal_minus[j], ideal_plus[j]

    d_plus = np.sqrt(((y - ideal_plus) ** 2).sum(axis=1))
    d_minus = np.sqrt(((y - ideal_minus) ** 2).sum(axis=1))
    total_d = d_plus + d_minus
    total_d[total_d == 0] = 1
    v = d_minus / total_d

    v = np.nan_to_num(v, nan=0, posinf=0, neginf=0)

    solusi_ideal = pd.DataFrame({
        "Kriteria": df.columns,
        "Ideal_Positive (A⁺)": ideal_plus,
        "Ideal_Negative (A⁻)": ideal_minus
    })

    hasil = pd.DataFrame({
        "Alternatif": df.index,
        "Skor": v,
        "Ranking": pd.Series(v).rank(ascending=False, method="min").fillna(0).astype(int)
    }).sort_values("Ranking").reset_index(drop=True)

    return hasil, solusi_ideal
