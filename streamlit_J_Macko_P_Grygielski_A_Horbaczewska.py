import subprocess
import sys

# Funkcja do sprawdzenia i zainstalowania brakujących pakietów
def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError:
        print(f"Błąd przy instalacji pakietu: {package}")

# Lista wymaganych pakietów
required_packages = ["streamlit", "pandas", "numpy", "matplotlib", "seaborn"]

# Sprawdzanie i instalowanie brakujących pakietów
for package in required_packages:
    install_package(package)

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
from itertools import combinations

# Funkcje pomocnicze
def chisq_stat(tabela):
    suma = tabela.values.sum()
    macierz = np.zeros(shape=[tabela.shape[0], tabela.shape[1]])
    for x in range(0, tabela.shape[0]):
        for y in range(0, tabela.shape[1]):
            macierz[x, y] = (sum(tabela.iloc[x, :]) * sum(tabela.iloc[:, y])) / suma
    Chis_stat = 0
    for x in range(0, macierz.shape[0]):
        for y in range(0, macierz.shape[1]):
            Chis_stat += ((tabela.iloc[x, y] - macierz[x, y]) ** 2) / macierz[x, y]
    return macierz, Chis_stat.round(3)

def dystrybuant(stat_test, df):
    s = df / 2
    if s < 1:
        s = 1
    lower_gamma = 0
    for n in range(110):
        term = ((stat_test / 2) ** (s + n)) * math.exp(-stat_test / 2) / math.factorial(n) / (s + n)
        lower_gamma += term
    return lower_gamma / math.gamma(s)

def odds_ratio(a, b, c, d):
    return (a * d) / (b * c)

def OR(tabela):
    kolumny = list(tabela.columns)
    rakowe = list(tabela.iloc[0])
    zdrowe = list(tabela.iloc[1])
    lista = []
    for (i, j) in combinations(range(len(kolumny)), 2):
        a, b = rakowe[i], rakowe[j]
        c, d = zdrowe[i], zdrowe[j]
        odd_rat = odds_ratio(a, b, c, d)
        lista.append([kolumny[i], kolumny[j], odd_rat])
    return lista

# Funkcja do obliczenia oczekiwanych genotypów
def expect_gen(p_sqr, p_q_sqr, q_sqr, suma_gen):
    expect_gen1 = p_sqr * suma_gen  # AA
    expect_het = p_q_sqr * suma_gen  # AG
    expect_gen2 = q_sqr * suma_gen  # GG
    return expect_gen1, expect_het, expect_gen2

# Funkcja do analizy Hardy'ego-Weinberga
def HWE_control(genotypy, allele, grupa):
    suma_gen = sum(genotypy.loc[grupa, :])
    genotypy = genotypy.replace({'GA': 'AG', 'AG': 'AG', 'CT': 'CT', 'TC': 'CT'})  # Zamiana TC na CT i GA/AG na AG
    genotypy_values = genotypy.loc[grupa, :].values
    if len(genotypy_values) != 3:
        raise ValueError(f"Błąd: Oczekiwano 3 wartości, ale znaleziono {len(genotypy_values)} dla grupy {grupa}")
    gen1, het, gen2 = genotypy_values / suma_gen
    p, q = allele.loc[grupa, :] / sum(allele.loc[grupa, :])
    p_square = p ** 2
    q_square = q ** 2
    p_q_square = 2 * p * q
    expect_gen1, expect_het, expect_gen2 = expect_gen(p_square, p_q_square, q_square, suma_gen)
    gen1_obs = gen1 * suma_gen
    het_obs = het * suma_gen
    gen2_obs = gen2 * suma_gen
    
    tabela = pd.DataFrame(
        {"Obserwowane": [gen1_obs, het_obs, gen2_obs], "Oczekiwane": [expect_gen1, expect_het, expect_gen2]},
        index=["AA", "AG", "GG"],
    )
    return tabela.T

def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("https://i.imgur.com/DBGp1Yv.png");
             background-size: cover;
             background-position: top right 18vw;
             background-repeat: no-repeat
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

set_bg_hack_url()

# Aplikacja Streamlit
st.title("Analiza genów VDR (FokI i BSMI)")
st.write("Wgraj plik CSV z danymi.")

