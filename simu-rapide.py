# Import des modules
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader.data as web


def bool_pente(label, index, dataframe, limite=0.):
    #print(index)
    #print(len(dataframe.index) - 1)
    if index <= len(dataframe.index) - 1:
        pente = (dataframe[label].values[index] - dataframe[label].values[index - 1]) / (index - (index - 1))
        # print(f'pente : {pente}')
        if pente >= limite:
            return True
    return False


# Simulation achat/vente sur 2019
date_debut = dt.datetime(2019, 1, 7)
df = web.DataReader('AAPL', 'yahoo', date_debut, date_debut + dt.timedelta(days=+359))
# print(df)
valeur_action = float(df['Open'].values[0])
mise_depart = 100.  # euros
# Achat d'action au 7 Janvier 2019
nbr_action = mise_depart / valeur_action
print('valeur_action : ', valeur_action)
print('nbr_action : ', nbr_action)

# Creation du dataframe
my_df = pd.DataFrame(data=df['Close'])

# Rajout des moyennes
my_df['J2'] = my_df['Close'].rolling(window=2).mean()
my_df['J3'] = my_df['Close'].rolling(window=3).mean()
my_df['J4'] = my_df['Close'].rolling(window=4).mean()
my_df['J5'] = my_df['Close'].rolling(window=5).mean()
my_df['J6'] = my_df['Close'].rolling(window=6).mean()
my_df['J7'] = my_df['Close'].rolling(window=7).mean()

# Rajout des valeurs specifiques
my_df['SansTransaction'] = nbr_action * my_df['Close']

#print(my_df.head(5))
#print(my_df.tail(5))

# Initialisation lancement Scenario
bool_Max = True
bool_Max_ssSecu = True
bool_Max_NbrActionCste = True
bool_S1 = True
bool_S1_ssSecu = True
bool_S1_NbrActionCste = True

# Iteration sur l'année 2019 Rendement Max
if bool_Max:
    # Rajout des valeurs specifiques
    my_df['Mise'] = 100.
    my_df['Secu'] = 0.
    my_df['PorteFeuille'] = 0.
    my_df['NbrAction'] = 0.
    my_df['Vente'] = False
    my_df['Achat'] = False
    my_df['ValeurAchat'] = np.NaN
    my_df['ValeurVente'] = np.NaN
    my_df['MaxRendement'] = 0.

    # Initialisation du premier achat
    my_df['Mise'].values[0] = 0.
    my_df['PorteFeuille'].values[0] = nbr_action * my_df['Close'].values[0]
    my_df['NbrAction'].values[0] = nbr_action
    my_df['Achat'].values[0] = True
    my_df['ValeurAchat'].values[0] = valeur_action
    my_df['MaxRendement'].values[0] = my_df['Mise'].values[0] + my_df['Secu'].values[0] + my_df['PorteFeuille'].values[0]
    vente = False
    achat = True
    inc = 0
    for i, my_ligne in enumerate(my_df.index):
        if i > 0:
            my_df['Mise'].values[i] = my_df['Mise'].values[i - 1]
            my_df['Secu'].values[i] = my_df['Secu'].values[i - 1]
            my_df['NbrAction'].values[i] = my_df['NbrAction'].values[i - 1]
            my_df['PorteFeuille'].values[i] = my_df['Close'].values[i] * my_df['NbrAction'].values[i]
            my_df['ValeurAchat'].values[i] = my_df['ValeurAchat'].values[i - 1]
            my_df['ValeurVente'].values[i] = my_df['ValeurVente'].values[i - 1]
            my_df['MaxRendement'].values[i] = my_df['Mise'].values[i] + my_df['Secu'].values[i] + \
                                              my_df['PorteFeuille'].values[i]
        #print(my_df.iloc[i])
        if achat:  # On possède des actions
            # Regarde si vente
            if bool_pente('Close', i + 1, my_df):  # Pas de vente l'action augmente ou stagne
                vente = False
            else:  # on vend
                vente = True
        # print('Vente ?')
        if vente and achat:  # on va vendre, on ne possèdera plus d'action
            my_df['Vente'].values[i] = True
            my_df['Achat'].values[i] = False
            if my_df['Close'].values[i] * my_df['NbrAction'].values[i] > 100.:
                my_df['Mise'].values[i] = 100.
                my_df['Secu'].values[i] += my_df['Close'].values[i] * my_df['NbrAction'].values[i] - 100.
            else:
                my_df['Mise'].values[i] = my_df['Close'].values[i] * my_df['NbrAction'].values[i]
                my_df['Secu'].values[i] += 0.
            my_df['PorteFeuille'].values[i] = 0.
            my_df['NbrAction'].values[i] = 0.
            my_df['ValeurVente'].values[i] = my_df['Close'].values[i]
            my_df['ValeurAchat'].values[i] = np.NaN
            my_df['MaxRendement'].values[i] = my_df['Mise'].values[i] + my_df['Secu'].values[i] + \
                                              my_df['PorteFeuille'].values[i]
            #print(my_df.iloc[i])
            print(f"VENTE (Date : {my_df.index[i]}) :\n     Mise : {my_df['Mise'].values[i]}\n"
                  f"     Sécurisé : {my_df['Secu'].values[i]}\n"
                  f"     Valeur d'achat : {my_df['ValeurAchat'].values[i - 1]}\n"
                  f"     Valeur de vente : {my_df['ValeurVente'].values[i]}")
            achat = False
        # print('achat ?')
        if vente and not achat and not my_df['Vente'].values[i] and not my_df['Achat'].values[i]:
            # On a vendu et pas encore racheté.
            # Conditions pour rachat
            if bool_pente('Close', i + 1, my_df):  # On achète, car remonté au niveau vente
                my_df['Vente'].values[i] = False
                my_df['Achat'].values[i] = True
                achat = True
                vente = False
                my_df['Mise'].values[i] = 0.
                my_df['Secu'].values[i] = my_df['Secu'].values[i - 1]
                my_df['NbrAction'].values[i] = my_df['Mise'].values[i - 1] / my_df['Close'].values[i]
                my_df['PorteFeuille'].values[i] = my_df['Close'].values[i] * my_df['NbrAction'].values[i]
                my_df['ValeurAchat'].values[i] = my_df['Close'].values[i]
                my_df['ValeurVente'].values[i] = np.NaN
                my_df['MaxRendement'].values[i] = my_df['Mise'].values[i] + my_df['Secu'].values[i] + \
                                                  my_df['PorteFeuille'].values[i]
                #print(my_df.iloc[i])
                print(f"ACHAT (Date : {my_df.index[i]}) :\n     PorteFeuille : {my_df['PorteFeuille'].values[i]}\n"
                      f"     Sécurisé : {my_df['Secu'].values[i]}\n"
                      f"     Nbr Action(s) : {my_df['NbrAction'].values[i]}\n"
                      f"     Valeur d'achat : {my_df['ValeurAchat'].values[i]}\n"
                      f"     Valeur de vente : {my_df['ValeurVente'].values[i - 1]}")
        inc += 1

    #print(my_df.tail(10))
    print(f"A LA FIN (Date : {my_df.index[-1]}) :\n     PorteFeuille : {my_df['PorteFeuille'].values[-1]}\n"
          f"     Nbr Action(s) : {my_df['NbrAction'].values[-1]}\n"
          f"     Sécurisé : {my_df['Secu'].values[-1]}\n"
          f"     Mise : {my_df['Mise'].values[-1]}")

