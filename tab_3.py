"""
IMPORTS NÉCESSAIRES À CE MODULE :
"""

# Pour la récupération d'entrées utilisateur sur streamlit + l'affichage (titres, pages déroulantes, figures, texte) :
import streamlit as st

# Module contenant les fonctions appelées pour la préparation du jeu de données avant entraînement du modèle
import preparation_modele as prep


"""
FONCTION "ETAPES_PREPARATION_MODELE" :
    > fonction unique de ce module
    > entrée : dataframe "donnees"
    > sorties : la serie "target" + le dataframe "features" (entrées du modèle)
"""

def etapes_preparation_modele(donnees):    

    """
    1. ENCODAGE DES DONNÉES
    """
    st.subheader('**Encodage des données :**')
    with st.expander('**Encodage des données :**'):
    # à compléter
        pass


    #------------------------------------------------------------------------

    """
    2. STANDARDISATION DES DONNÉES
    """
    st.subheader('**Standardisation des données :**')
    with st.expander('**Standardisation des données :**'):
    # à compléter
        pass


    #------------------------------------------------------------------------

    """
    3. VISUALISATION DES CORRELATIONS
    """

    st.subheader('**Target :**')
    with st.expander('**Carte des corrélations du jeu de données :**', expanded=False):

        # Affichage de la heatmap de correlations :
        st.write('Corrélations entre les variables :')
        fig_corr = prep.map_corr(donnees)
        st.pyplot(fig_corr, clear_figure=True)

    with st.expander('**Sélection de la target:**', expanded=False):
        # Sélection de la target :
        nom_par_defaut="target"
        target = st.text_input("Entrez une chaîne de caractères", nom_par_defaut)
        target = prep.target_select(donnees,target)
        st.write("Votre choix : ",target.name)

        # Target correlations :
        st.write('Corrélations entre la target et les autres variables :')
        target_corr = prep.calc_target_correlations(donnees,target)
        fig_target_corr = prep.fig_target_correlations(target_corr)
        st.pyplot(fig_target_corr, clear_figure=True, use_container_width=False)

    with st.expander('**Détection du type de target:**', expanded=False):
        # à compléter
        pass



    #------------------------------------------------------------------------

    """
    4. SÉLECTION DES FEATURES
    """

    st.subheader('**Sélection des features pour le modèle :**')

    # Sélection des colonnes
    col_selectionnees = prep.select_colonnes(donnees)
    
    with st.expander('**Visualisation des corrélations entre variables :**', expanded=False):
        # Pair plot :
        st.write("Pair plot des variables : vérification qu'il n'y a pas de colinéarités")
        fig_pairplot = prep.pairplot(donnees, col_selectionnees)
        st.pyplot(fig_pairplot)   

    #with st.expander('**Mode de sélection**', expanded=True):

    mode_selection_features = st.radio("Sélectionnez : ", \
                                        ("Toutes les colonnes (par défaut)", "Sélection manuelle", "Sélection automatique")
                                        )
    st.write("Vous avez choisi : "+mode_selection_features)

    if mode_selection_features == "Sélection manuelle":
        features = prep.features_manual_select(donnees,col_selectionnees)

    elif mode_selection_features == "Sélection automatique":
        corr_seuil_defaut = "0.5"
        st.write('Entrez un seuil de coefficient de correlation : \n - valeur absolue comprise entre 0 et 1 \n - séparateur décimal : "."')
        corr_seuil = float(st.text_input("seuil : ", corr_seuil_defaut))        
        features = prep.features_auto_select(donnees,corr_seuil,target)

        # si aucune colonne ne vérifie la condition : on fait la sélection par défaut (i.e. toutes les colonnes)
        if features.empty == True:
            st.write("Aucune variable sélectionnée ! --> Sélection par défaut (toutes les variables)")
            features = prep.features_select_all(donnees,target)

    else:
        features = prep.features_select_all(donnees,target)
    
    # Affichage des variables sélectionnées :
    st.write("Variables sélectionnées pour l'entraînement du modèle (features) : ")
    for feature in features:
        st.write("-",feature)


    #------------------------------------------------------------------------

    """
    5. RÉÉQUILIBRAGE DES DONNÉES
    """

    st.subheader('**Rééquilibrage des données :**')
    with st.expander('**Rééquilibrage :**'):
    # à compléter
        pass

    
    #------------------------------------------------------------------------

    """
    6. AFFICHAGE FIN DE PAGE : TARGET ET FEATURES ENTRÉES DU MODÈLE
    """
    st.subheader('**Récapitulatif des données sélectionnées pour le modèle**')

    st.write("Variable d'intérêt (target) : ",target.name)
    st.write("Variables sélectionnées pour l'entraînement du modèle (features) :",', '.join(features.columns))


    # sorties de fonction tab_3 (qui sont les arguemnts d'entrée de la fonction tab_4)
    return features, target