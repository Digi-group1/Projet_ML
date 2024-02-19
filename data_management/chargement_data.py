import pandas as pd 
import streamlit as st

def charger(nom_base):
    if nom_base == 'Diabète':
        df = pd.read_csv(r'data\diabete.csv', sep=",")
        base = 'Diabète'
    elif nom_base == 'Vins':
        df = pd.read_csv(r'data\vin.csv', sep=",")
        base = 'Vins'
    else:
        # Charger un fichier CSV personnalisé
        uploaded_file = st.sidebar.file_uploader("Charger un fichier CSV", type=["csv"])
        separateur_csv = st.sidebar.text_input("Quel est le délimiteur de votre fichier")
        
        if uploaded_file is not None:
            # Lire le fichier CSV chargé
            df = pd.read_csv(uploaded_file, sep = separateur_csv)
            base = st.sidebar.text_input("Nommez votre base de données", "MaBaseDeDonnees")
        else:
            # Afficher un message si aucun fichier n'a été chargé
            st.warning("Veuillez charger un fichier CSV")
    return df, base