"""
IMPORTS
"""

# Pour les correlations
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Pour le split
from sklearn.model_selection import train_test_split

# Pour intéragir avec streamlit
import streamlit as st

"""
SELECTION DE COLONNES
"""
# Fonction qui retourne une liste avec le nom des colonnes sélectionnées
# Inputs streamlit : nb de colonnes et noms des colonnes

def select_colonnes(df,nb_col): # dataframe et nombre de colonnes que l'on veut sélectionner
    list_col = list()

    # si "nb_col" est égal au nombre total de colonnes
    if nb_col == df.shape[1]:
        list_col = df.columns.tolist()

    else:
        # Création de "nb_col" champs d'input pour entrer les "nb_col" colonnes :
        for i in range(nb_col):
            col = st.text_input(f"Colonne {i+1} : ")
            list_col.append(col)

    return list_col



"""
CORRELATIONS
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


# PAIRPLOT
def pairplot(df, list_col):
    fig = sns.pairplot(df[list_col])
    return fig

def target_correlations(df,target):
    fig, ax = plt.subplots(figsize=(2, 5))
    cmap = sns.diverging_palette(15, 160, n=11, s=100)
    
    target_corr_list = df.corr()[[target]].sort_values(by=target, ascending=False)

    sns.heatmap(target_corr_list,
                annot=True,
                cmap=cmap,
                center=0,
                vmin=-1,
                vmax=1,
                ax=ax)
    return fig


"""
Target et Features
"""
def features(df):
    X = df[:-1]
    y = df[-1]
    return X, y

# ou
    
def features(df, list_col):
    FEATURES = list_col #liste des colonnes sélectionnées du type : [col1,col2,col3]
    X = df[FEATURES]
    y = df[-1]
    return X, y

# ou

def features(df, target):   # où target = string du type "target"
    X = [x for x in df.columns if x!=target]
    y = df[target]
    return X, y


"""
Split
"""
def split(X,y,pourcentage):
    X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size = pourcentage,
    random_state = 42
    )
    return X_train, X_test, y_train, y_test