# Import des modules
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader.data as web
from Internet import Internet
from Action import Action
from Affichage import Affichage
from Classement import Classement


# DEFINITIONS DES VARIABLES
debut = dt.datetime(2019, 1, 1)  # Date de debut recup donnees
fin = dt.datetime(2021, 12, 31)  # Date de fin recup donnees
# d_tickers = {  # Dictionnaire pour les valeurs
#     'AAPL': {'nom': 'Apple', 'label': 'Close'},
#     'MSFT': {'nom': 'Microsoft', 'label': 'Close'},
# }
d_tickers = {  # Dictionnaire pour les valeurs
    "AI.PA": {"nom": "Air liquide", "label": "Close"},
    "AIR.PA": {"nom": "Airbus", "label": "Close"},
    "ALO.PA": {"nom": "Alstom", "label": "Close"},
    "MT.AS": {"nom": "ArcelorMittal", "label": "Close"},
    "CS.PA": {"nom": "Axa", "label": "Close"},
    "BNP.PA": {"nom": "BNP Paribas", "label": "Close"},
    "EN.PA": {"nom": "Bouygues", "label": "Close"},
    "CAP.PA": {"nom": "Capgemini", "label": "Close"},
    "CA.PA": {"nom": "Carrefour", "label": "Close"},
    "ACA.PA": {"nom": "Credit agricole", "label": "Close"},
    "BN.PA": {"nom": "Danone", "label": "Close"},
    "DSY.PA": {"nom": "Dassault Systemes", "label": "Close"},
    "ENGI.PA": {"nom": "Engie", "label": "Close"},
    "EL.PA": {"nom": "EssilorLuxottica", "label": "Close"},
    "ERF.PA": {"nom": "EUROFINS SCIENTIFIC", "label": "Close"},
    "RMS.PA": {"nom": "Hermes International", "label": "Close"},
    "KER.PA": {"nom": "Kering", "label": "Close"},
    "OR.PA": {"nom": "L-Oreal", "label": "Close"},
    "LR.PA": {"nom": "Legrand", "label": "Close"},
    "MC.PA": {"nom": "LVMH", "label": "Close"},
    "ML.PA": {"nom": "Michelin", "label": "Close"},
    "ORA.PA": {"nom": "Orange", "label": "Close"},
    "RI.PA": {"nom": "Pernod Ricard", "label": "Close"},
    "PUB.PA": {"nom": "Publicis Groupe", "label": "Close"},
    "RNO.PA": {"nom": "Renault", "label": "Close"},
    "SAF.PA": {"nom": "Safran", "label": "Close"},
    "SGO.PA": {"nom": "Saint-Gobain", "label": "Close"},
    "SAN.PA": {"nom": "Sanofi", "label": "Close"},
    "SU.PA": {"nom": "Schneider Electric", "label": "Close"},
    "GLE.PA": {"nom": "Societe generale", "label": "Close"},
    "STLA.PA": {"nom": "Stellantis", "label": "Close"},
    "STM.PA": {"nom": "STMicroelectronics", "label": "Close"},
    "TEP.PA": {"nom": "Teleperformance", "label": "Close"},
    "HO.PA": {"nom": "Thales", "label": "Close"},
    "TTE.PA": {"nom": "TotalEnergies", "label": "Close"},
    "URW.AS": {"nom": "Unibail-Rodamco-Westfield", "label": "Close"},
    "VIE.PA": {"nom": "Veolia", "label": "Close"},
    "DG.PA": {"nom": "Vinci", "label": "Close"},
    "VIV.PA": {"nom": "Vivendi", "label": "Close"},
    "WLN.PA": {"nom": "Worldline", "label": "Close"}
}

# RECUPERATION DATAFRAME DES ACTIONS SUR INTERNET
df = Internet.get_actions_df(d_tickers, debut, fin)
df.to_csv(r'/Users/stephanecau/PycharmProjects/StecauApps/FinancialApp/action_CAC40.csv', index=True)
#df = pd.read_csv(r'/Users/stephanecau/PycharmProjects/StecauApps/FinancialApp/action_CAC40.csv', index_col=0)


# CREATION DES INSTANCES D'ACTIONS
for key, valeur in d_tickers.items():
    action = Action(valeur['nom'], valeur['label'], key, df)
print(Action.l_actions)

# Visualisation des donnees de fermeture
#Affichage.affichage_actions()

# Affichage spécifiques
Affichage.affichage_selections(Action.l_actions[Action.action_index('Air liquide')].df,
                               **{'Air liquide_Close': 'Cours Air liquide à la fermeture',
                                  'Air liquide_J5': 'Moyenne glissante Air liquide sur 5 jours'})

print(f"Liste labels action Air liquide = {Action.l_actions[Action.action_index('Air liquide')].l_labels}")

