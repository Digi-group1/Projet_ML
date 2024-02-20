#########################
##### PARTIE IMPORT #####
#########################

#########################
# IMPORT DES LIBRAIRIES #
#########################

import streamlit as st

##############################
# IMPORT DES FICHIERS PYTHON #
##############################

import preparation_modele as pm



#################################################
##### PARTIE ENCODAGE COLONES CATEGORIELLES ##### 
#################################################

def encodage_colonne(data,nom_target) :
    colonnes_sans_target = [colonne for colonne in data.columns if colonne != nom_target]
    df_sans_target = data[colonnes_sans_target]
    colonnes_categorielles = df_sans_target.select_dtypes(include=['object', 'category']).columns.tolist()
    nb_colonnes = len(colonnes_categorielles)
    if nb_colonnes == 0 :
        st.write("Votre jeu de données ne comporte pas de colonnes catégorielles")
    else : 
        st.write("Votre jeu de données comporte " + str(nb_colonnes) + " colonnes catégorielles") 
        choix_encodage = st.radio("Souhaitez-vous encoder certaines colonnes pour les utiliser dans un modèle ?", ("Oui", "Non"))
        if choix_encodage == "Non" :
            st.write("D'accord, votre base de données n'est pas modifiée")
        elif choix_encodage == "Oui" :
            col_selec_encod = st.multiselect("Sélectionnez une ou plusieurs colonnes à encoder", colonnes_categorielles)
            for colonne in col_selec_encod :
                nom_encod = st.text_input("Entrez un nom pour la future colonne "+colonne, " encodée")
                message, new_col_test = pm.encodage(data,colonne, nom_encod)
                st.write(message)
                st.write(new_col_test)
    return data
     
