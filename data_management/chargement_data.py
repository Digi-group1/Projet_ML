import pandas as pd 

def charger(nom_base):
    if nom_base == 'Diabète':
        return pd.read_csv(r'data\diabete.csv', sep=",")
    elif nom_base == 'Vins':
        return pd.read_csv(r'data\vin.csv', sep=",")