# REALISATION DU CLASSEMENT DES ACTIONS
classement = Classement(Action.l_actions)
Affichage.affichage_actions()
toto





# Simulation achat/vente sur 2019
date_debut = dt.datetime(2019, 1, 2)
df = web.DataReader('AAPL', 'yahoo', date_debut, date_debut + dt.timedelta(days=+5))
#print(df)
valeur_action = float(df['Open'].values[3])
mise_depart = 100.  # euros
# Achat d'action au 7 Janvier 2019
nbr_action = mise_depart / valeur_action
print('valeur_action : ', valeur_action)
print('nbr_action : ', nbr_action)

# Creation du dataframe
my_df = pd.DataFrame(data=df['Close'])

# Calcul des moyennes et ajout dans le dataframe
my_df['J2'] = df['Close'].rolling(window=2).mean()
my_df['J3'] = df['Close'].rolling(window=3).mean()
my_df['J4'] = df['Close'].rolling(window=4).mean()
my_df['J5'] = df['Close'].rolling(window=5).mean()
my_df['J6'] = df['Close'].rolling(window=6).mean()
my_df['J7'] = df['Close'].rolling(window=7).mean()

# Rajout des valeurs specifiques
my_df['Mise'] = 100.
my_df['Secu'] = 0.
my_df['PorteFeuille'] = 0.
my_df['NbrAction'] = 0.
my_df['Vente'] = False
my_df['Achat'] = False
my_df['ValeurAchat'] = np.NaN
my_df['ValeurVente'] = np.NaN
for i, my_ligne in enumerate(my_df.index):
    if i < len(my_df.index) - 1:
        my_df['Mise'].values[i] = 100.
        my_df['Secu'].values[i] = 0.
        my_df['PorteFeuille'].values[i] = 0.
        my_df['NbrAction'].values[i] = 0.
        my_df['Vente'].values[i] = False
        my_df['Achat'].values[i] = False
        my_df['ValeurAchat'].values[i] = np.NaN
        my_df['ValeurVente'].values[i] = np.NaN
    else:
        my_df['Mise'].values[i] = 0.
        my_df['Secu'].values[i] = 0.
        my_df['PorteFeuille'].values[i] = my_df['Close'].values[i] * nbr_action
        my_df['NbrAction'].values[i] = nbr_action
        my_df['Vente'].values[i] = False
        my_df['Achat'].values[i] = True
        my_df['ValeurAchat'].values[i] = valeur_action
        my_df['ValeurVente'].values[i] = np.NaN

#print(my_df)

