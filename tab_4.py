"""
IMPORTS NÉCESSAIRES À CE MODULE :
"""

# Pour la récupération d'entrées utilisateur sur streamlit + l'affichage (titres, figures, texte) :
import streamlit as st

# Module contenant les fonctions appelées pour le modèle de regression
import regression # remplacer par : from modeles import regression

# Pour la validation croisée
from sklearn.linear_model import LinearRegression, Ridge, Lasso


"""
FONCTION "ETAPE_REGRESSION" :
    > fonction unique de ce module
    > entrée : la serie "target" + le dataframe "features" (entrées du modèle)
    > sorties : R² et erreur quadratique moyenne
"""

def etapes_regression(features,target):

    st.subheader('Modèle')

    """
    1. SPLIT DES DONNÉES :
    """
    pourentage_test_defaut = 20
    pourcentage_test = st.text_input('Entrez un pourcentage (ex: entrez "20" pour 20%) :', pourentage_test_defaut)
    test_size = float(pourcentage_test)/100
    
    X_train, X_test, y_train, y_test = regression.split(features,target,test_size)

    st.write("Taille de l'échantillon d'entraînement : ", X_train.shape[0])
    st.write("Taille de l'échantillon de test : ", X_test.shape[0])


    """
    2. CHOIX DU MODÈLE DE RÉGRESSION :
    """

    modele_selection = st.radio("Sélectionnez un modèle de régression : ", \
                                        ("LinearRegression (par défaut)", "Ridge", "Lasso")
                                        )
    st.write("Vous avez choisi : "+modele_selection)


    """
    3. ENTRAINEMENT DU MODÈLE :
    """

    if modele_selection == "Ridge":
        # n_alphas = 1_000
        # alphas = np.arange(0,n_alphas,0.5)
        # for alpha in alphas:
        alpha = 0.5
        y_pred = regression.ridge(alpha,X_train,y_train,X_test)
    elif modele_selection == "Lasso":
        alpha = 0.5
        y_pred = regression.lasso(alpha,X_train,y_train,X_test)
    else:
        y_pred = regression.linear(X_train,y_train,X_test)


    """
    4. CALCUL DES METRICS :
    """

    R2, MSE = regression.metrics(y_test, y_pred)
    st.write("R² = ", R2)
    st.write("Erreur quadratique moyenne = ",MSE)


    """
    5. CROSS VALIDATION
    """

    alpha = 0.5
    n_splits = 5

    if modele_selection == "Ridge":
        model = Ridge(alpha=alpha)
    elif modele_selection == "Lasso":
        model = Lasso(alpha=alpha)
    else:
        model = LinearRegression()

    cv_scores, cv_scores_moy = regression.validation_croisee(model,n_splits,features,target)

    # Affichage les scores de validation croisée
    st.write("Scores de validation croisée:", cv_scores)
    st.write("Score moyen de validation croisée:", cv_scores_moy)



    # sorties de fonction tab_4 :
    return (R2, MSE)