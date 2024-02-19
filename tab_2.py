import streamlit as st

from data_management import nettoyage

def nettoyage_donnees(selected_database,donnees) :
    
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
            supprimer_colonnes = st.checkbox("Supprimer toutes les colonnes sans nom ?")
            supp_colonne_choix = st.checkbox("Choisir les colonnes à supprimer")
            renommer_colonne = st.checkbox("Renommer la(les) colonne(s) sans nom ?")
            
            if supprimer_colonnes :
                donnees = nettoyage.supp_colonnes(donnees,colonnes_nom)
                st.write("Vous venez de supprimer toutes les colonnes sans nom. Voici votre nouvelle base de données : ")
                st.write(donnees.head())
                
            if supp_colonne_choix : 
                col_selec_supp = st.multiselect("Sélectionnez une ou plusieurs colonnes à supprimer", colonnes_nom)
                colonnes_supp = []
                for colonnes in col_selec_supp :
                    colonnes_supp.append(colonnes)
                donnees = nettoyage.supp_colonnes(donnees,colonnes_supp)
                st.write("Vous venez de supprimer la (les) colonne(s) sélectionnée(s). Voici votre nouvelle base de données : ")
                st.write(donnees.head())    
                            
            if renommer_colonne : 
                for i in range(len(colonnes_nom)) :
                    colonne = colonnes_nom[i]
                    nouveau_nom = st.text_input("Entrez le nouveau nom pour la colonne "+colonne, "")
                    donnees = nettoyage.renommer_colonnes(donnees,colonne,nouveau_nom)
                    st.write("Vous venez de renommer la colonne "+ colonne + "par :" + nouveau_nom + ". Voici votre nouvelle base de données :")
                    st.write(donnees.head())
        donnees = donnees
    
    ### Etape 2 - Identification des valeurs manquantes : 
    with st.expander('Etape 2 : Identification et traitement des valeurs manquantes :') :
        message_valeurs, valeurs_null = nettoyage.identification_nan(donnees)
        st.write(message_valeurs)
        if valeurs_null == "Oui" :
            donnees = nettoyage.choix_traitement_nan(donnees)
        else :
            donnees = donnees
    
    return donnees
