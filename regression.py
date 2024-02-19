"""
IMPORTS NÉCESSAIRES À CE MODULE :
"""

# Pour le split
from sklearn.model_selection import train_test_split

# Pour les fonctions qui appellent les modèles de regression
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import KFold

# Pour le calcul des métrics (RMSE)
import numpy as np
import pandas as pd

# Pour les figures
import matplotlib.pyplot as plt

# Pour intéragir avec streamlit
import streamlit as st


"""
Split
"""
def split(X,y,test_size):
    X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size = test_size,
    random_state = 42)
    return X_train, X_test, y_train, y_test


"""
Modèles de regression linéaire
"""
def linear(X_train,y_train,X_test):
    model = LinearRegression()      # Instanciation du modèle
    model.fit(X_train, y_train)     # Ajustement du modèle aux données d'entraînement
    y_pred = model.predict(X_test)  # Prédiction
    return y_pred

def ridge(alpha,X_train,y_train,X_test):
    model = Ridge(alpha=alpha)      # Instanciation du modèle
    model.fit(X_train, y_train)     # Ajustement du modèle aux données d'entraînement
    y_pred = model.predict(X_test)  # Prédiction
    return y_pred

def lasso(alpha,X_train,y_train,X_test):
    model = Lasso(alpha=alpha)      # Instanciation du modèle
    model.fit(X_train, y_train)     # Ajustement du modèle aux données d'entraînement
    y_pred = model.predict(X_test)  # Prédiction
    return y_pred


"""
Metrics
"""
# Fonction qui retourne deux métrics : R² et erreur quad. moy.
def metrics(y_test,y_pred):
    R2 = round(r2_score(y_test,y_pred),4)
    MSE = mean_squared_error(y_test,y_pred)
    RMSE = round(np.sqrt(MSE),2)
    MAE = round(mean_absolute_error(y_test,y_pred),2)
    return R2, RMSE, MAE


"""
# Validation croisée
"""
# Fonction qui lance une validation croisée pour un modèle donné en input, retourne les scores et le score moyen
def validation_croisee(model,n_splits,features,target):
    # model : instanciation du modèle (se fait en amont de l'appel de la fonction)
    # n_splits : Nombre de plis pour la validation croisée (input utilisateur)
    
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)

    # Dataframe pour stocker les métrics des diffénrents "trains" + tailles des échantillons "train" et "test" :
    # cv_metrics = pd.DataFrame(columns=['R2', 'RMSE', 'MAE'])
    cv_metrics = pd.DataFrame(columns=['R2', 'RMSE', 'MAE','taille éch. train', 'taille éch. test'])

    # Liste pour remplir le dataframe cv_metrics
    liste_metrics = list()
    
    # Boucle sur les "n_splits" plis de la validation croisée :
    for train_index, test_index in kf.split(features):
        X_train, X_test = features.iloc[train_index], features.iloc[test_index]
        y_train, y_test = target.iloc[train_index], target.iloc[test_index]

        # Entraînement du modèle sur les données d'entraînement :
        model.fit(X_train, y_train)

        # Prédiction du modèle sur X_test :
        y_pred = model.predict(X_test)

        # Évaluation du modèle sur les données de test :
        R2, RMSE, MAE = metrics(y_test,y_pred)

        # ligne_metrics = {'R2': R2, 'RMSE': RMSE, 'MAE': MAE}
        ligne_metrics = {'R2': R2, 'RMSE': RMSE, 'MAE': MAE, 'train_sample_size': X_train.shape[0], 'test_sample_size': X_test.shape[0]}
        liste_metrics.append(ligne_metrics)

        # Plots :
        fig, ax = plt.subplots()
        ax.scatter(y_test,y_pred)
        max_value_y = y_test.max()
        plt.plot(np.arange(0,max_value_y))
        ax.set_xlabel('y_pred')
        ax.set_ylabel('y_test')
        st.pyplot(fig)

    cv_metrics = pd.DataFrame(liste_metrics)

    # return cv_R2, cv_RMSE, cv_MAE
    return cv_metrics