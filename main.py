# Import des modules
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader.data as web


def bool_pente(label, index, dataframe, limite=0.):
    pente = (dataframe[label].values[index] - dataframe[label].values[index - 1]) / (index - (index - 1))
    #print(f'pente : {pente}')
    if pente >= limite:
        return True
    return False


# Definition des variables
debut = dt.datetime(2019, 1, 1)  # Date de debut recup donnees
fin = dt.datetime(2019, 12, 31)  # Date de fin recup donnees
tickers = list()  # Liste pour les valeurs
tickers.append('AAPL')  # Ajout apple valeur
#tickers.append('MSFT')  # Ajout microsoft valeur
df = web.DataReader('AAPL', 'yahoo', debut, fin)
#print(df.head())

# Visualisation des donnees de fermeture
#df['Close'].plot()
#plt.show()

# Calcul des moyennes sur 5 jours (1 semaine) [pas de bourse le samedi et le dimanche]
# Calcul de la moyenne sur 2 jours
df['2J'] = df['Close'].rolling(window=2).mean()
# Calcul de la moyenne sur 3 jours
df['3J'] = df['Close'].rolling(window=3).mean()
# Calcul de la moyenne sur 4 jours
df['4J'] = df['Close'].rolling(window=4).mean()
# Calcul de la moyenne sur 5 jours
df['5J'] = df['Close'].rolling(window=5).mean()
# Calcul de la moyenne sur 30 jours (1 mois)
df['6J'] = df['Close'].rolling(window=6).mean()
# Calcul de la moyenne sur 30 jours (1 mois)
df['7J'] = df['Close'].rolling(window=7).mean()

# Visualisation
fig, ax = plt.subplots(figsize=(16, 9))
ax.plot(df.index, df['Close'], label='Apple')
ax.plot(df.index, df['2J'], label='Apple moyenne sur 2 jours')
ax.plot(df.index, df['3J'], label='Apple moyenne sur 3 jours')
ax.plot(df.index, df['4J'], label='Apple moyenne sur 4 jours')
ax.plot(df.index, df['5J'], label='Apple moyenne sur 5 jours')
ax.plot(df.index, df['6J'], label='Apple moyenne sur 6 jours')
ax.plot(df.index, df['7J'], label='Apple moyenne sur 7 jours')
ax.set_xlabel('Date')
ax.set_ylabel('Valeur de fermeture')
ax.legend()
plt.show()

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
