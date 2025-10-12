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
# INITIALIZE SESSION STATE
# ============================================================
if 'metode' not in st.session_state:
    st.session_state.metode = "SAW"
if 'n_kriteria' not in st.session_state:
    st.session_state.n_kriteria = 3
if 'n_alternatif' not in st.session_state:
    st.session_state.n_alternatif = 3
if 'kriteria' not in st.session_state:
    st.session_state.kriteria = [f"C{i+1}" for i in range(3)]
if 'alternatif' not in st.session_state:
    st.session_state.alternatif = [f"A{i+1}" for i in range(3)]
if 'tipe' not in st.session_state:
    st.session_state.tipe = ["Benefit"] * 3
if 'bobot' not in st.session_state:
    st.session_state.bobot = [1.0/3] * 3
if 'data_df' not in st.session_state:
    st.session_state.data_df = pd.DataFrame(
        [[50.0 for _ in range(3)] for _ in range(3)],
        columns=[f"C{i+1}" for i in range(3)], 
        index=[f"A{i+1}" for i in range(3)]
    )

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
    with col2:
        metode = st.selectbox("*Pilih Metode*", ["SAW", "WP", "TOPSIS", "AHP"], 
                              index=["SAW", "WP", "TOPSIS", "AHP"].index(st.session_state.metode),
                              key="metode_select")
        st.session_state.metode = metode

# ============================================================
# INPUT JUMLAH KRITERIA DAN ALTERNATIF
# ============================================================
with st.container():
    st.subheader("Input Dasar")
    col1, col2 = st.columns(2)
    with col1:
        n_kriteria = st.number_input("*Jumlah Kriteria*", 1, 10, st.session_state.n_kriteria, key="kriteria_input")
        if n_kriteria != st.session_state.n_kriteria:
            st.session_state.n_kriteria = n_kriteria
            # Adjust kriteria list
            if n_kriteria > len(st.session_state.kriteria):
                st.session_state.kriteria.extend([f"C{i+1}" for i in range(len(st.session_state.kriteria), n_kriteria)])
            else:
                st.session_state.kriteria = st.session_state.kriteria[:n_kriteria]
            # Adjust tipe and bobot
            if n_kriteria > len(st.session_state.tipe):
                st.session_state.tipe.extend(["Benefit"] * (n_kriteria - len(st.session_state.tipe)))
            else:
                st.session_state.tipe = st.session_state.tipe[:n_kriteria]
            if n_kriteria > len(st.session_state.bobot):
                st.session_state.bobot.extend([1.0/n_kriteria] * (n_kriteria - len(st.session_state.bobot)))
            else:
                st.session_state.bobot = [b/sum(st.session_state.bobot[:n_kriteria]) for b in st.session_state.bobot[:n_kriteria]]
            st.rerun()

    with col2:
        n_alternatif = st.number_input("*Jumlah Alternatif*", 1, 10, st.session_state.n_alternatif, key="alternatif_input")
        if n_alternatif != st.session_state.n_alternatif:
            st.session_state.n_alternatif = n_alternatif
            # Adjust alternatif list
            if n_alternatif > len(st.session_state.alternatif):
                st.session_state.alternatif.extend([f"A{i+1}" for i in range(len(st.session_state.alternatif), n_alternatif)])
            else:
                st.session_state.alternatif = st.session_state.alternatif[:n_alternatif]
            st.rerun()

st.markdown("---")

# ============================================================
# INPUT NAMA KRITERIA & ALTERNATIF
# ============================================================
st.subheader("Nama Kriteria")
cols_kriteria = st.columns(3)
for i in range(st.session_state.n_kriteria):
    with cols_kriteria[i % 3]:
        st.session_state.kriteria[i] = st.text_input(f"Kriteria {i+1}", st.session_state.kriteria[i], key=f"kriteria_name_{i}")

st.subheader("Nama Alternatif")
cols_alt = st.columns(3)
for i in range(st.session_state.n_alternatif):
    with cols_alt[i % 3]:
        st.session_state.alternatif[i] = st.text_input(f"Alternatif {i+1}", st.session_state.alternatif[i], key=f"alternatif_name_{i}")
        
st.markdown("---")

# ============================================================
# BAGIAN SAW / WP / TOPSIS
# ============================================================
if st.session_state.metode in ["SAW", "WP", "TOPSIS"]:
    st.subheader("Input Tipe & Bobot Kriteria")
    with st.expander("Tipe & Bobot Kriteria", expanded=True):
        for i in range(st.session_state.n_kriteria):
            col1, col2 = st.columns(2)
            with col1:
                st.session_state.tipe[i] = st.selectbox(
                    f"Tipe {st.session_state.kriteria[i]}", 
                    ["Benefit", "Cost"], 
                    index=["Benefit", "Cost"].index(st.session_state.tipe[i]),
                    key=f"type{i}"
                )
            with col2:
                default_val = 1.0/st.session_state.n_kriteria if st.session_state.metode != "WP" else 1.0
                st.session_state.bobot[i] = st.number_input(
                    f"Bobot {st.session_state.kriteria[i]}", 
                    min_value=0.0, 
                    value=st.session_state.bobot[i], 
                    step=0.01, 
                    key=f"bobot{i}"
                )

    st.markdown("### Input Nilai Alternatif x Kriteria")
    
    # Update dataframe dengan nama terbaru
    st.session_state.data_df.columns = st.session_state.kriteria
    st.session_state.data_df.index = st.session_state.alternatif
    
    df_edited = st.data_editor(st.session_state.data_df, use_container_width=True, num_rows="dynamic", key="data_editor")
    st.session_state.data_df = df_edited

    if st.button("Hitung", type="primary"):
        if st.session_state.metode == "SAW":
            hasil = hitung_saw(st.session_state.data_df, st.session_state.bobot, st.session_state.tipe)
        elif st.session_state.metode == "WP":
            hasil = hitung_wp(st.session_state.data_df, st.session_state.bobot, st.session_state.tipe)
        elif st.session_state.metode == "TOPSIS":
            hasil, solusi_ideal = hitung_topsis(st.session_state.data_df, st.session_state.bobot, st.session_state.tipe)
            st.subheader("Solusi Ideal (A⁺ dan A⁻)")
            st.dataframe(solusi_ideal, use_container_width=True)

        st.subheader("Hasil Perhitungan dan Ranking")
        styled_df = hasil.style.apply(highlight_rank1, axis=1)
        st.markdown(styled_df.to_html(), unsafe_allow_html=True)

