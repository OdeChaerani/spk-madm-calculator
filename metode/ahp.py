import pandas as pd

def normalisasi_matriks(m):
    n = len(m)
    kolom_jumlah = [sum(m[i][j] for i in range(n)) for j in range(n)]
    normalisasi = [[m[i][j] / kolom_jumlah[j] for j in range(n)] for i in range(n)]
    rata_baris = [sum(normalisasi[i]) / n for i in range(n)]
    return normalisasi, rata_baris

def hitung_consistency_ratio(m, priority_vector):
    n = len(m)
    lambda_max = sum(sum(m[i][j] * priority_vector[j] for j in range(n)) / priority_vector[i] for i in range(n)) / n
    ci = (lambda_max - n) / (n - 1) if n > 1 else 0
    RI = {1:0, 2:0, 3:0.58, 4:0.9, 5:1.12, 6:1.24, 7:1.32, 8:1.41, 9:1.45, 10:1.49}
    cr = ci / RI.get(n, 1)
    return cr

def hitung_ahp(kriteria, matriks_kriteria, alternatif, matriks_alternatif):
    # Bobot kriteria
    norm_kriteria, bobot_kriteria = normalisasi_matriks(matriks_kriteria)
    cr_kriteria = hitung_consistency_ratio(matriks_kriteria, bobot_kriteria)

    # Bobot lokal alternatif per kriteria
    bobot_alternatif_lokal = []
    cr_alternatif = []
    for k in range(len(kriteria)):
        norm_alt, bobot_alt = normalisasi_matriks(matriks_alternatif[k])
        bobot_alternatif_lokal.append(bobot_alt)
        cr_alt = hitung_consistency_ratio(matriks_alternatif[k], bobot_alt)
        cr_alternatif.append(cr_alt)

    # Bobot global
    skor_global = []
    for i in range(len(alternatif)):
        total = sum(bobot_alternatif_lokal[j][i] * bobot_kriteria[j] for j in range(len(kriteria)))
        skor_global.append(total)

    ranking = sorted(zip(alternatif, skor_global), key=lambda x: x[1], reverse=True)

    hasil_df = pd.DataFrame({
        "Alternatif": alternatif,
        "Skor": skor_global
    }).sort_values("Skor", ascending=False)
    hasil_df["Ranking"] = range(1, len(hasil_df) + 1)

    return {
        "bobot_kriteria": bobot_kriteria,
        "cr_kriteria": cr_kriteria,
        "bobot_alternatif_lokal": bobot_alternatif_lokal,
        "cr_alternatif": cr_alternatif,
        "hasil_df": hasil_df,
        "ranking": ranking
    }