# Iteration sur l'année 2019 Scenario1
if bool_S1:
    # Rajout des valeurs specifiques
    my_df['Mise'] = 100.
    my_df['Secu'] = 0.
    my_df['PorteFeuille'] = 0.
    my_df['NbrAction'] = 0.
    my_df['Vente'] = False
    my_df['Achat'] = False
    my_df['ValeurAchat'] = np.NaN
    my_df['ValeurVente'] = np.NaN
    my_df['Scenario1'] = 0.

    # Initialisation du premier achat
    my_df['Mise'].values[0] = 0.
    my_df['PorteFeuille'].values[0] = nbr_action * my_df['Close'].values[0]
    my_df['NbrAction'].values[0] = nbr_action
    my_df['Achat'].values[0] = True
    my_df['ValeurAchat'].values[0] = valeur_action
    my_df['Scenario1'].values[0] = my_df['Mise'].values[0] + my_df['Secu'].values[0] + my_df['PorteFeuille'].values[0]
    vente = False
    achat = True
    inc = 0
    for i, my_ligne in enumerate(my_df.index):
        if i > 0:
            my_df['Mise'].values[i] = my_df['Mise'].values[i - 1]
            my_df['Secu'].values[i] = my_df['Secu'].values[i - 1]
            my_df['NbrAction'].values[i] = my_df['NbrAction'].values[i - 1]
            my_df['PorteFeuille'].values[i] = my_df['Close'].values[i] * my_df['NbrAction'].values[i]
            my_df['ValeurAchat'].values[i] = my_df['ValeurAchat'].values[i - 1]
            my_df['ValeurVente'].values[i] = my_df['ValeurVente'].values[i - 1]
            my_df['Scenario1'].values[i] = my_df['Mise'].values[i] + my_df['Secu'].values[i] + \
                                           my_df['PorteFeuille'].values[i]

        #print(my_df.iloc[i])
        if achat:  # On possède des actions
            # Regarde si vente
            if i > 5:
                # vente si diminution de l'action qui provoque diminution moyenne 2j, 3j, 4j et 7j (pente inf à -0,05) et
                # valeur plus basse qu'il y a 14j ou pente négative de plus de 0,8
                if not bool_pente('Close', i, my_df) and \
                        not bool_pente('J2', i, my_df) and \
                        not bool_pente('J3', i, my_df) and \
                        not bool_pente('J4', i, my_df) and \
                        not bool_pente('J7', i, my_df, -0.05) and \
                        (my_df['Close'].values[i] <= my_df['Close'].values[i - 10] or
                         not bool_pente('J2', i, my_df, -0.8)):
                    vente = True
                else:  # on ne vend pas
                    vente = False
        # print('Vente ?')
        if vente and achat:  # on va vendre, on ne possèdera plus d'action
            my_df['Vente'].values[i] = True
            my_df['Achat'].values[i] = False
            if my_df['Close'].values[i] * my_df['NbrAction'].values[i] > 100.:
                my_df['Mise'].values[i] = 100.
                my_df['Secu'].values[i] += my_df['Close'].values[i] * my_df['NbrAction'].values[i] - 100.
            else:
                my_df['Mise'].values[i] = my_df['Close'].values[i] * my_df['NbrAction'].values[i]
                my_df['Secu'].values[i] += 0.
            my_df['PorteFeuille'].values[i] = 0.
            my_df['NbrAction'].values[i] = 0.
            my_df['ValeurVente'].values[i] = my_df['Close'].values[i]
            my_df['ValeurAchat'].values[i] = np.NaN
            my_df['Scenario1'].values[i] = my_df['Mise'].values[i] + my_df['Secu'].values[i] + \
                                           my_df['PorteFeuille'].values[i]
            #print(my_df.iloc[i])
            print(f"VENTE (Date : {my_df.index[i]}) :\n     Mise : {my_df['Mise'].values[i]}\n"
                  f"     Sécurisé : {my_df['Secu'].values[i]}\n"
                  f"     Valeur d'achat : {my_df['ValeurAchat'].values[i - 1]}\n"
                  f"     Valeur de vente : {my_df['ValeurVente'].values[i]}")
            achat = False
        # print('achat ?')
        if vente and not achat and not my_df['Vente'].values[i] and not my_df['Achat'].values[i]:
            # On a vendu et pas encore racheté.
            # Conditions pour rachat:
            # La valeur de vente <= à la valeur de l'action et on n'a pas vendu le jour d'avant OU
            # La pente de l'action ainsi que J2 et J3 sont positives
            if my_df['ValeurVente'].values[i] <= my_df['Close'].values[i] and not my_df['Vente'].values[i - 1] \
                    or bool_pente('Close', i, my_df) and bool_pente('J2', i, my_df) and bool_pente('J3', i, my_df):
                my_df['Vente'].values[i] = False
                my_df['Achat'].values[i] = True
                achat = True
                vente = False
                my_df['Mise'].values[i] = 0.
                my_df['Secu'].values[i] = my_df['Secu'].values[i - 1]
                my_df['NbrAction'].values[i] = my_df['Mise'].values[i - 1] / my_df['Close'].values[i]
                my_df['PorteFeuille'].values[i] = my_df['Close'].values[i] * my_df['NbrAction'].values[i]
                my_df['ValeurAchat'].values[i] = my_df['Close'].values[i]
                my_df['ValeurVente'].values[i] = np.NaN
                my_df['Scenario1'].values[i] = my_df['Mise'].values[i] + my_df['Secu'].values[i] + \
                                               my_df['PorteFeuille'].values[i]
                #print(my_df.iloc[i])
                print(f"ACHAT (Date : {my_df.index[i]}) :\n     PorteFeuille : {my_df['PorteFeuille'].values[i]}\n"
                      f"     Sécurisé : {my_df['Secu'].values[i]}\n"
                      f"     Nbr Action(s) : {my_df['NbrAction'].values[i]}\n"
                      f"     Valeur d'achat : {my_df['ValeurAchat'].values[i]}\n"
                      f"     Valeur de vente : {my_df['ValeurVente'].values[i - 1]}")
        inc += 1

    #print(my_df.tail(10))
    print(f"A LA FIN (Date : {my_df.index[-1]}) :\n     PorteFeuille : {my_df['PorteFeuille'].values[-1]}\n"
          f"     Nbr Action(s) : {my_df['NbrAction'].values[-1]}\n"
          f"     Sécurisé : {my_df['Secu'].values[-1]}\n"
          f"     Mise : {my_df['Mise'].values[-1]}")