# Wczytanie pliku
uploaded_file = st.file_uploader("Wybierz plik CSV", type=["csv"])
if uploaded_file is not None:
    dane = pd.read_csv(uploaded_file, sep=";")
    dane.rename(columns={"VDR FokI": "VDR_FokI", "BSM": "VDR_BSMI"}, inplace=True)

    # Zastąpienie TC na CT i GA na AG w danych
    dane["VDR_FokI"] = dane["VDR_FokI"].replace({'TC': 'CT', 'GA': 'AG', 'AG': 'AG', 'CT': 'CT'})
    dane["VDR_BSMI"] = dane["VDR_BSMI"].replace({'TC': 'CT', 'GA': 'AG', 'AG': 'AG', 'CT': 'CT'})

    # Wybór genotypu do analizy
    gen = st.selectbox("Wybierz gen do analizy:", ["VDR_FokI", "VDR_BSMI"])

    # Filtracja danych
    dane_gen = dane[["Grupa", gen]].dropna(subset=[gen])

    st.write(f"Dane po usunięciu pustych wierszy dla genotypu {gen}:")
    st.write(dane_gen)

    # Rozkład genotypów
    st.header(f"Rozkład genotypów dla {gen}")
    tabela = pd.crosstab(dane_gen["Grupa"], dane_gen[gen])
    st.write(tabela)

    # Wykres rozkładu genotypów
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.countplot(data=dane_gen, x=gen, hue="Grupa", ax=ax)
    ax.set_title(f"Rozkład genotypów dla {gen}")
    st.pyplot(fig)

    # Obliczenie statystyki chi-kwadrat
    macierz, Chis_stat = chisq_stat(tabela)
    df = (tabela.shape[0] - 1) * (tabela.shape[1] - 1)
    p_value = 1 - dystrybuant(Chis_stat, df)

    st.subheader("Test chi-kwadrat:")
    st.write(f"Statystyka chi-kwadrat: {Chis_stat}")
    st.write(f"Liczba stopni swobody: {df}")
    st.write(f"Wartość p: {p_value}")

    # Analiza częstości alleli
    st.header("Analiza częstości alleli")
    allele_table = pd.DataFrame(index=tabela.index)

    for kolumna in tabela.columns:
        allel1, allel2 = kolumna[0], kolumna[1]
        if allel1 not in allele_table.columns:
            allele_table[allel1] = tabela[kolumna]
        else:
            allele_table[allel1] += tabela[kolumna]

        if allel2 not in allele_table.columns:
            allele_table[allel2] = tabela[kolumna]
        else:
            allele_table[allel2] += tabela[kolumna]

    st.write("Tabela częstości alleli:")
    st.write(allele_table)

    # Wykres analizy częstości alleli
    fig, ax = plt.subplots(figsize=(8, 6))
    allele_table.plot(kind="bar", stacked=True, ax=ax)
    ax.set_title(f"Częstości alleli dla {gen}")
    ax.set_ylabel("Liczba osób")
    st.pyplot(fig)

    # Test Hardy'ego-Weinberga
    st.header("Test Hardy'ego-Weinberga")
    HWE_results = HWE_control(tabela, allele_table, "Control")
    st.write(HWE_results)
    macierz, Chi_square_HWE = chisq_stat(HWE_results.T)
    df_HWE = HWE_results.shape[1] - 1 - 1
    p_value_HWE = 1 - dystrybuant(Chi_square_HWE, df_HWE)
    st.write(f"Statystyka chi-kwadrat HWE: {Chi_square_HWE}")
    st.write(f"Liczba stopni swobody: {df_HWE}")
    st.write(f"Wartość p HWE: {p_value_HWE}")

    # Wykres testu Hardy'ego-Weinberga
    fig, ax = plt.subplots(figsize=(8, 6))
    HWE_results.T.plot(kind="bar", ax=ax, color=["blue", "red"])
    ax.set_title(f"Porównanie obserwowanych i oczekiwanych genotypów w teście HWE dla {gen}")
    ax.set_ylabel("Liczba osób")
    st.pyplot(fig)

    # Analiza Odds Ratio
    st.header("Analiza Odds Ratio")
    OR_results = OR(tabela)
    or_df = pd.DataFrame(OR_results, columns=["Genotyp 1", "Genotyp 2", "Odds Ratio"])
    st.write(or_df)
