import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from data_management import chargement_data
from data_management import nettoyage



#### STREAMLIT ####
# Titre de l'application
st.title('Bienvenue sur votre application de Machine Learning')


# Menu sur la gauche avec les différents paramètres à choisir
st.sidebar.title("Paramètres de l'application")

#### Choix de la base de données
selected_database = st.sidebar.radio("Sélectionnez une base de données", ("Diabète", "Vins"))
st.sidebar.write("Vous avez choisi la base "+selected_database)
donnees = chargement_data.charger(selected_database)


# Pages du milieu qui changent en fonction de l'onglet sélectionné

#### Initialisation des onglets 
tabs_1, tabs_2, tabs_3, tabs_4, tabs_5 = st.tabs(['Statistiques descriptives', 'Nettoyage des données', 'Préparation au modèle', 'Modèle','Prédictions'])

# Afin de bien repartir d'une base propre sur chacun des onglets, on éxecute dans le code d'abord tous les changements réalisés à l'onglet 2
# Nettoyage des données

#### Page de l'onglet 2
with tabs_2:
    st.subheader('Nettoyage des données')
    
    ### Etape 1 - Champs sans nom : 
    with st.expander('Etape 1 : Vérification du nom des champs :') :
        colonnes_nom = nettoyage.colonnes_unnamed(donnees)
        message_nom = nettoyage.affichage_unnamed(colonnes_nom)
    
        if len(colonnes_nom) == 0 :
            st.write('Vos colonnes comportent toutes des noms de variables !')
        else:
            st.write(message_nom)
            st.write("Affichage des 5 premières lignes de la base de données " + selected_database + " :")
            st.write(donnees[colonnes_nom].head())
            
            st.write('Souhaitez-vous ?')
            supprimer_colonne = st.checkbox("Supprimer la(les) colonne(s) sans nom ?")
            renommer_colonne = st.checkbox("Renommer la(les) colonne(s) sans nom ?")
            
            if supprimer_colonne :
                donnees = nettoyage.supp_colonnes(donnees,colonnes_nom)
                st.write("Vous venez de supprimer la(les) colonne(s). Voici votre nouvelle base de données : ")
                st.write(donnees.head())
            if renommer_colonne : 
                for i in range(len(colonnes_nom)) :
                    colonne = colonnes_nom[i]
                    nouveau_nom = st.text_input("Entrez le nouveau nom pour la colonne "+colonne, "")
                    donnees = nettoyage.renommer_colonnes(donnees,colonne,nouveau_nom)
                    st.write("Vous venez de renommer la colonne "+ colonne + "par :" + nouveau_nom + ". Voici votre nouvelle base de données :")
                    st.write(donnees.head())
    
    
    ### Etape 2 - Identification des valeurs manquantes : 
    with st.expander('Etape 2 : Identification et traitement des valeurs manquantes :') :
        message_valeurs = nettoyage.identification_nan(donnees)
        st.write(message_valeurs)

    
#### Page de l'onglet 1
with tabs_1:
    
    st.subheader('Statistiques descriptives')
    with st.expander('Affichage de la base de données ' + selected_database) :
       st.dataframe(donnees)    
        
    with st.expander('Résumé des données') :
        resume = donnees.describe()
        st.write(resume)
    
    with st.expander('Distribution des valeurs numériques') :
        colonnes_numeriques = donnees.select_dtypes(include=['int', 'float']).columns.tolist()
        if len(colonnes_numeriques) == 0 :
            st.write('Votre jeu de données ne comporte pas de variables numériques')
        else :
            colonne_selectionnee = st.selectbox("Sélectionnez une colonne numérique", colonnes_numeriques)
            data = donnees[colonne_selectionnee]
            # Afficher les histogrammes
            st.write("Histogramme")
            # Créer une figure
            fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 6))
            # Afficher l'histogramme dans la figure
            data.hist(ax=ax1)
            ax1.set_title('Histogramme')
            data.plot(kind='box', ax=ax2)
            ax2.set_title('Boîte à moustaches')
            data.plot(kind='kde', ax=ax3)
            ax3.set_title('KDE plot')
            # Afficher le graphique dans Streamlit
            st.pyplot(fig)
    
    # Fréquence des valeurs catégorielles
    with st.expander('Fréquence des valeurs catégorielles') :
        colonnes_categorielles = donnees.select_dtypes(include=['object', 'category']).columns.tolist()
        if len(colonnes_categorielles) == 0 :
            st.write('Votre jeu de données ne comporte pas de variables catégorielles')
        else : 
            colonne_selec_cat = st.selectbox("Sélectionnez une colonne catégorielle", colonnes_categorielles)
            data = donnees[colonne_selec_cat]
            valeurs_frequences = data.value_counts()

            st.write('Graphique à barres de la fréquence')
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            data.hist(ax=ax1)
            ax1.set_title('Histogramme')
            ax2.pie(valeurs_frequences, labels=valeurs_frequences.index, autopct='%1.1f%%')
            ax2.set_title('Diagramme circulaire')
            st.pyplot(fig)
            

    



        
    

#### Page de l'onglet 3
with tabs_3:
    st.subheader('Préparation au modèle')
    st.write('Remplacer par votre code')


#### Page de l'onglet 4
with tabs_4:
    st.subheader('Modèle')
    st.write('Remplacer par votre code')

#### Page de l'onglet 5
with tabs_5:
    st.subheader('Prédictions')
    st.write('Remplacer par votre code')




