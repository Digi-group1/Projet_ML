"""
IMPORTS NÉCESSAIRES À CE MODULE :
"""

# Pour le split
from sklearn.model_selection import train_test_split

# Pour les fonctions qui appellent les modèles de regression
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import KFold


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
Regression linéaire
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
    MSE = round(mean_squared_error(y_test,y_pred),4)
    return R2, MSE


"""
# Validation croisée
"""
# Fonction qui lance une validation croisée pour un modèle donné en input, retourne les scores et le score moyen
def validation_croisee(model,n_splits,features,target):
    # model : instanciation du modèle (se fait en amont de l'appel de la fonction)
    # n_splits : Nombre de plis pour la validation croisée (input utilisateur)
    
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)

    # Liste pour stocker les scores de validation croisée
    cv_scores = list()

    # Boucle sur les "n_splits" plis de la validation croisée :
    for train_index, test_index in kf.split(features):
        X_train, X_test = features.iloc[train_index], features.iloc[test_index]
        y_train, y_test = target.iloc[train_index], target.iloc[test_index]

        # Entraînement du modèle sur les données d'entraînement :
        model.fit(X_train, y_train)

        # Évaluation du modèle sur les données de test :
        score = model.score(X_test, y_test)
        cv_scores.append(score)
    # score moyen
    cv_scores_moy = sum(cv_scores) / n_splits

    return cv_scores, cv_scores_moy
