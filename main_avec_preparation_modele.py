import streamlit as st
import pandas as pd
import correlation
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
    st.write("Affichage des 5 premières lignes de la base de données " + selected_database + " :")
    st.write(donnees.head())    
    
    

#### Page de l'onglet 3
with tabs_3:
    # st.subheader('Préparation au modèle')
    st.subheader('Correlations')

    # Affichage de la heatmap de correlations :
    st.write('Heatmap des corrélations :')
    fig_corr = prep.map_corr(donnees)
    st.pyplot(fig_corr)

    # Target correlations :
    target = "target"
    fig_target_corr = prep.target_correlations(donnees,target)
    st.pyplot(fig_target_corr)

    # Pair plot
    # Sélection des colonnes
    st.write('Nuage de points de deux colonnes :')
    nb_col = st.number_input("Entrez le nombre de colonnes", min_value=1, step=1)
    list_col = prep.select_colonnes(donnees,nb_col)
    # list_col = ["age","sex","bmi"]
    fig_pairplot = prep.pairplot(donnees, list_col)
    st.pyplot(fig_pairplot)


#### Page de l'onglet 4
with tabs_4:
    st.subheader('Modèle')
    st.write('Remplacer par votre code')

#### Page de l'onglet 5
with tabs_5:
    st.subheader('Prédictions')
    st.write('Remplacer par votre code')







