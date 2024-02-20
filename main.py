#########################
##### PARTIE IMPORT #####
#########################

#########################
# IMPORT DES LIBRAIRIES #
#########################

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

##############################
# IMPORT DES FICHIERS PYTHON #
##############################
 
from data_management import chargement_data
import tab_1
import tab_2
import tab_3
import tab_4



############################
##### PARTIE STREAMLIT #####
############################

##########################
# TITRE DE L'APPLICATION #
##########################
st.title('Bienvenue sur votre application de Machine Learning')

#################################################
# MENU DE GAUCHE POUR CHOISIR / CHARGER UNE BDD #
#################################################
st.sidebar.title("Paramètres de l'application")
selected_database = st.sidebar.radio("Sélectionnez une base de données", ("Diabète", "Vins","Charger un fichier CSV"))
donnees,base = chargement_data.charger(selected_database)
st.sidebar.write("Vous avez choisi la base "+base)

#######################################################################
# SECTION PRINCIPALE (QUI CHANGE EN FONCTION DE L'ONGLET SELECTIONNE) #
#######################################################################

#### Initialisation des onglets ###
tabs_1, tabs_2, tabs_3, tabs_4, tabs_5 = st.tabs(['Statistiques descriptives', 'Nettoyage des données', 'Préparation au modèle', 'Modèle','Prédictions'])

### Commentaire ###
# Afin de bien repartir d'une base propre sur chacun des onglets :
# on éxecute dans le code d'abord tous les changements réalisés à l'onglet 2

#### Page de l'onglet 2 -- Nettoyage des données ###
with tabs_2:
    donnees = tab_2.nettoyage_donnees(base,donnees)
    
#### Page de l'onglet 1 -- Statistiques descriptives ###
with tabs_1:
    tab_1.statistiques_desc(base,donnees)         

#### Page de l'onglet 3 -- Prépartion au modèle ###
with tabs_3:
    features, target, type_model = tab_3.etapes_preparation_modele(donnees)

#### Page de l'onglet 4 -- Modèle ### 
with tabs_4:
   model = tab_4.etapes_model(features,target,type_model)

#### Page de l'onglet 5 -- Prédictions ###
with tabs_5:
    st.subheader('Prédictions')
    st.write('Ce module est en cours de développement. Sa mise en application sera prévue à la prochaine mise à jour.')