# Iteration sur l'année 2019
vente = False
achat = True
inc = 4
for jour in range(6, 230, 1):
    try:
        df = web.DataReader('AAPL', 'yahoo', date_debut + dt.timedelta(days=jour), date_debut + dt.timedelta(days=jour))
        #print(df)
        #print(my_df['Close'])
        df_new = pd.DataFrame([[float(df['Close'].values[0]), 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., False, False,
                                np.NaN, np.NaN]],
                              index=df.index,
                              columns=['Close', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'Mise', 'Secu', 'PorteFeuille',
                                       'NbrAction', 'Vente', 'Achat', 'ValeurAchat', 'ValeurVente'])
        #print(df_new)
        my_df = my_df.append(df_new)
        #print(my_df)
        my_df['J2'] = my_df['Close'].rolling(window=2).mean()
        my_df['J3'] = my_df['Close'].rolling(window=3).mean()
        my_df['J4'] = my_df['Close'].rolling(window=4).mean()
        my_df['J5'] = my_df['Close'].rolling(window=5).mean()
        my_df['J6'] = my_df['Close'].rolling(window=6).mean()
        my_df['J7'] = my_df['Close'].rolling(window=7).mean()
        my_df['Mise'].values[inc] = my_df['Mise'].values[inc - 1]
        my_df['Secu'].values[inc] = my_df['Secu'].values[inc - 1]
        my_df['PorteFeuille'].values[inc] = my_df['Close'].values[inc] * my_df['NbrAction'].values[inc - 1]
        my_df['NbrAction'].values[inc] = my_df['NbrAction'].values[inc - 1]
        my_df['ValeurAchat'].values[inc] = my_df['ValeurAchat'].values[inc - 1]
        my_df['ValeurVente'].values[inc] = my_df['ValeurVente'].values[inc - 1]
        #print(my_df)
        if achat:  # On possède des actions
            # Regarde si vente
            # if bool_pente('Close', inc, my_df):  # Pas de vente l'action augmente ou stagne
            #     vente = False
            # elif bool_pente('J2', inc, my_df):  # Pas de vente l'action diminue mais pas sur 2 jours
            #     vente = False
            # elif bool_pente('J3', inc, my_df):  # Pas de vente l'action diminue mais pas sur 3 jours
            #     vente = False
            # elif bool_pente('J4', inc, my_df):  # Pas de vente l'action diminue mais pas sur 4 jours
            #     vente = False
            # elif bool_pente('J5', inc, my_df):  # Pas de vente l'action diminue mais pas sur 5 jours
            #     vente = False
            # elif bool_pente('J6', inc, my_df):  # Pas de vente l'action diminue mais pas sur 6 jours
            #     vente = False
            # elif bool_pente('J7', inc, my_df):  # Pas de vente l'action diminue mais pas sur 7. jours
            #     vente = False

            # vente si diminution de l'action qui provoque diminution moyenne 2j, 3j, 4j et 7j et
            # valeur plus basse qu'il y a 14j ou pente de plus de 1
            if not bool_pente('Close', inc, my_df) and \
                    not bool_pente('J2', inc, my_df) and \
                    not bool_pente('J3', inc, my_df) and \
                    not bool_pente('J4', inc, my_df) and \
                    not bool_pente('J7', inc, my_df, -0.05) and \
                    (my_df['Close'].values[inc] <= my_df['Close'].values[inc - 10] or
                     not bool_pente('J2', inc, my_df, -0.8)):
                vente = True
            else:  # on ne vend pas
                vente = False
        #print('Vente ?')
        if vente and achat:  # on va vendre, on ne possèdera plus d'action
            my_df['Vente'].values[inc] = True
            my_df['Achat'].values[inc] = False
            if my_df['Close'].values[inc] * my_df['NbrAction'].values[inc] > 100.:
                my_df['Mise'].values[inc] = 100.
                my_df['Secu'].values[inc] += my_df['Close'].values[inc] * my_df['NbrAction'].values[inc] - 100.
            else:
                my_df['Mise'].values[inc] = my_df['Close'].values[inc] * my_df['NbrAction'].values[inc]
                my_df['Secu'].values[inc] += 0.
            my_df['PorteFeuille'].values[inc] = 0.
            my_df['NbrAction'].values[inc] = 0.
            my_df['ValeurVente'].values[inc] = my_df['Close'].values[inc]
            my_df['ValeurAchat'].values[inc] = np.NaN
            print(f"VENTE (Date : {my_df.index[-1]}) :\n     Mise : {my_df['Mise'].values[-1]}\n"
                  f"     Sécurisé : {my_df['Secu'].values[-1]}\n"
                  f"     Valeur d'achat : {my_df['ValeurAchat'].values[-2]}\n"
                  f"     Valeur de vente : {my_df['ValeurVente'].values[-1]}")
            achat = False
        #print('achat ?')
        if vente and not achat and not my_df['Vente'].values[inc] and not my_df['Achat'].values[inc]:
            # On a vendu et pas encore racheté.
            # Conditions pour rachat
            if my_df['ValeurVente'].values[inc] <= my_df['Close'].values[inc] and not my_df['Vente'].values[inc - 1] \
                    or bool_pente('Close', inc, my_df) and bool_pente('J2', inc, my_df) and bool_pente('J3', inc, my_df):  # On achète, car remonté au niveau vente
                my_df['Vente'].values[inc] = False
                my_df['Achat'].values[inc] = True
                achat = True
                vente = False
                my_df['Mise'].values[inc] = 0.
                my_df['Secu'].values[inc] = my_df['Secu'].values[inc - 1]
                my_df['NbrAction'].values[inc] = my_df['Mise'].values[inc - 1] / my_df['Close'].values[inc]
                my_df['PorteFeuille'].values[inc] = my_df['Close'].values[inc] * my_df['NbrAction'].values[inc]
                my_df['ValeurAchat'].values[inc] = my_df['Close'].values[inc]
                my_df['ValeurVente'].values[inc] = np.NaN
                print(f"ACHAT (Date : {my_df.index[-1]}) :\n     PorteFeuille : {my_df['PorteFeuille'].values[-1]}\n"
                      f"     Sécurisé : {my_df['Secu'].values[-1]}\n"
                      f"     Nbr Action(s) : {my_df['NbrAction'].values[-1]}\n"
                      f"     Valeur d'achat : {my_df['ValeurAchat'].values[-1]}\n"
                      f"     Valeur de vente : {my_df['ValeurVente'].values[-2]}")
        inc += 1
    except KeyError as key:
        pass
    
print(my_df.tail(10))
print(f"A LA FIN (Date : {my_df.index[-1]}) :\n     PorteFeuille : {my_df['PorteFeuille'].values[-1]}\n"
      f"     Nbr Action(s) : {my_df['NbrAction'].values[-1]}\n"
      f"     Sécurisé : {my_df['Secu'].values[-1]}\n"
      f"     Mise : {my_df['Mise'].values[-1]}")

my_df.to_csv(r'/Users/stephanecau/PycharmProjects/StecauApps/FinancialApp/'
             r'simulation_commit-1ereVerdion.csv', index=True)
