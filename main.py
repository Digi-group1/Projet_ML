# Import des librairies
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Import des fichiers python 
from data_management import chargement_data

# Import des fichiers Python qui affichent les onglets
import tab_1
import tab_2
import tab_3
import tab_4



#### STREAMLIT ####
# Titre de l'application
st.title('Bienvenue sur votre application de Machine Learning')

# Menu sur la gauche avec les différents paramètres à choisir
st.sidebar.title("Paramètres de l'application")

#### Choix de la base de données
selected_database = st.sidebar.radio("Sélectionnez une base de données", ("Diabète", "Vins","Charger un fichier CSV"))
donnees,base = chargement_data.charger(selected_database)
st.sidebar.write("Vous avez choisi la base "+base)


# Pages du milieu qui changent en fonction de l'onglet sélectionné

#### Initialisation des onglets 
tabs_1, tabs_2, tabs_3, tabs_4, tabs_5 = st.tabs(['Statistiques descriptives', 'Nettoyage des données', 'Préparation au modèle', 'Modèle','Prédictions'])

# Afin de bien repartir d'une base propre sur chacun des onglets, on éxecute dans le code d'abord tous les changements réalisés à l'onglet 2

#### Page de l'onglet 2 -- Nettoyage des données
with tabs_2:
    donnees = tab_2.nettoyage_donnees(base,donnees)

    
#### Page de l'onglet 1 -- Statistiques descriptives
with tabs_1:
    tab_1.statistiques_desc(base,donnees)         


#### Page de l'onglet 3 -- Prépartion au modèle
with tabs_3:
    features, target, type_model = tab_3.etapes_preparation_modele(donnees)


#### Page de l'onglet 4 -- Modèle
with tabs_4:
    R2, MSE = tab_4.etapes_regression(features,target,type_model)


#### Page de l'onglet 5 -- Prédictions
with tabs_5:
    st.subheader('Prédictions')
    st.write('Remplacer par votre code')




