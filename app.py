import streamlit as st
import pandas as pd
from metode.saw import hitung_saw
from metode.wp import hitung_wp
from metode.topsis import hitung_topsis
from metode.ahp import hitung_ahp

def highlight_rank1(row):
    if 'Ranking' in row and row['Ranking'] == 1:
        return ['background-color: lightgreen; font-weight: bold'] * len(row)
    return [''] * len(row)

st.set_page_config(page_title="Kalkulator MCDM", layout="centered")

# ============================================================
# HEADER UTAMA
# ============================================================
st.markdown(
    """
    <h1 style='text-align: center; color: black;'> Aplikasi Pengambilan Keputusan Multi Kriteria (MCDM) </h1>
    <p style='text-align: center; color: gray;'> SAW · WP · TOPSIS · AHP </p>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ============================================================
# PILIHAN METODE
# ============================================================
with st.container():
    st.subheader("Metode Perhitungan")
    col1, col2, col3 = st.columns([1, 2, 1])

    metode_list = ["SAW", "WP", "TOPSIS", "AHP"]

    # Inisialisasi session_state kalau belum ada
    if "metode_aktif" not in st.session_state:
        st.session_state.metode_aktif = metode_list[0]

    # Gunakan index berdasarkan metode_aktif
    metode_index = metode_list.index(st.session_state.metode_aktif)

    # Pilihan metode tanpa key, biar tidak tumpang tindih dengan session_state
    metode_baru = st.selectbox(
        "**Pilih Metode**",
        metode_list,
        index=metode_index
    )

    # Langsung update session_state bila berubah
    if metode_baru != st.session_state.metode_aktif:
        st.session_state.metode_aktif = metode_baru
        st.rerun()  # paksa rerun biar langsung pindah tanpa klik dua kali

    metode = st.session_state.metode_aktif

# ============================================================
# INPUT JUMLAH KRITERIA DAN ALTERNATIF
# ============================================================
with st.container():
    st.subheader("Input Dasar")

    # Simpan jumlah kriteria & alternatif di session_state agar tidak reset saat rerun
    if "n_kriteria" not in st.session_state:
        st.session_state.n_kriteria = 3
    if "n_alternatif" not in st.session_state:
        st.session_state.n_alternatif = 3

    col1, col2 = st.columns(2)
    with col1:
        n_kriteria = st.number_input(
            "**Jumlah Kriteria**", 1, 10, st.session_state.n_kriteria, key="input_kriteria"
        )
    with col2:
        n_alternatif = st.number_input(
            "**Jumlah Alternatif**", 1, 10, st.session_state.n_alternatif, key="input_alternatif"
        )

    # Update session_state jika berubah
    if n_kriteria != st.session_state.n_kriteria:
        st.session_state.n_kriteria = n_kriteria
    if n_alternatif != st.session_state.n_alternatif:
        st.session_state.n_alternatif = n_alternatif

st.markdown("---")

# ============================================================
# INPUT NAMA KRITERIA & ALTERNATIF
# ============================================================
st.subheader("Nama Kriteria")
cols_kriteria = st.columns(3)
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
# BAGIAN SAW / WP / TOPSIS
# ============================================================
if metode in ["SAW", "WP", "TOPSIS"]:
    st.subheader("Input Tipe & Bobot Kriteria")

    # Simpan tipe & bobot di session_state
    if "tipe" not in st.session_state:
        st.session_state.tipe = ["Benefit"] * n_kriteria
    elif len(st.session_state.tipe) != n_kriteria:
        st.session_state.tipe = (st.session_state.tipe + ["Benefit"] * n_kriteria)[:n_kriteria]

    if "bobot" not in st.session_state:
        st.session_state.bobot = [1.0/n_kriteria] * n_kriteria
    elif len(st.session_state.bobot) != n_kriteria:
        st.session_state.bobot = (st.session_state.bobot + [1.0/n_kriteria] * n_kriteria)[:n_kriteria]

    with st.expander("Tipe & Bobot Kriteria", expanded=True):
        tipe, bobot = [], []
        for i in range(n_kriteria):
            col1, col2 = st.columns(2)
            with col1:
                tipe_val = st.selectbox(
                    f"Tipe {kriteria[i]}",
                    ["Benefit", "Cost"],
                    index=["Benefit", "Cost"].index(st.session_state.tipe[i]),
                    key=f"type{i}"
                )
                tipe.append(tipe_val)
                st.session_state.tipe[i] = tipe_val

            with col2:
                default_val = st.session_state.bobot[i]
                bobot_val = st.number_input(
                    f"Bobot {kriteria[i]}",
                    min_value=0.0,
                    value=float(default_val),
                    step=0.01,
                    key=f"bobot{i}"
                )
                bobot.append(bobot_val)
                st.session_state.bobot[i] = bobot_val

    # ============================================================
    # SIMPAN DATAFRAME NILAI ALTERNATIF X KRITERIA
    # ============================================================
    if "df_data" not in st.session_state:
        st.session_state.df_data = pd.DataFrame(
            [[50.0 for _ in range(n_kriteria)] for _ in range(n_alternatif)],
            columns=kriteria, index=alternatif
        )
    else:
        # Pastikan kolom dan index selalu sinkron dengan input
        old_df = st.session_state.df_data.copy()

        for k in kriteria:
            if k not in old_df.columns:
                old_df[k] = 50.0
        old_df = old_df[[c for c in old_df.columns if c in kriteria]]

        for a in alternatif:
            if a not in old_df.index:
                old_df.loc[a] = [50.0] * len(kriteria)
        old_df = old_df.loc[[a for a in old_df.index if a in alternatif]]

        # Urutkan ulang
        st.session_state.df_data = old_df.reindex(index=alternatif, columns=kriteria)

    st.markdown("### Input Nilai Alternatif x Kriteria")
    df = st.data_editor(
        st.session_state.df_data,
        use_container_width=True,
        num_rows="dynamic",
        key="data_editor"
    )

    # Perbarui session_state hanya sekali setelah edit
    if not df.equals(st.session_state.df_data):
        st.session_state.df_data = df

    if st.button("Hitung", type="primary"):
        if metode == "SAW":
            hasil = hitung_saw(df, bobot, tipe)
        elif metode == "WP":
            hasil = hitung_wp(df, bobot, tipe)
        elif metode == "TOPSIS":
            hasil, solusi_ideal = hitung_topsis(df, bobot, tipe)
            st.subheader("Solusi Ideal (A⁺ dan A⁻)")
            st.dataframe(solusi_ideal, use_container_width=True)

        st.subheader("Hasil Perhitungan dan Ranking")
        styled_df = hasil.style.apply(highlight_rank1, axis=1)
        st.markdown(styled_df.to_html(), unsafe_allow_html=True)

# ============================================================
# BAGIAN AHP
# ============================================================
elif metode == "AHP":
    st.subheader("Tipe Kriteria")
    tipe = [st.selectbox(f"Tipe {kriteria[i]}", ["Benefit", "Cost"], key=f"type{i}") for i in range(n_kriteria)]
    st.markdown("---")

    st.markdown("### Matriks Perbandingan Antar Kriteria")
    df_matrix = pd.DataFrame([[1.0 if i == j else 1.0 for j in range(n_kriteria)] for i in range(n_kriteria)],
                             columns=kriteria, index=kriteria)

    for i in range(n_kriteria):
        for j in range(i+1, n_kriteria):
            df_matrix.iloc[i, j] = st.number_input(
                f"{kriteria[i]} dibanding {kriteria[j]}",
                min_value=0.1, max_value=9.0, value=1.0, key=f"k{i}{j}"
            )
            df_matrix.iloc[j, i] = round(1 / df_matrix.iloc[i, j], 4)

    st.dataframe(df_matrix, use_container_width=True)
    st.markdown("---")

    matriks_kriteria = df_matrix.values.tolist()
    matriks_alternatif = []
    
    st.markdown("### Matriks Perbandingan Alternatif")
    for k in range(n_kriteria):
        with st.expander(f"**Kriteria {kriteria[k]}**", expanded=False):
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

    if st.button("Hitung", type="primary"):
        hasil = hitung_ahp(kriteria, matriks_kriteria, alternatif, matriks_alternatif)

        st.subheader("Bobot Kriteria")
        st.dataframe(pd.DataFrame({"Kriteria": kriteria, "Bobot": hasil["bobot_kriteria"]}), use_container_width=True)
        cr_krit = hasil['cr_kriteria']
        status_krit = "Konsisten" if cr_krit <= 0.1 else "Tidak Konsisten"
        st.markdown(f"**CR Kriteria = {cr_krit:.3f}** ({':green['+status_krit+']' if cr_krit <= 0.1 else ':red['+status_krit+']'})")

        for i, k in enumerate(kriteria):
            st.write(f"### Bobot Lokal Alternatif untuk {k}")
            st.dataframe(pd.DataFrame({"Alternatif": alternatif, "Bobot": hasil["bobot_alternatif_lokal"][i]}))
            cr_alt = hasil['cr_alternatif'][i]
            status_alt = "Konsisten" if cr_alt <= 0.1 else "Tidak Konsisten"
            st.markdown(f"**CR = {cr_alt:.3f}** ({':green['+status_alt+']' if cr_alt <= 0.1 else ':red['+status_alt+']'})")

        st.subheader("Hasil Perhitungan dan Ranking")
        styled_df_ahp = hasil["hasil_df"].style.apply(highlight_rank1, axis=1)
        st.markdown(styled_df_ahp.to_html(), unsafe_allow_html=True)
