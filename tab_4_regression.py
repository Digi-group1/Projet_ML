"""
IMPORTS NÉCESSAIRES À CE MODULE :
"""

# Pour la récupération d'entrées utilisateur sur streamlit + l'affichage (titres, figures, texte) :
import streamlit as st

# Module contenant les fonctions appelées pour le modèle de regression
import regression # remplacer par : from modeles import regression

# Pour la validation croisée et le grissearch
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import GridSearchCV,train_test_split


"""
FONCTION "ETAPE_REGRESSION" :
    > fonction unique de ce module
    > entrée : la serie "target" + le dataframe "features" (entrées du modèle)
    > sorties : R² et erreur quadratique moyenne
"""

def etapes(features,target):

    st.subheader('Modèle')
   
    """
    1. CHOIX D'UN MODÈLE
    """

    with st.expander("**Choix d'un modèle de régression :**", expanded=False):
       
        """
        a. CHOIX DU MODÈLE DE RÉGRESSION :
        """

        modele_selection = st.radio("Sélectionnez un modèle de régression : ", \
                                            ("LinearRegression (par défaut)", "Ridge", "Lasso")
                                            )
        st.write("Vous avez choisi : "+modele_selection)


        """
        b. CROSS VALIDATION
        """

        n_splits = st.number_input(label="Entrez un nombre de lots : ", min_value=5, max_value=10, step=1)

        if modele_selection == "Ridge":
            alpha_defaut = 0.5
            max_iter_defaut = 1000
            tol_defaut = 1e-4
            alpha = float(st.text_input("Entrez une valeur de alpha (nombre décimal compris entre 0 et 1 ) : ", alpha_defaut))
            max_iter = int(st.text_input("Entrez un nombre d'itérations maximum : ", max_iter_defaut))
            tol = float(st.text_input("Entrez une valeur pour la tolérance : ", tol_defaut))
            model = Ridge(alpha=alpha, max_iter=max_iter, tol= tol)

        elif modele_selection == "Lasso":
            alpha_defaut = 0.5
            max_iter_defaut = 1000
            tol_defaut = 1e-4
            alpha = float(st.text_input("Entrez une valeur de alpha (nombre décimal compris entre 0 et 1 ) : ", alpha_defaut))
            max_iter = int(st.text_input("Entrez un nombre d'itérations maximum : ", max_iter_defaut))
            tol = float(st.text_input("Entrez une valeur pour la tolérance : ", tol_defaut))
            model = Lasso(alpha=alpha, max_iter=max_iter, tol= tol)

        else:
            model = LinearRegression()

        # Appel de la validation croisée, retourne les 3 metrics :
        # cv_R2, cv_RMSE, cv_MAE = regression.validation_croisee(model,n_splits,features,target)
        cv_metrics = regression.validation_croisee(model,n_splits,features,target)
        st.write(cv_metrics)

        # Métrics moyennes
        cv_R2_moy = round((sum(cv_metrics['R2']) / n_splits),4)
        cv_RMSE_moy = round((sum(cv_metrics['RMSE']) / n_splits),2)
        cv_MAE_moy = round((sum(cv_metrics['MAE']) / n_splits),2)

        # Affichage les scores de validation croisée
        st.write("Metrics moyennes de validation croisée sur les", str(n_splits),"lots :")
        st.write("- Moyenne des coefficients de détermination : R² = ", str(cv_R2_moy))
        st.write("- Moyenne des racines carrées de l'erreur quadratique moyenne : RMSE = ",str(cv_RMSE_moy))
        st.write("- Moyenne de l'erreur absolue moyenne : MAE = ",str(cv_MAE_moy))

        
    """
    3. GRID SEARCH
    """
    n_splits = st.number_input(label="Entrez un nombre de lots pour la validation croisée : ", min_value=5, max_value=10, step=1)
    # scoring_defaut = 'r2'
    # scoring = st.multiselect(label="Sélectionnez la métrique de performance : ", options = ['r2','neg_mean_squared_error'],default=scoring_defaut)
    scoring = 'r2'

    with st.expander("**Évaluation des modèles de régression :**", expanded=False):

        # Liste des modèles à évaluer
        models = [
            ('LinearRegression', LinearRegression()),
            ('Lasso', Lasso()),
            ('Ridge', Ridge())
        ]

        # Grille de paramètres pour chaque modèle
        parameters = {
            'LinearRegression': {},
            'Lasso': {'alpha': [0.01, 0.1, 1.0, 10.0], 'max_iter': [100, 1000, 10000], 'tol': [0.0001, 0.001, 0.01]},
            'Ridge': {'alpha': [0.01, 0.1, 1.0, 10.0], 'max_iter': [100, 1000, 10000], 'tol': [0.0001, 0.001, 0.01]}
        }

        # Split des données
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
        
        # Effectuer une recherche sur grille pour chaque modèle
        best_estimators = {}
        for model_name, model in models:
            grid_search = GridSearchCV(model, parameters[model_name], cv=5, scoring=scoring)
            grid_search.fit(X_train, y_train)
            best_estimators[model_name] = grid_search.best_estimator_

        st.write(best_estimators)


    # sorties de fonction tab_4 :
    return (model)