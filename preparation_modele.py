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

def select_colonnes(df, selection_par_defaut, key='default'): # dataframe et nombre de colonnes que l'on veut sélectionner
    
    liste_colonnes = df.columns.tolist()

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

def detect_target(data):
    # nom_target = 'target' #ou = re.compile(r'\b\w*target\w*\b', re.IGNORECASE) pour généraliser -> à tester
    nom_target = 'target'

    if nom_target in data.columns:
        return nom_target

    else:
        # nom de la dernière colonne proposé par défaut à l'utilisateur
        col = data.columns[-1]
        target_defaut = data[col]
        choix_col = st.text_input("Entrez une chaîne de caractères", target_defaut.name)
        return choix_col


def type_target(target):
        # test_target = isinstance(target, (int, float))
        test_target = pd.api.types.is_numeric_dtype(target)
        if test_target == True:
            st.write("La target détectée est de type numérique.")
            type_target = "num"
            type_model = "regression"
            return type_target, type_model
        else:
            st.write("La target détectée est de type objet/texte.")
            type_model = "classification"
            type_target = "texte"
            return type_target, type_model
    


#Encodage de la target (cas d'une target non numérique)
def encodage(data, colonne: str, new_col: str): # prend le nom de la colonne à encoder et celui de la nvle colonne
    i = 0
    labels = {}
    for _, val in enumerate(data[colonne].unique()):
        labels.update({val : i})
        i +=1
        data[new_col] = data[colonne].map(labels)
    st.write("La colonne", colonne, "a bien été encodée. Voici le résultat de", new_col, ": ")
    new_col_res = data[new_col].value_counts()
    col_encod = data[new_col]
    return col_encod, new_col_res


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