# Iteration sur l'année 2019 Rendement Max sans Sécurisation
if bool_Max_ssSecu:
    # Rajout des valeurs specifiques
    my_df['Mise'] = 100.
    my_df['Secu'] = 0.
    my_df['PorteFeuille'] = 0.
    my_df['NbrAction'] = 0.
    my_df['Vente'] = False
    my_df['Achat'] = False
    my_df['ValeurAchat'] = np.NaN
    my_df['ValeurVente'] = np.NaN
    my_df['MaxRendement_ssSecu'] = 0.

    # Initialisation du premier achat
    my_df['Mise'].values[0] = 0.
    my_df['PorteFeuille'].values[0] = nbr_action * my_df['Close'].values[0]
    my_df['NbrAction'].values[0] = nbr_action
    my_df['Achat'].values[0] = True
    my_df['ValeurAchat'].values[0] = valeur_action
    my_df['MaxRendement_ssSecu'].values[0] = my_df['Mise'].values[0] + my_df['Secu'].values[0] + my_df['PorteFeuille'].values[0]
    vente = False
    achat = True
    inc = 0
    for i, my_ligne in enumerate(my_df.index):
        if i > 0:
            my_df['Mise'].values[i] = my_df['Mise'].values[i - 1]
            my_df['Secu'].values[i] = my_df['Secu'].values[i - 1]
            my_df['NbrAction'].values[i] = my_df['NbrAction'].values[i - 1]
            my_df['PorteFeuille'].values[i] = my_df['Close'].values[i] * my_df['NbrAction'].values[i]
            my_df['ValeurAchat'].values[i] = my_df['ValeurAchat'].values[i - 1]
            my_df['ValeurVente'].values[i] = my_df['ValeurVente'].values[i - 1]
            my_df['MaxRendement_ssSecu'].values[i] = my_df['Mise'].values[i] + my_df['Secu'].values[i] + \
                                              my_df['PorteFeuille'].values[i]
        #print(my_df.iloc[i])
        if achat:  # On possède des actions
            # Regarde si vente
            if bool_pente('Close', i + 1, my_df):  # Pas de vente l'action augmente ou stagne
                vente = False
            else:  # on vend
                vente = True
        # print('Vente ?')
        if vente and achat:  # on va vendre, on ne possèdera plus d'action
            my_df['Vente'].values[i] = True
            my_df['Achat'].values[i] = False
            my_df['Mise'].values[i] = my_df['Close'].values[i] * my_df['NbrAction'].values[i]
            my_df['Secu'].values[i] += 0.
            my_df['PorteFeuille'].values[i] = 0.
            my_df['NbrAction'].values[i] = 0.
            my_df['ValeurVente'].values[i] = my_df['Close'].values[i]
            my_df['ValeurAchat'].values[i] = np.NaN
            my_df['MaxRendement_ssSecu'].values[i] = my_df['Mise'].values[i] + my_df['Secu'].values[i] + \
                                              my_df['PorteFeuille'].values[i]
            #print(my_df.iloc[i])
            print(f"VENTE (Date : {my_df.index[i]}) :\n     Mise : {my_df['Mise'].values[i]}\n"
                  f"     Sécurisé : {my_df['Secu'].values[i]}\n"
                  f"     Valeur d'achat : {my_df['ValeurAchat'].values[i - 1]}\n"
                  f"     Valeur de vente : {my_df['ValeurVente'].values[i]}")
            achat = False
        # print('achat ?')
        if vente and not achat and not my_df['Vente'].values[i] and not my_df['Achat'].values[i]:
            # On a vendu et pas encore racheté.
            # Conditions pour rachat
            if bool_pente('Close', i + 1, my_df):  # On achète, car remonté au niveau vente
                my_df['Vente'].values[i] = False
                my_df['Achat'].values[i] = True
                achat = True
                vente = False
                my_df['Mise'].values[i] = 0.
                my_df['Secu'].values[i] = my_df['Secu'].values[i - 1]
                my_df['NbrAction'].values[i] = my_df['Mise'].values[i - 1] / my_df['Close'].values[i]
                my_df['PorteFeuille'].values[i] = my_df['Close'].values[i] * my_df['NbrAction'].values[i]
                my_df['ValeurAchat'].values[i] = my_df['Close'].values[i]
                my_df['ValeurVente'].values[i] = np.NaN
                my_df['MaxRendement_ssSecu'].values[i] = my_df['Mise'].values[i] + my_df['Secu'].values[i] + \
                                                  my_df['PorteFeuille'].values[i]
                #print(my_df.iloc[i])
                print(f"ACHAT (Date : {my_df.index[i]}) :\n     PorteFeuille : {my_df['PorteFeuille'].values[i]}\n"
                      f"     Sécurisé : {my_df['Secu'].values[i]}\n"
                      f"     Nbr Action(s) : {my_df['NbrAction'].values[i]}\n"
                      f"     Valeur d'achat : {my_df['ValeurAchat'].values[i]}\n"
                      f"     Valeur de vente : {my_df['ValeurVente'].values[i - 1]}")
        inc += 1

    #print(my_df.tail(10))
    print(f"A LA FIN (Date : {my_df.index[-1]}) :\n     PorteFeuille : {my_df['PorteFeuille'].values[-1]}\n"
          f"     Nbr Action(s) : {my_df['NbrAction'].values[-1]}\n"
          f"     Sécurisé : {my_df['Secu'].values[-1]}\n"
          f"     Mise : {my_df['Mise'].values[-1]}")

