#########################
##### PARTIE IMPORT #####
#########################

#########################
# IMPORT DES LIBRAIRIES #
#########################

import streamlit as st



####################################################################
##### PARTIE VALEURS NULLES -- SUPPRESSION DES LIGNES ENTIERES ##### 
####################################################################

#####################
# SUPPRESSION LIGNE #
#####################

def suppression_ligne_null(data) :
    # On affiche un message d'alerte
    st.write("<span style='color:red'>!! Attention, cette action peut fortement réduire le nombre d'enregistrements de votre base de données !! </span>", unsafe_allow_html=True)
    # On compte le nombre d'enregistrements avant suppression, et on affiche le message
    nb_enreg = data.shape[0]
    st.write("Votre base de données contient actuellement " + str(nb_enreg) + " enregistrements")
    # On compte le nombre d'enregistrement qu'il y aurait après suppression, et on affiche le message
    data_sans_nulles = data.dropna()
    nb_enreg_apres = data_sans_nulles.shape[0]
    nb_supp = nb_enreg - nb_enreg_apres
    st.write("Vous allez supprimer " + str(nb_supp) + " enregistrements")
    # On redemande l'utilisateur s'il est sûr de vouoloir supprimer toutes les lignes qui comportent des valeurs nulles
    verification_supp = st.radio("Souhaitez-vous vraiment supprimer tous les enregistrements ?", ("Oui", "Non"))
    # Si non : On revient au menu précédent
    if verification_supp == "Non" :
        st.write("Veuillez sélectionner un autre choix au menu du dessus")
    # Si oui : On applique la suppression
    elif verification_supp == "Oui" :
        data = data_sans_nulles
    return data