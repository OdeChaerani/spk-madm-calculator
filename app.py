import streamlit as st
import pandas as pd
from metode.saw import hitung_saw
from metode.wp import hitung_wp
from metode.topsis import hitung_topsis
from metode.ahp import hitung_ahp

# Layout tidak full layar
st.set_page_config(page_title="MCDM App", layout="centered")

# Judul utama
st.title("🧮 Aplikasi Pengambilan Keputusan Multi Kriteria (MCDM)")
st.markdown("---")

# Pilihan metode  di tengah
st.markdown("### Pilih Metode Perhitungan")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    metode = st.selectbox("Pilih Metode:", ["SAW", "WP", "TOPSIS", "AHP"])

col1, col2 = st.columns([1, 1])
with col1:
    n_kriteria = st.number_input("Jumlah Kriteria", 1, 10, 3, key="kriteria")
with col2:
    n_alternatif = st.number_input("Jumlah Alternatif", 1, 10, 3, key="alternatif")

st.markdown("---")

# Input umum
st.subheader("Nama Kriteria")
cols_kriteria = st.columns(3)  # tampilkan 3 kolom sejajar
kriteria = []
for i in range(n_kriteria):
    with cols_kriteria[i % 3]:
        kriteria.append(st.text_input(f"Kriteria {i+1}", f"C{i+1}"))

st.subheader("Nama Alternatif")
cols_alt = st.columns(3)
alternatif = []
for i in range(n_alternatif):
    with cols_alt[i % 3]:
        alternatif.append(st.text_input(f"Alternatif {i+1}", f"A{i+1}"))

st.markdown("---")

# ============================================================
# BAGIAN INPUT UNTUK METODE SAW, WP, TOPSIS
# ============================================================
if metode in ["SAW", "WP", "TOPSIS"]:
    with st.container():
        st.subheader("Input Jenis & Bobot Kriteria")
        tipe = []
        bobot = []
        for i in range(n_kriteria):
            col1, col2 = st.columns(2)
            with col1:
                tipe.append(st.selectbox(f"Jenis {kriteria[i]}", ["benefit", "cost"], key=f"type{i}"))
            with col2:
                if metode == "WP":
                    bobot.append(st.number_input(f"Bobot {kriteria[i]}", min_value=0.0, value=1.0, step=0.1, key=f"bobot{i}"))
                else:
                    bobot.append(st.number_input(f"Bobot {kriteria[i]}", min_value=0.0, max_value=1.0, value=1.0/n_kriteria, step=0.01, key=f"bobot{i}"))
        st.subheader("Input Nilai Alternatif × Kriteria")

        # Membuat DataFrame awal
        df_default = pd.DataFrame(
            [[50.0 for _ in range(n_kriteria)] for _ in range(n_alternatif)],
            columns=kriteria,
            index=alternatif
        )

        # Editable data table
        df = st.data_editor(
            df_default,
            use_container_width=True,
            num_rows="dynamic",
            key="data_editor"
        )

        st.write("### Matriks Keputusan")
        st.dataframe(df, use_container_width=True)

        if st.button("🔢 Hitung"):
            if metode == "SAW":
                hasil = hitung_saw(df, bobot, tipe)
            elif metode == "WP":
                hasil = hitung_wp(df, bobot, tipe)
            elif metode == "TOPSIS":
                hasil, solusi_ideal = hitung_topsis(df, bobot, tipe)
                st.subheader("Solusi Ideal (A⁺ dan A⁻)")
                st.dataframe(solusi_ideal, use_container_width=True)

            st.subheader("📊 Hasil Perhitungan dan Ranking")
            st.dataframe(hasil, use_container_width=True)

# ============================================================
# METODE AHP
# ============================================================
elif metode == "AHP":
    with st.container():
        st.subheader("Input Jenis Kriteria (Benefit/Cost)")
        tipe = [st.selectbox(f"Jenis {kriteria[i]}", ["benefit", "cost"], key=f"type{i}") for i in range(n_kriteria)]

        st.markdown("### Matriks Perbandingan Antar Kriteria")
        st.markdown(
            "Isikan nilai **perbandingan berpasangan antar kriteria** (skala 1–9). "
            "Bagian bawah tabel otomatis dihitung sebagai kebalikannya."
        )

        # Buat matriks default
        df_matrix = pd.DataFrame([[1.0 if i == j else 1.0 for j in range(n_kriteria)] for i in range(n_kriteria)],
                                 columns=kriteria, index=kriteria)

        # Editable bagian atas saja
        for i in range(n_kriteria):
            for j in range(i+1, n_kriteria):
                df_matrix.iloc[i, j] = st.number_input(
                    f"{kriteria[i]} dibanding {kriteria[j]}",
                    min_value=0.1, max_value=9.0, value=1.0, key=f"k{i}{j}"
                )
                df_matrix.iloc[j, i] = round(1 / df_matrix.iloc[i, j], 4)

        st.write("📋 Matriks Perbandingan Kriteria")
        st.dataframe(df_matrix, use_container_width=True)

        # Simpan matriks ke list of lists untuk hitung
        matriks_kriteria = df_matrix.values.tolist()

        # ============================================================
        # Matriks perbandingan alternatif untuk tiap kriteria
        # ============================================================
        matriks_alternatif = []
        for k in range(n_kriteria):
            st.markdown(f"### Matriks Perbandingan Alternatif untuk Kriteria **{kriteria[k]}**")
            st.markdown("Isi nilai pada segitiga atas, bagian bawah otomatis diisi kebalikannya.")

            df_alt = pd.DataFrame(
                [[1.0 if i == j else 1.0 for j in range(n_alternatif)] for i in range(n_alternatif)],
                columns=alternatif, index=alternatif
            )

            for i in range(n_alternatif):
                for j in range(i+1, n_alternatif):
                    df_alt.iloc[i, j] = st.number_input(
                        f"{alternatif[i]} dibanding {alternatif[j]} (Kriteria {kriteria[k]})",
                        min_value=0.1, max_value=9.0, value=1.0, key=f"a{k}{i}{j}"
                    )
                    df_alt.iloc[j, i] = round(1 / df_alt.iloc[i, j], 4)

            st.dataframe(df_alt, use_container_width=True)
            matriks_alternatif.append(df_alt.values.tolist())

        if st.button("🔢 Hitung"):
            hasil = hitung_ahp(kriteria, matriks_kriteria, alternatif, matriks_alternatif)

            st.subheader("📘 Bobot Kriteria")
            st.write(pd.DataFrame({"Kriteria": kriteria, "Bobot": hasil["bobot_kriteria"]}))
            st.write(f"CR Kriteria = {hasil['cr_kriteria']:.3f} "
                     f"{'✅ (Konsisten)' if hasil['cr_kriteria'] <= 0.1 else '⚠️ (Tidak Konsisten)'}")

            for i, k in enumerate(kriteria):
                st.write(f"### Bobot Lokal Alternatif untuk {k}")
                df_alt = pd.DataFrame({
                    "Alternatif": alternatif,
                    "Bobot": hasil["bobot_alternatif_lokal"][i]
                })
                st.dataframe(df_alt)
                st.write(f"CR = {hasil['cr_alternatif'][i]:.3f} "
                         f"{'✅ (Konsisten)' if hasil['cr_alternatif'][i] <= 0.1 else '⚠️ (Tidak Konsisten)'}")

            st.subheader("📊 Hasil Akhir dan Ranking Global")
            st.dataframe(hasil["hasil_df"], use_container_width=True)