# Iteration sur l'année 2019 Scenario1 sans Sécurisation
if bool_S1_ssSecu:
    # Rajout des valeurs specifiques
    my_df['Mise'] = 100.
    my_df['Secu'] = 0.
    my_df['PorteFeuille'] = 0.
    my_df['NbrAction'] = 0.
    my_df['Vente'] = False
    my_df['Achat'] = False
    my_df['ValeurAchat'] = np.NaN
    my_df['ValeurVente'] = np.NaN
    my_df['Scenario1_ssSecu'] = 0.

    # Initialisation du premier achat
    my_df['Mise'].values[0] = 0.
    my_df['PorteFeuille'].values[0] = nbr_action * my_df['Close'].values[0]
    my_df['NbrAction'].values[0] = nbr_action
    my_df['Achat'].values[0] = True
    my_df['ValeurAchat'].values[0] = valeur_action
    my_df['Scenario1_ssSecu'].values[0] = my_df['Mise'].values[0] + my_df['Secu'].values[0] + my_df['PorteFeuille'].values[0]
    vente = False
    achat = True
    inc = 0
    for i, my_ligne in enumerate(my_df.index):
        if i > 0:
            my_df['Mise'].values[i] = my_df['Mise'].values[i - 1]
            my_df['Secu'].values[i] = my_df['Secu'].values[i - 1]
            my_df['NbrAction'].values[i] = my_df['NbrAction'].values[i - 1]
            my_df['PorteFeuille'].values[i] = my_df['Close'].values[i] * my_df['NbrAction'].values[i]
            my_df['ValeurAchat'].values[i] = my_df['ValeurAchat'].values[i - 1]
            my_df['ValeurVente'].values[i] = my_df['ValeurVente'].values[i - 1]
            my_df['Scenario1_ssSecu'].values[i] = my_df['Mise'].values[i] + my_df['Secu'].values[i] + \
                                           my_df['PorteFeuille'].values[i]

        #print(my_df.iloc[i])
        if achat:  # On possède des actions
            # Regarde si vente
            if i > 5:
                # vente si diminution de l'action qui provoque diminution moyenne 2j, 3j, 4j et 7j (pente inf à -0,05) et
                # valeur plus basse qu'il y a 14j ou pente négative de plus de 0,8
                if not bool_pente('Close', i, my_df) and \
                        not bool_pente('J2', i, my_df) and \
                        not bool_pente('J3', i, my_df) and \
                        not bool_pente('J4', i, my_df) and \
                        not bool_pente('J7', i, my_df, -0.05) and \
                        (my_df['Close'].values[i] <= my_df['Close'].values[i - 10] or
                         not bool_pente('J2', i, my_df, -0.8)):
                    vente = True
                else:  # on ne vend pas
                    vente = False
        # print('Vente ?')
        if vente and achat:  # on va vendre, on ne possèdera plus d'action
            my_df['Vente'].values[i] = True
            my_df['Achat'].values[i] = False
            my_df['Mise'].values[i] = my_df['Close'].values[i] * my_df['NbrAction'].values[i]
            my_df['Secu'].values[i] += 0.
            my_df['PorteFeuille'].values[i] = 0.
            my_df['NbrAction'].values[i] = 0.
            my_df['ValeurVente'].values[i] = my_df['Close'].values[i]
            my_df['ValeurAchat'].values[i] = np.NaN
            my_df['Scenario1_ssSecu'].values[i] = my_df['Mise'].values[i] + my_df['Secu'].values[i] + \
                                           my_df['PorteFeuille'].values[i]
            #print(my_df.iloc[i])
            print(f"VENTE (Date : {my_df.index[i]}) :\n     Mise : {my_df['Mise'].values[i]}\n"
                  f"     Sécurisé : {my_df['Secu'].values[i]}\n"
                  f"     Valeur d'achat : {my_df['ValeurAchat'].values[i - 1]}\n"
                  f"     Valeur de vente : {my_df['ValeurVente'].values[i]}")
            achat = False
        # print('achat ?')
        if vente and not achat and not my_df['Vente'].values[i] and not my_df['Achat'].values[i]:
            # On a vendu et pas encore racheté.
            # Conditions pour rachat:
            # La valeur de vente <= à la valeur de l'action et on n'a pas vendu le jour d'avant OU
            # La pente de l'action ainsi que J2 et J3 sont positives
            if my_df['ValeurVente'].values[i] <= my_df['Close'].values[i] and not my_df['Vente'].values[i - 1] \
                    or bool_pente('Close', i, my_df) and bool_pente('J2', i, my_df) and bool_pente('J3', i, my_df):
                my_df['Vente'].values[i] = False
                my_df['Achat'].values[i] = True
                achat = True
                vente = False
                my_df['Mise'].values[i] = 0.
                my_df['Secu'].values[i] = my_df['Secu'].values[i - 1]
                my_df['NbrAction'].values[i] = my_df['Mise'].values[i - 1] / my_df['Close'].values[i]
                my_df['PorteFeuille'].values[i] = my_df['Close'].values[i] * my_df['NbrAction'].values[i]
                my_df['ValeurAchat'].values[i] = my_df['Close'].values[i]
                my_df['ValeurVente'].values[i] = np.NaN
                my_df['Scenario1_ssSecu'].values[i] = my_df['Mise'].values[i] + my_df['Secu'].values[i] + \
                                               my_df['PorteFeuille'].values[i]
                #print(my_df.iloc[i])
                print(f"ACHAT (Date : {my_df.index[i]}) :\n     PorteFeuille : {my_df['PorteFeuille'].values[i]}\n"
                      f"     Sécurisé : {my_df['Secu'].values[i]}\n"
                      f"     Nbr Action(s) : {my_df['NbrAction'].values[i]}\n"
                      f"     Valeur d'achat : {my_df['ValeurAchat'].values[i]}\n"
                      f"     Valeur de vente : {my_df['ValeurVente'].values[i - 1]}")
        inc += 1

    #print(my_df.tail(10))
    print(f"A LA FIN (Date : {my_df.index[-1]}) :\n     PorteFeuille : {my_df['PorteFeuille'].values[-1]}\n"
          f"     Nbr Action(s) : {my_df['NbrAction'].values[-1]}\n"
          f"     Sécurisé : {my_df['Secu'].values[-1]}\n"
          f"     Mise : {my_df['Mise'].values[-1]}")

