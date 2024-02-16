import streamlit as st
import pandas as pd
import correlation
from data_management import chargement_data
# from data_management import nettoyage

donnees = chargement_data.charger('base_diabete')



#### STREAMLIT ####
# Titre de l'application
st.title('Bienvenue sur votre application de Machine Learning')

# Menu sur la gauche avec les différentes étapes
st.sidebar.title('Étapes du Machine Learning')
etapes = ['Chargement des données', 'Data Management', 'Split des données', 'Modèle', 'Résultats']
choix_etape = st.sidebar.selectbox('Sélectionner une étape :', etapes)

# Choix de l'étape 
# if choix_etape == 'Chargement des données' :
#     st.subheader('Chargement des données')
#     choix_base = st.radio('Choisir une base de données :', ('base_diabete', 'base_vins'))
#     donnees = chargement_data.charger(choix_base)
#     st.write('Aperçu des données :')
#     st.write(donnees.head())

tabs_1, tabs_2, tabs_3, tabs_4, tabs_5 = st.tabs(['Statistiques descriptives', 'Nettoyage des données', 'Préparation au modèle', 'Modèle','Prédictions'])

with tabs_1:
    st.subheader('Statistiques descriptives')
    st.write('Remplacer par votre code')
    fig = correlation.map_corr(donnees)
    st.pyplot(fig)


with tabs_2:
    st.subheader('Nettoyage des données')
    st.write('Remplacer par votre code')

with tabs_3:
    st.subheader('Préparation au modèle')
    st.write('Remplacer par votre code')


with tabs_4:
    st.subheader('Modèle')
    st.write('Remplacer par votre code')
    
with tabs_5:
    st.subheader('Prédictions')
    st.write('Remplacer par votre code')




