import streamlit as st
import pandas as pd
import correlation

# Fonction pour charger les données
def charger_donnees(nom_base):
    if nom_base == 'base_diabete':
        return pd.read_csv(r'data\diabete.csv', sep=",")
    elif nom_base == 'base_vins':
        return pd.read_csv(r'data\vin.csv', sep=",")

# Fonction pour nettoyer et standardiser les données (simulée ici)
def nettoyer_standardiser_donnees():
    message = 'Les données ont été nettoyées'
    return message

# Fonction pour fractionner les données en ensembles d'entraînement et de test
def fractionner_donnees():
    message = 'Les données ont été splitées'
    return message
    
# Fonction pour créer et entraîner le modèle (simulée ici)
def entrainer_modele():
    message = 'Le modèle est créé et entrainé'
    return message
    
# Fonction pour évaluer le modèle sur l'ensemble de test (simulée ici)
def evaluer_modele():
    message = "Voici les résultats du modèle pour l'évaluer"
    return message


donnees = charger_donnees('base_diabete')



#### STREAMLIT ####
# Titre de l'application
st.title('Bienvenue sur votre application de Machine Learning')

# Menu sur la gauche avec les différentes étapes
st.sidebar.title('Étapes du Machine Learning')
etapes = ['Chargement des données', 'Data Management', 'Split des données', 'Modèle', 'Résultats']
choix_etape = st.sidebar.selectbox('Sélectionner une étape :', etapes)

# Choix de l'étape 
if choix_etape == 'Chargement des données' :
    st.subheader('Chargement des données')
    choix_base = st.radio('Choisir une base de données :', ('base_diabete', 'base_vins'))
    donnees = charger_donnees(choix_base)
    st.write('Aperçu des données :')
    st.write(donnees.head())


elif choix_etape == 'Data Management':
    st.subheader('Data Management')
    st.write(nettoyer_standardiser_donnees())
    fig = correlation.map_corr(donnees)
    st.pyplot(fig)


elif choix_etape == 'Split des données':
    st.subheader('Split des données')
    st.write(fractionner_donnees())

elif choix_etape == 'Modèle':
    st.subheader('Modèle')
    st.write(entrainer_modele())


elif choix_etape == 'Résultats':
    st.subheader('Résultats')
    st.write(evaluer_modele())




