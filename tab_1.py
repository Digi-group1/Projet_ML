#########################
##### PARTIE IMPORT #####
#########################

#########################
# IMPORT DES LIBRAIRIES #
#########################

import streamlit as st
import matplotlib.pyplot as plt



############################################
##### PARTIE STATISTIQUES DESCRIPTIVES #####
############################################

def statistiques_desc(selected_database,donnees) :

    st.subheader('Statistiques descriptives')
    # On affiche notre BDD sous forme de tableau
    with st.expander('Affichage de la base de données ' + selected_database) :
       st.dataframe(donnees)    
    # On affiche quelques stats descriptives générales de notre BDD    
    with st.expander('Résumé des données') :
        resume = donnees.describe()
        st.write(resume)
    # On affiche des graphiques pour les valeurs numériques 
    with st.expander('Distribution des valeurs numériques') :
        colonnes_numeriques = donnees.select_dtypes(include=['int', 'float']).columns.tolist()
        if len(colonnes_numeriques) == 0 :
            st.write('Votre jeu de données ne comporte pas de variables numériques')
        else :
            colonne_selectionnee = st.selectbox("Sélectionnez une colonne numérique", colonnes_numeriques)
            data = donnees[colonne_selectionnee]
            # Afficher les histogrammes
            st.write("Voici l'histogramme, la boîte à moustache et le KDE plot de votre colonne " + colonne_selectionnee)
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
            st.markdown("- **Histogramme** : *diagramme représentant la répartition des valeurs d'une variable sous forme de barres, chaque barre représentant une plage de valeurs et sa hauteur étant proportionnelle à la fréquence ou à la densité de ces valeurs.*")
            st.markdown("- **Boîte à moustaches** : *graphique statistique représentant la distribution des données en affichant la médiane, les quartiles et les valeurs extrêmes, permettant ainsi de visualiser la dispersion et les valeurs aberrantes des données.*")
            st.markdown("- **KDE plot** (Kernel Density Estimation) : *méthode de visualisation statistique estimant la densité de probabilité d'une variable continue en lissant les données et en créant une courbe continue représentant la distribution des données.*")
    
    # Fréquence des valeurs catégorielles
    with st.expander('Fréquence des valeurs catégorielles') :
        colonnes_categorielles = donnees.select_dtypes(include=['object', 'category']).columns.tolist()
        if len(colonnes_categorielles) == 0 :
            st.write('Votre jeu de données ne comporte pas de variables catégorielles')
        else : 
            colonne_selec_cat = st.selectbox("Sélectionnez une colonne catégorielle", colonnes_categorielles)
            data = donnees[colonne_selec_cat]
            valeurs_frequences = data.value_counts()
            st.write("Voici l'histogramme et le diagramme circulaire de votre colonne " + colonne_selec_cat)
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            data.hist(ax=ax1)
            ax1.set_title('Histogramme')
            ax2.pie(valeurs_frequences, labels=valeurs_frequences.index, autopct='%1.1f%%')
            ax2.set_title('Diagramme circulaire')
            st.pyplot(fig)
            
            st.markdown("- **Histogramme** : *diagramme représentant la répartition des valeurs d'une variable sous forme de barres, chaque barre représentant une plage de valeurs et sa hauteur étant proportionnelle à la fréquence ou à la densité de ces valeurs.*")
            st.markdown("- **Diagramme circulaire** : *graphique statistique représentant les données sous forme de secteurs circulaires, chacun proportionnel à la fréquence ou à la proportion de la catégorie qu'il représente.*")