# ============================================================
# BAGIAN AHP
# ============================================================
elif st.session_state.metode == "AHP":
    st.subheader("Tipe Kriteria")
    for i in range(st.session_state.n_kriteria):
        st.session_state.tipe[i] = st.selectbox(
            f"Tipe {st.session_state.kriteria[i]}", 
            ["Benefit", "Cost"], 
            index=["Benefit", "Cost"].index(st.session_state.tipe[i]),
            key=f"type{i}"
        )
    st.markdown("---")

    st.markdown("### Matriks Perbandingan Antar Kriteria")
    df_matrix = pd.DataFrame(
        [[1.0 if i == j else 1.0 for j in range(st.session_state.n_kriteria)] for i in range(st.session_state.n_kriteria)],
        columns=st.session_state.kriteria, 
        index=st.session_state.kriteria
    )

    for i in range(st.session_state.n_kriteria):
        for j in range(i+1, st.session_state.n_kriteria):
            df_matrix.iloc[i, j] = st.number_input(
                f"{st.session_state.kriteria[i]} dibanding {st.session_state.kriteria[j]}",
                min_value=0.1, max_value=9.0, value=1.0, key=f"k{i}{j}"
            )
            df_matrix.iloc[j, i] = round(1 / df_matrix.iloc[i, j], 4)

    st.dataframe(df_matrix, use_container_width=True)
    st.markdown("---")

    matriks_kriteria = df_matrix.values.tolist()
    matriks_alternatif = []
    
    st.markdown("### Matriks Perbandingan Alternatif")
    for k in range(st.session_state.n_kriteria):
        with st.expander(f"*Kriteria {st.session_state.kriteria[k]}*", expanded=False):
            df_alt = pd.DataFrame(
                [[1.0 if i == j else 1.0 for j in range(st.session_state.n_alternatif)] for i in range(st.session_state.n_alternatif)],
                columns=st.session_state.alternatif, 
                index=st.session_state.alternatif
            )
            for i in range(st.session_state.n_alternatif):
                for j in range(i+1, st.session_state.n_alternatif):
                    df_alt.iloc[i, j] = st.number_input(
                        f"{st.session_state.alternatif[i]} dibanding {st.session_state.alternatif[j]} (Kriteria {st.session_state.kriteria[k]})",
                        min_value=0.1, max_value=9.0, value=1.0, key=f"a{k}{i}{j}"
                    )
                    df_alt.iloc[j, i] = round(1 / df_alt.iloc[i, j], 4)
            st.dataframe(df_alt, use_container_width=True)
            matriks_alternatif.append(df_alt.values.tolist())

    if st.button("Hitung", type="primary"):
        hasil = hitung_ahp(st.session_state.kriteria, matriks_kriteria, st.session_state.alternatif, matriks_alternatif)

        st.subheader("Bobot Kriteria")
        st.dataframe(pd.DataFrame({"Kriteria": st.session_state.kriteria, "Bobot": hasil["bobot_kriteria"]}), use_container_width=True)
        cr_krit = hasil['cr_kriteria']
        status_krit = "Konsisten" if cr_krit <= 0.1 else "Tidak Konsisten"
        st.markdown(f"*CR Kriteria = {cr_krit:.3f}* ({':green['+status_krit+']' if cr_krit <= 0.1 else ':red['+status_krit+']'})")

        for i, k in enumerate(st.session_state.kriteria):
            st.write(f"### Bobot Lokal Alternatif untuk {k}")
            st.dataframe(pd.DataFrame({"Alternatif": st.session_state.alternatif, "Bobot": hasil["bobot_alternatif_lokal"][i]}))
            cr_alt = hasil['cr_alternatif'][i]
            status_alt = "Konsisten" if cr_alt <= 0.1 else "Tidak Konsisten"
            st.markdown(f"*CR = {cr_alt:.3f}* ({':green['+status_alt+']' if cr_alt <= 0.1 else ':red['+status_alt+']'})")

        st.subheader("Hasil Perhitungan dan Ranking")
        styled_df_ahp = hasil["hasil_df"].style.apply(highlight_rank1, axis=1)
        st.markdown(styled_df_ahp.to_html(), unsafe_allow_html=True)