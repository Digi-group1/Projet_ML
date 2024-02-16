import streamlit as st
import pandas as pd
import preparation_modele as prep
# from data_management import chargement_data
# from data_management import nettoyage

# donnees = chargement_data.charger('base_diabete')
donnees = pd.read_csv(r'data/diabete.csv', header=0)


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


with tabs_2:
    st.subheader('Nettoyage des données')
    st.write('Remplacer par votre code')

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



with tabs_4:
    st.subheader('Modèle')
    st.write('Remplacer par votre code')
    
with tabs_5:
    st.subheader('Prédictions')
    st.write('Remplacer par votre code')