# Iteration sur l'année 2019 Rendement Max Nbr Action Constante
if bool_Max_NbrActionCste:
    # Rajout des valeurs specifiques
    my_df['Mise'] = 100.
    my_df['Secu'] = 0.
    my_df['PorteFeuille'] = 0.
    my_df['NbrAction'] = 0.
    my_df['Vente'] = False
    my_df['Achat'] = False
    my_df['ValeurAchat'] = np.NaN
    my_df['ValeurVente'] = np.NaN
    my_df['MaxRendement_NbrActionCste'] = 0.

    # Initialisation du premier achat
    my_df['Mise'].values[0] = 0.
    my_df['PorteFeuille'].values[0] = nbr_action * my_df['Close'].values[0]
    my_df['NbrAction'].values[0] = nbr_action
    my_df['Achat'].values[0] = True
    my_df['ValeurAchat'].values[0] = valeur_action
    my_df['MaxRendement_NbrActionCste'].values[0] = my_df['Mise'].values[0] + my_df['Secu'].values[0] + my_df['PorteFeuille'].values[0]
    vente = False
    achat = True
    inc = 0
    for i, my_ligne in enumerate(my_df.index):
        if i > 0:
            my_df['Mise'].values[i] = my_df['Mise'].values[i - 1]
            my_df['Secu'].values[i] = my_df['Secu'].values[i - 1]
            my_df['NbrAction'].values[i] = my_df['NbrAction'].values[i - 1]
            my_df['PorteFeuille'].values[i] = my_df['Close'].values[i] * my_df['NbrAction'].values[i]
            my_df['ValeurAchat'].values[i] = my_df['ValeurAchat'].values[i - 1]
            my_df['ValeurVente'].values[i] = my_df['ValeurVente'].values[i - 1]
            my_df['MaxRendement_NbrActionCste'].values[i] = my_df['Mise'].values[i] + my_df['Secu'].values[i] + \
                                                            my_df['PorteFeuille'].values[i]
        #print(my_df.iloc[i])
        if achat:  # On possède des actions
            # Regarde si vente
            if bool_pente('Close', i + 1, my_df):  # Pas de vente l'action augmente ou stagne
                vente = False
            else:  # on vend
                vente = True
        # print('Vente ?')
        if vente and achat:  # on va vendre, on ne possèdera plus d'action
            my_df['Vente'].values[i] = True
            my_df['Achat'].values[i] = False
            my_df['Mise'].values[i] = my_df['Close'].values[i] * my_df['NbrAction'].values[i]
            my_df['Secu'].values[i] += 0.
            my_df['PorteFeuille'].values[i] = 0.
            my_df['NbrAction'].values[i] = 0.
            my_df['ValeurVente'].values[i] = my_df['Close'].values[i]
            my_df['ValeurAchat'].values[i] = np.NaN
            my_df['MaxRendement_NbrActionCste'].values[i] = my_df['Mise'].values[i] + my_df['Secu'].values[i] + \
                                                            my_df['PorteFeuille'].values[i]
            #print(my_df.iloc[i])
            print(f"VENTE (Date : {my_df.index[i]}) :\n     Mise : {my_df['Mise'].values[i]}\n"
                  f"     Sécurisé : {my_df['Secu'].values[i]}\n"
                  f"     Valeur d'achat : {my_df['ValeurAchat'].values[i - 1]}\n"
                  f"     Valeur de vente : {my_df['ValeurVente'].values[i]}")
            achat = False
        # print('achat ?')
        if vente and not achat and not my_df['Vente'].values[i] and not my_df['Achat'].values[i]:
            # On a vendu et pas encore racheté.
            # Conditions pour rachat
            if bool_pente('Close', i + 1, my_df):  # On achète, car remonté au niveau vente
                my_df['Vente'].values[i] = False
                my_df['Achat'].values[i] = True
                achat = True
                vente = False
                if my_df['Mise'].values[i] + my_df['Secu'].values[i] >= nbr_action * my_df['Close'].values[i]:
                    my_df['Secu'].values[i] = my_df['Mise'].values[i] + my_df['Secu'].values[i] - \
                                              (nbr_action * my_df['Close'].values[i])
                    my_df['Mise'].values[i] = 0.
                    my_df['NbrAction'].values[i] = nbr_action
                else:
                    my_df['NbrAction'].values[i] = (my_df['Mise'].values[i] + my_df['Secu'].values[i]) / \
                                                   my_df['Close'].values[i]
                    my_df['Secu'].values[i] = 0.
                    my_df['Mise'].values[i] = 0.
                my_df['PorteFeuille'].values[i] = my_df['Close'].values[i] * my_df['NbrAction'].values[i]
                my_df['ValeurAchat'].values[i] = my_df['Close'].values[i]
                my_df['ValeurVente'].values[i] = np.NaN
                my_df['MaxRendement_NbrActionCste'].values[i] = my_df['Mise'].values[i] + my_df['Secu'].values[i] + \
                                                                my_df['PorteFeuille'].values[i]
                #print(my_df.iloc[i])
                print(f"ACHAT (Date : {my_df.index[i]}) :\n     PorteFeuille : {my_df['PorteFeuille'].values[i]}\n"
                      f"     Sécurisé : {my_df['Secu'].values[i]}\n"
                      f"     Nbr Action(s) : {my_df['NbrAction'].values[i]}\n"
                      f"     Valeur d'achat : {my_df['ValeurAchat'].values[i]}\n"
                      f"     Valeur de vente : {my_df['ValeurVente'].values[i - 1]}")
        inc += 1

    #print(my_df.tail(10))
    print(f"A LA FIN (Date : {my_df.index[-1]}) :\n     PorteFeuille : {my_df['PorteFeuille'].values[-1]}\n"
          f"     Nbr Action(s) : {my_df['NbrAction'].values[-1]}\n"
          f"     Sécurisé : {my_df['Secu'].values[-1]}\n"
          f"     Mise : {my_df['Mise'].values[-1]}")

