# Import des modules
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader.data as web


def bool_pente(label, index, dataframe, limite=0.):
    pente = (dataframe[label].values[index] - dataframe[label].values[index - 1]) / (index - (index - 1))
    # print(f'pente : {pente}')
    if pente >= limite:
        return True
    return False


# Simulation achat/vente sur 2019
date_debut = dt.datetime(2019, 1, 2)
df = web.DataReader('AAPL', 'yahoo', date_debut, date_debut + dt.timedelta(days=+5))
# print(df)
valeur_action = float(df['Open'].values[3])
mise_depart = 100.  # euros
# Achat d'action au 7 Janvier 2019
nbr_action = mise_depart / valeur_action
print('valeur_action : ', valeur_action)
print('nbr_action : ', nbr_action)

# Creation du dataframe
my_df = pd.DataFrame(data=df['Close'])

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
inc = 3
for jour in range(6, 230, 1):
    try:
        df = web.DataReader('AAPL', 'yahoo', date_debut + dt.timedelta(days=jour), date_debut + dt.timedelta(days=jour))
        # print(df)
        # print(my_df['Close'])
        df_new = pd.DataFrame([[float(df['Close'].values[0]), 0., 0., 0., 0., False, False,
                                np.NaN, np.NaN]],
                              index=df.index,
                              columns=['Close', 'Mise', 'Secu', 'PorteFeuille',
                                       'NbrAction', 'Vente', 'Achat', 'ValeurAchat', 'ValeurVente'])
        #print(df_new)
        my_df = my_df.append(df_new)
        # print(my_df)
        if not my_df['Achat'].values[inc]:
            my_df['ValeurAchat'].values[inc] = my_df['ValeurAchat'].values[inc - 1]
            my_df['Mise'].values[inc] = my_df['Mise'].values[inc - 1]
            my_df['PorteFeuille'].values[inc] = my_df['Close'].values[inc] * my_df['NbrAction'].values[inc - 1]
            my_df['NbrAction'].values[inc] = my_df['NbrAction'].values[inc - 1]
        if not my_df['Vente'].values[inc]:
            my_df['ValeurVente'].values[inc] = my_df['ValeurVente'].values[inc - 1]
            my_df['Secu'].values[inc] = my_df['Secu'].values[inc - 1]
        #print(my_df)
        if achat:  # On possède des actions
            # Regarde si vente
            if bool_pente('Close', inc + 1, my_df):  # Pas de vente l'action augmente ou stagne
                vente = False
            else:  # on vend
                vente = True
        # print('Vente ?')
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
            print(f"VENTE (Date : {my_df.index[inc]}) :\n     Mise : {my_df['Mise'].values[inc]}\n"
                  f"     Sécurisé : {my_df['Secu'].values[inc]}\n"
                  f"     Valeur d'achat : {my_df['ValeurAchat'].values[inc - 1]}\n"
                  f"     Valeur de vente : {my_df['ValeurVente'].values[inc]}")
            achat = False
        # print('achat ?')
        if vente and not achat and not my_df['Vente'].values[inc] and not my_df['Achat'].values[inc]:
            # On a vendu et pas encore racheté.
            # Conditions pour rachat
            if bool_pente('Close', inc + 1, my_df):  # On achète, car remonté au niveau vente
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
                print(f"ACHAT (Date : {my_df.index[inc]}) :\n     PorteFeuille : {my_df['PorteFeuille'].values[inc]}\n"
                      f"     Sécurisé : {my_df['Secu'].values[inc]}\n"
                      f"     Nbr Action(s) : {my_df['NbrAction'].values[inc]}\n"
                      f"     Valeur d'achat : {my_df['ValeurAchat'].values[inc]}\n"
                      f"     Valeur de vente : {my_df['ValeurVente'].values[inc - 1]}")
        inc += 1
    except KeyError as key:
        pass

print(my_df.tail(10))
# Pour la fin
if my_df['Close'].values[-1] >= my_df['Close'].values[-2]:
    my_df['Mise'].values[-1] = 0.
    my_df['Secu'].values[-1] = my_df['Secu'].values[-2]
    my_df['NbrAction'].values[-1] = my_df['NbrAction'].values[-2]
    my_df['PorteFeuille'].values[-1] = my_df['Close'].values[-1] * my_df['NbrAction'].values[-1]
    my_df['ValeurAchat'].values[-1] = my_df['ValeurAchat'].values[-2]
    my_df['ValeurVente'].values[-1] = my_df['ValeurVente'].values[-2]
    my_df['Vente'].values[inc] = False
    my_df['Achat'].values[inc] = False
else:  # Vente
    my_df['Mise'].values[-1] = 100.
    my_df['Secu'].values[-1] = my_df['Secu'].values[-2] + \
                               my_df['NbrAction'].values[-2] * my_df['Close'].values[-2] - 100.
    my_df['NbrAction'].values[-1] = 0.
    my_df['PorteFeuille'].values[-1] = 0.
    my_df['ValeurAchat'].values[-1] = np.NaN
    my_df['ValeurVente'].values[-1] = my_df['Close'].values[-2]
    my_df['Vente'].values[inc] = True
    my_df['Achat'].values[inc] = False

print(f"A LA FIN (Date : {my_df.index[-1]}) :\n     PorteFeuille : {my_df['PorteFeuille'].values[-1]}\n"
      f"     Nbr Action(s) : {my_df['NbrAction'].values[-1]}\n"
      f"     Sécurisé : {my_df['Secu'].values[-1]}\n"
      f"     Mise : {my_df['Mise'].values[-1]}")

my_df.to_csv(r'/Users/stephanecau/PycharmProjects/StecauApps/FinancialApp/'
             r'simulation_rendement_max_Apple-230jours.csv', index=True)

