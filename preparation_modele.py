"""
IMPORTS NÉCESSAIRES À CE MODULE :
"""

# Pour les correlations
import numpy as np
import pandas as pd

# Pour les figures
import seaborn as sns
import matplotlib.pyplot as plt

# Pour intéragir avec streamlit
import streamlit as st


"""
a. FONCTIONS POUR LA SELECTION DE COLONNES D'UN DATAFRAME
"""

def select_colonnes(df, key='default'): # dataframe et nombre de colonnes que l'on veut sélectionner
    
    liste_colonnes = df.columns.tolist()

    # Sélection des 2 premières colonnes par défaut :
    selection_par_defaut = df.columns[:2].tolist()

    # Afficher le multiselect à l'utilisateur
    colonnes_selectionnees = st.multiselect('Sélectionnez deux colonnes ou plus :', liste_colonnes, default=selection_par_defaut, key=key)

    # Afficher les options sélectionnées
    st.write('Options sélectionnées :', colonnes_selectionnees)

    # st.write('Options sélectionnées :', st.multiselect('Sélectionnez deux colonnes ou plus :', liste_colonnes))
    
    return colonnes_selectionnees



"""
b. FONCTIONS DE CORRELATIONS (CALCUL ET AFFICHAGE)
"""

# HEATMAP CORRELATIONS : retourne la heatmap avec l'ensemble des corrélations
def map_corr(df):
    # ajouter un filtre colonnes numériques
    mask = np.triu(df.corr())
    fig, ax = plt.subplots(figsize=(8, 8))
    cmap = sns.diverging_palette(15, 160, n=11, s=100)
    sns.heatmap(df.corr(),
                mask=mask,
                annot=True,
                cmap=cmap,
                center=0,
                vmin=-1,
                vmax=1,
                ax=ax)

    return fig


# PAIRPLOT : VISUALISATION DES ÉVENTUELLES COLINÉARITÉS ENTRE FEATURES
def pairplot(df, list_col):
    fig = sns.pairplot(df[list_col])
    return fig


# CORRELATIONS AVEC LA TARGET

# calcul des corrélations avec la target (retourne une serie, entrée de la fonction suivante) :
def calc_target_correlations(df,target):

    target_corr_dict = dict()
    for column in df:
        correlation = target.corr(df[column])
        target_corr_dict[column] = correlation

    target_corr_df = pd.DataFrame({'Correlation': list(target_corr_dict.values())}, index=target_corr_dict.keys())
    target_corr_df = target_corr_df.sort_values(by='Correlation', ascending=False)

    return target_corr_df

# création de la figure (heatmap) :
def fig_target_correlations(target_corr_df):
    
    fig, ax = plt.subplots(figsize=(1,3))

    cmap = sns.diverging_palette(15, 160, n=11, s=100)

    plt.figure()
    sns.heatmap(target_corr_df,
                annot=True,
                annot_kws={"size": 7},
                cmap=cmap,
                center=0,
                vmin=-1,
                vmax=1,
                ax=ax,
                cbar=False)
    plt.yticks(fontsize=3)

    return fig


"""
c. TARGET :     /!\ À COMPLÉTER /!\ 
"""

# Sélection de la target
def target_select(df,TARGET):
    y = df[TARGET]
    return y

# Détection du type de target (--> type de ML)
    # ...


"""
d. FEATURES
"""

# Sélection de toutes les colonnes (sauf la target)
def features_select_all(df,target):   # où target est une serie
    FEATURES = [col for col in df.columns if col!=target.name]
    X = df[FEATURES]
    return X

# Sélection manuelle, à partir d'une liste de noms de colonnes    
def features_manual_select(df, list_col):
    FEATURES = list_col #liste des colonnes sélectionnées du type : [col1,col2,col3]
    X = df[FEATURES]
    return X

# Sélection des colonnes (sauf la target) dont la corrélation avec la target est au-dessus d'un seuil
def features_auto_select(df, corr_seuil, target):   # où corr_seuil est un seuil de coeff de corrélation avec la target
    FEATURES = [col for col in df.columns if (abs(df[col].corr(target)) >= float(corr_seuil) and col!=target.name)]
    X = df[FEATURES]
    return X