# Iteration sur l'année 2019 Scenario1 Nbr Action Constante
if bool_S1_NbrActionCste:
    # Rajout des valeurs specifiques
    my_df['Mise'] = 100.
    my_df['Secu'] = 0.
    my_df['PorteFeuille'] = 0.
    my_df['NbrAction'] = 0.
    my_df['Vente'] = False
    my_df['Achat'] = False
    my_df['ValeurAchat'] = np.NaN
    my_df['ValeurVente'] = np.NaN
    my_df['Scenario1_NbrActionCste'] = 0.

    # Initialisation du premier achat
    my_df['Mise'].values[0] = 0.
    my_df['PorteFeuille'].values[0] = nbr_action * my_df['Close'].values[0]
    my_df['NbrAction'].values[0] = nbr_action
    my_df['Achat'].values[0] = True
    my_df['ValeurAchat'].values[0] = valeur_action
    my_df['Scenario1_NbrActionCste'].values[0] = my_df['Mise'].values[0] + my_df['Secu'].values[0] + \
                                                 my_df['PorteFeuille'].values[0]
    vente = False
    achat = True
    inc = 0
    for i, my_ligne in enumerate(my_df.index):
        if i > 0:
            my_df['Mise'].values[i] = my_df['Mise'].values[i - 1]
            my_df['Secu'].values[i] = my_df['Secu'].values[i - 1]
            my_df['NbrAction'].values[i] = my_df['NbrAction'].values[i - 1]
            my_df['PorteFeuille'].values[i] = my_df['Close'].values[i] * my_df['NbrAction'].values[i]
            my_df['ValeurAchat'].values[i] = my_df['ValeurAchat'].values[i - 1]
            my_df['ValeurVente'].values[i] = my_df['ValeurVente'].values[i - 1]
            my_df['Scenario1_NbrActionCste'].values[i] = my_df['Mise'].values[i] + my_df['Secu'].values[i] + \
                                                         my_df['PorteFeuille'].values[i]

        #print(my_df.iloc[i])
        if achat:  # On possède des actions
            # Regarde si vente
            if i > 5:
                # vente si diminution de l'action qui provoque diminution moyenne 2j, 3j, 4j et 7j (pente inf à -0,05) et
                # valeur plus basse qu'il y a 14j ou pente négative de plus de 0,8
                if not bool_pente('Close', i, my_df) and \
                        not bool_pente('J2', i, my_df) and \
                        not bool_pente('J3', i, my_df) and \
                        not bool_pente('J4', i, my_df) and \
                        not bool_pente('J7', i, my_df, -0.05) and \
                        (my_df['Close'].values[i] <= my_df['Close'].values[i - 10] or
                         not bool_pente('J2', i, my_df, -0.8)):
                    vente = True
                else:  # on ne vend pas
                    vente = False
        # print('Vente ?')
        if vente and achat:  # on va vendre, on ne possèdera plus d'action
            my_df['Vente'].values[i] = True
            my_df['Achat'].values[i] = False
            my_df['Mise'].values[i] = my_df['Close'].values[i] * my_df['NbrAction'].values[i]
            my_df['Secu'].values[i] += 0.
            my_df['PorteFeuille'].values[i] = 0.
            my_df['NbrAction'].values[i] = 0.
            my_df['ValeurVente'].values[i] = my_df['Close'].values[i]
            my_df['ValeurAchat'].values[i] = np.NaN
            my_df['Scenario1_NbrActionCste'].values[i] = my_df['Mise'].values[i] + my_df['Secu'].values[i] + \
                                                         my_df['PorteFeuille'].values[i]
            #print(my_df.iloc[i])
            print(f"VENTE (Date : {my_df.index[i]}) :\n     Mise : {my_df['Mise'].values[i]}\n"
                  f"     Sécurisé : {my_df['Secu'].values[i]}\n"
                  f"     Valeur d'achat : {my_df['ValeurAchat'].values[i - 1]}\n"
                  f"     Valeur de vente : {my_df['ValeurVente'].values[i]}")
            achat = False
        # print('achat ?')
        if vente and not achat and not my_df['Vente'].values[i] and not my_df['Achat'].values[i]:
            # On a vendu et pas encore racheté.
            # Conditions pour rachat:
            # La valeur de vente <= à la valeur de l'action et on n'a pas vendu le jour d'avant OU
            # La pente de l'action ainsi que J2 et J3 sont positives
            if my_df['ValeurVente'].values[i] <= my_df['Close'].values[i] and not my_df['Vente'].values[i - 1] \
                    or bool_pente('Close', i, my_df) and bool_pente('J2', i, my_df) and bool_pente('J3', i, my_df):
                my_df['Vente'].values[i] = False
                my_df['Achat'].values[i] = True
                achat = True
                vente = False
                if my_df['Mise'].values[i] + my_df['Secu'].values[i] >= nbr_action * my_df['Close'].values[i]:
                    my_df['Secu'].values[i] = my_df['Mise'].values[i] + my_df['Secu'].values[i] - \
                                              (nbr_action * my_df['Close'].values[i])
                    my_df['Mise'].values[i] = 0.
                    my_df['NbrAction'].values[i] = nbr_action
                else:
                    my_df['NbrAction'].values[i] = (my_df['Mise'].values[i] + my_df['Secu'].values[i]) / \
                                                   my_df['Close'].values[i]
                    my_df['Secu'].values[i] = 0.
                    my_df['Mise'].values[i] = 0.
                my_df['PorteFeuille'].values[i] = my_df['Close'].values[i] * my_df['NbrAction'].values[i]
                my_df['ValeurAchat'].values[i] = my_df['Close'].values[i]
                my_df['ValeurVente'].values[i] = np.NaN
                my_df['Scenario1_NbrActionCste'].values[i] = my_df['Mise'].values[i] + my_df['Secu'].values[i] + \
                                                             my_df['PorteFeuille'].values[i]
                #print(my_df.iloc[i])
                print(f"ACHAT (Date : {my_df.index[i]}) :\n     PorteFeuille : {my_df['PorteFeuille'].values[i]}\n"
                      f"     Sécurisé : {my_df['Secu'].values[i]}\n"
                      f"     Nbr Action(s) : {my_df['NbrAction'].values[i]}\n"
                      f"     Valeur d'achat : {my_df['ValeurAchat'].values[i]}\n"
                      f"     Valeur de vente : {my_df['ValeurVente'].values[i - 1]}")
        inc += 1

    #print(my_df.tail(10))
    print(f"A LA FIN (Date : {my_df.index[-1]}) :\n     PorteFeuille : {my_df['PorteFeuille'].values[-1]}\n"
          f"     Nbr Action(s) : {my_df['NbrAction'].values[-1]}\n"
          f"     Sécurisé : {my_df['Secu'].values[-1]}\n"
          f"     Mise : {my_df['Mise'].values[-1]}")

