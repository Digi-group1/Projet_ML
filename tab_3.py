"""
IMPORTS NÉCESSAIRES À CE MODULE :
"""

# Pour la récupération d'entrées utilisateur sur streamlit + l'affichage (titres, pages déroulantes, figures, texte) :
import streamlit as st

# Module contenant les fonctions appelées pour la préparation du jeu de données avant entraînement du modèle
import preparation_modele as prep
import standardisation



"""
FONCTION "ETAPES_PREPARATION_MODELE" :
    > fonction unique de ce module
    > entrée : dataframe "donnees"
    > sorties : la serie "target" + le dataframe "features" (entrées du modèle)
"""


def etapes_preparation_modele(donnees):    

    """
    1. DÉTECTION DE LA TARGET ET DE SON TYPE
    """

    st.subheader('**Détection de la target :**')
    with st.expander('**Sélection de la target:**', expanded=False):
        # Sélection de la target :
        target_name = prep.detect_target(donnees)
        st.write("Votre choix : ",target_name)

        type_target,type_model = prep.type_target(donnees[target_name])
        st.write(type_model)
        

    """
   2. ENCODAGE DES DONNÉES
    """

    st.subheader('**Encodage des données :**')

    with st.expander('**Encodage de la target :**'):

        # Sélection des colonnes (Sélection de la dernière colonne par défaut) :
        # selection_par_defaut = donnees.columns[-1]
        # col_encod_select = prep.select_colonnes(donnees,selection_par_defaut, key="1")

        # for col in col_encod_select:
        #     new_col_name =  "new_" + col
        #     col_encod, new_col_res = prep.encodage(donnees,col, new_col_name)
        #     st.write(new_col_res)

        if type_target == "texte":
            nom_target_encod = "target_encod"
            target, target_encod_res = prep.encodage(donnees,target_name, "target_encod")
            st.write(target_encod_res)
        else:
            target = donnees[target_name]
            st.write("Pas d'encodage nécessaire")

        st.write(target.head())

    #------------------------------------------------------------------------

    """
    3. STANDARDISATION DES DONNÉES
    """
    st.subheader('**Standardisation des données :**')
    with st.expander('**Standardisation des données :**'):
    # On vérifie si le modèle est standardisé ou non
        colonnes_sans_target = [colonne for colonne in donnees.columns if colonne != target_name]
        df_sans_target = donnees[colonnes_sans_target]
        if standardisation.est_standardise(df_sans_target) == False :
            st.write("Votre base de données n'est pas standardisée")
            choix_standardisation = st.radio("Souhaitez-vous standardiser votre base de données ?", ("Oui", "Non"))
            if choix_standardisation == "Non" :
                donnees = donnees
                st.write("Vous conservez votre base de données, dont voici les premières lignes : ")
                st.write(donnees.head())
            elif choix_standardisation == "Oui" :
                donnees = standardisation.standardiser_dataframe(donnees)
                st.write("Voici les premières lignes de votre base de données standardisée :")
                st.write(donnees.head())
        else : 
            st.write("Votre base de données est standardisée (Toutes les moyennes sont proches de zéro)") 
        


    #------------------------------------------------------------------------

    """
    4. VISUALISATION DES CORRELATIONS
    """

    st.subheader('**Target :**')

    col_num = donnees.select_dtypes(include=["int","float"]).columns.tolist()

    with st.expander('**Carte des corrélations du jeu de données :**', expanded=False):

        # Affichage de la heatmap de correlations :
        st.write('Corrélations entre les variables :')
        fig_corr = prep.map_corr(donnees[col_num])
        # fig_corr = prep.map_corr(donnees)
        st.pyplot(fig_corr, clear_figure=True)

    with st.expander('*Correlations avec la target:**', expanded=False):

        # Target correlations :
        st.write('Corrélations entre la target et les autres variables :')
        target_corr = prep.calc_target_correlations(donnees[col_num],target)
        fig_target_corr = prep.fig_target_correlations(target_corr)
        st.pyplot(fig_target_corr, clear_figure=True, use_container_width=False)


    #------------------------------------------------------------------------

    """
    5. SÉLECTION DES FEATURES
    """

    st.subheader('**Sélection des features pour le modèle :**')

    # Sélection des colonnes (Sélection des 2 premières colonnes par défaut) :
    selection_par_defaut = donnees[col_num].columns[:2].tolist()
    col_selectionnees = prep.select_colonnes(donnees[col_num],selection_par_defaut)
    
    with st.expander('**Visualisation des corrélations entre variables :**', expanded=False):
        # Pair plot :
        st.write("Pair plot des variables : vérification qu'il n'y a pas de colinéarités")
        fig_pairplot = prep.pairplot(donnees[col_num], col_selectionnees)
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
    6. RÉÉQUILIBRAGE DES DONNÉES
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
    return features, target, type_model