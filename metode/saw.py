import pandas as pd
import numpy as np

def normalisasi_matrix(df, tipe):
    """Normalisasi matriks sesuai tipe kriteria (benefit/cost)"""
    matrix = df.values.astype(float)
    norm = np.zeros_like(matrix, dtype=float)

    for j in range(len(tipe)):
        if tipe[j] == "benefit":
            norm[:, j] = matrix[:, j] / np.max(matrix[:, j])
        else:
            col = np.where(matrix[:, j] == 0, 1e-9, matrix[:, j])
            norm[:, j] = np.min(col) / col
    return norm


def hitung_saw(df, bobot, tipe):
    """Fungsi utama untuk menghitung SAW."""
    if len(bobot) != df.shape[1] or len(tipe) != df.shape[1]:
        raise ValueError("Jumlah bobot dan tipe harus sama dengan jumlah kolom")

    norm = normalisasi_matrix(df, tipe)
    w = np.array(bobot)
    
    # Cek apakah bobot sudah ternormalisasi
    if not np.isclose(np.sum(w), 1.0):
        print("⚠️ Bobot tidak ternormalisasi, melakukan normalisasi otomatis...")
        w = w / np.sum(w)
    
    skor = np.dot(norm, w)

    hasil = pd.DataFrame({
        "Alternatif": df.index,
        "Skor": skor,
        "Ranking": pd.Series(skor).rank(ascending=False, method='dense').astype(int)
    }).sort_values("Ranking").reset_index(drop=True)

    return hasil


# ======== CONTOH PENGGUNAAN ========
data = {
    'Quality': [8, 7, 9],
    'Price': [300, 250, 350],
    'Warranty': [2, 3, 1],
    'Delivery': [5, 7, 3]
}

df = pd.DataFrame(data, index=['A1', 'A2', 'A3'])

bobot = [0.4658, 0.1611, 0.2771, 0.096]
tipe = ["benefit", "cost", "benefit", "cost"]

hasil = hitung_saw(df, bobot, tipe)

print("=" * 60)
print("HASIL ANALISIS SAW")
print("=" * 60)
print(hasil)
print("\n🏆 SUPPLIER TERBAIK:", hasil.iloc[0]['Alternatif'], 
      f"(Skor: {hasil.iloc[0]['Skor']:.4f})")
print("=" * 60)