my_df.to_csv(r'/Users/stephanecau/PycharmProjects/StecauApps/FinancialApp/'
             r'simu_rapide.csv', index=True)

# Visualisation
fig, ax = plt.subplots(figsize=(16, 9))
ax.plot(my_df.index, my_df['Close'], label='Action Apple')
#ax.plot(my_df.index, my_df['Mise'], label='Evolution de la mise')
#ax.plot(my_df.index, my_df['Secu'], label='Evolution de la Sécurisation')
#ax.plot(my_df.index, my_df['PorteFeuille'], label='Evolution du PorteFeuille')
#ax.plot(my_df.index, my_df['NbrAction'], label="Evolution du nombre d'actions")
ax.plot(my_df.index, my_df['SansTransaction'], label='Evolution du Total Sans Transaction')
if bool_Max:
    ax.plot(my_df.index, my_df['MaxRendement'], label='Evolution du Total Rendement Max')
if bool_Max_ssSecu:
    ax.plot(my_df.index, my_df['MaxRendement_ssSecu'], label='Evolution du Total Rendement Max sans sécurisation')
if bool_Max_NbrActionCste:
    ax.plot(my_df.index, my_df['MaxRendement_NbrActionCste'], label='Evolution du Total Rendement Max '
                                                                    'avec Nbr Action cste')
if bool_S1:
    ax.plot(my_df.index, my_df['Scenario1'], label='Evolution du Total Scenario1')
if bool_S1_ssSecu:
    ax.plot(my_df.index, my_df['Scenario1_ssSecu'], label='Evolution du Total Scenario1 sans sécurisation')
if bool_S1_NbrActionCste:
    ax.plot(my_df.index, my_df['Scenario1_NbrActionCste'], label='Evolution du Scenario1 avec Nbr Action cste')
ax.set_xlabel('Date')
ax.set_ylabel('Valeur de fermeture')
ax.legend()
plt.show()
