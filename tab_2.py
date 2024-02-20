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
from data_management import nettoyage_unnamed as net_unnamed
from data_management import nettoyage_general as general
from data_management import nettoyage_nan_info as nan_info
from data_management import nettoyage_nan_traitement as nan_traitement



###################################################
##### PARTIE TRAITEMENT DE LA BASE DE DONNEES #####
###################################################

def nettoyage_donnees(selected_database,donnees) :
    
    st.subheader('Nettoyage des données')
    
    ###############################################
    ### Etape 1 - Champs sans nom ("Unnamed") : ###
    ###############################################
    with st.expander('Etape 1 : Vérification du nom des champs :') :
        colonnes_nom = net_unnamed.colonnes_unnamed(donnees)
        message_nom = net_unnamed.affichage_unnamed(colonnes_nom)
        # Si la liste colonnes_nom ne comporte pas de données, alors toutes les colonnes ont des noms
        if len(colonnes_nom) == 0 :
            st.write('Vos colonnes comportent toutes des noms de variables !')
        # Sinon, si la liste colonnes_nom comporte des données, on affiche les colonnes
        else:
            st.write(message_nom)
            st.write("Affichage des 5 premières lignes de la base de données " + selected_database + " :")
            st.write(donnees[colonnes_nom].head())
            # Et on décide ce qu'on veut faire de ces colonnes
            st.write('Souhaitez-vous ?')
            supprimer_colonnes = st.checkbox("Supprimer toutes les colonnes sans nom ?")
            supp_colonne_choix = st.checkbox("Choisir les colonnes à supprimer")
            renommer_colonne = st.checkbox("Renommer la(les) colonne(s) sans nom ?")
            # On supprime toutes les colonnes sans nom
            if supprimer_colonnes :
                donnees = general.supp_colonnes(donnees,colonnes_nom)
                st.write("Vous venez de supprimer toutes les colonnes sans nom. Voici votre nouvelle base de données : ")
                st.write(donnees.head())
            # On choisit les colonnes qu'on veut supprimer 
            if supp_colonne_choix : 
                col_selec_supp = st.multiselect("Sélectionnez une ou plusieurs colonnes à supprimer", colonnes_nom)
                colonnes_supp = []
                for colonnes in col_selec_supp :
                    colonnes_supp.append(colonnes)
                donnees = general.supp_colonnes(donnees,colonnes_supp)
                st.write("Vous venez de supprimer la (les) colonne(s) sélectionnée(s). Voici votre nouvelle base de données : ")
                st.write(donnees.head())    
            # On choisit le nom que l'on veut donner à la (aux) colonne(s)                
            if renommer_colonne : 
                for i in range(len(colonnes_nom)) :
                    colonne = colonnes_nom[i]
                    nouveau_nom = st.text_input("Entrez le nouveau nom pour la colonne "+colonne, "")
                    donnees = general.renommer_colonnes(donnees,colonne,nouveau_nom)
                    st.write("Vous venez de renommer la colonne "+ colonne + "par :" + nouveau_nom + ". Voici votre nouvelle base de données :")
                    st.write(donnees.head())
        donnees = donnees
    
    #########################################################
    ### Etape 2 - Identification des valeurs manquantes : ###
    #########################################################
    with st.expander('Etape 2 : Identification et traitement des valeurs manquantes :') :
        message_valeurs, valeurs_null = nan_info.identification_nan(donnees)
        st.write(message_valeurs)
        if valeurs_null == "Oui" :
            donnees = nan_traitement.choix_traitement_nan(donnees)
        else :
            donnees = donnees
    
    return donnees
