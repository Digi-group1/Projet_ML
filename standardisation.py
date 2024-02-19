import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler


# Fonction pour vérifier si un DataFrame est standardisé
def est_standardise(data):
    colonnes_numeriques = data.select_dtypes(include=['float', 'int']).columns
    # Vérifier si la moyenne de chaque variable est proche de zéro
    moyennes = data[colonnes_numeriques].mean()
    est_proche_de_zero = moyennes.abs().max() < 1e-10  # Tous les moyennes sont proches de zéro

    return est_proche_de_zero

    
## Fonction pour standardiser le modèle 
def standardiser_dataframe(data):
    # Initialiser le scaler
    scaler = StandardScaler()
    # Séparer les colonnes numériques
    colonnes_numeriques = data.select_dtypes(include=['float', 'int']).columns
    # Copier le DataFrame pour éviter de modifier l'original
    df_standardise = data.copy()
    # Standardiser les données pour chaque colonne numérique
    for colonne in colonnes_numeriques:
        df_standardise[colonne] = scaler.fit_transform(data[[colonne]])

    return df_standardise