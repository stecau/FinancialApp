# Import des modules
import copy
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


def bool_comparison(label, index, dataframe, delta_index):
    if dataframe[label].values[index] <= dataframe[label].values[index - delta_index]:
        return True
    return False


def generation_listing_models(**kwargs):
    l_models = list()
    longueur_tableau_init = 0
    for position, key in enumerate(kwargs.keys()):
        for sub_position, sub_key in enumerate(kwargs[key].keys()):
            if key == 'pente' or key == 'comparaison':
                for inc_valeur, valeur in enumerate(kwargs[key][sub_key]):
                    # Remplissage du premier jeu de données
                    if position + sub_position + inc_valeur == 0:
                        l_models.append(copy.deepcopy(kwargs))
                        l_models[position + sub_position + inc_valeur][key][sub_key] = valeur
                        #print(str(l_models))
                    elif inc_valeur > 0 and position + sub_position + inc_valeur == inc_valeur:
                        l_models.append(copy.deepcopy(l_models[-1]))
                        l_models[position + sub_position + inc_valeur][key][sub_key] = valeur
                        #print(str(l_models))
                    # Duplication des données pour variable suivante
                    if inc_valeur < len(kwargs[key][sub_key]) - 1 and \
                            not position + sub_position + inc_valeur == inc_valeur:
                        #print(f"longueur_tableau_init = {longueur_tableau_init}")
                        if inc_valeur == 0:
                            longueur_tableau_init = len(l_models)
                        #print(f"longueur_tableau_init = {longueur_tableau_init}")
                        for inc in range(inc_valeur * longueur_tableau_init, len(l_models), 1):
                            l_models[inc][key][sub_key] = valeur
                            l_models.append(copy.deepcopy(l_models[inc]))
                            #print("copie")
                            #print(f"inc = {inc}")
                            #print(f"valeur = {valeur}")
                            #print(str(l_models))
                    elif inc_valeur == len(kwargs[key][sub_key]) - 1 and \
                            not position + sub_position + inc_valeur == inc_valeur:
                        #print(f"longueur_tableau_init = {longueur_tableau_init}")
                        for inc in range(inc_valeur * longueur_tableau_init, len(l_models), 1):
                            l_models[inc][key][sub_key] = valeur
                            #print("deuxième")
                            #print(f"inc = {inc}")
                            #print(f"valeur = {valeur}")
                            #print(str(l_models))
                    #print("Fin boucle : " + str(l_models))
            else:
                for subsub_position, subsub_key in enumerate(kwargs[key][sub_key].keys()):
                    for inc_valeur, valeur in enumerate(kwargs[key][sub_key][subsub_key]):
                        # Remplissage du premier jeu de données
                        if position + sub_position + subsub_position + inc_valeur == 0:
                            l_models.append(copy.deepcopy(kwargs))
                            l_models[position + sub_position + subsub_position + inc_valeur][key][sub_key][subsub_key] = valeur
                            #print(str(l_models))
                        elif inc_valeur > 0 and position + sub_position + subsub_position + inc_valeur == inc_valeur:
                            l_models.append(copy.deepcopy(l_models[-1]))
                            l_models[position + sub_position + subsub_position + inc_valeur][key][sub_key][subsub_key] = valeur
                            #print(str(l_models))
                        # Duplication des données pour variable suivante
                        if inc_valeur < len(kwargs[key][sub_key][subsub_key]) - 1 and \
                                not position + sub_position + subsub_position + inc_valeur == inc_valeur:
                            #print(f"longueur_tableau_init = {longueur_tableau_init}")
                            if inc_valeur == 0:
                                longueur_tableau_init = len(l_models)
                            #print(f"longueur_tableau_init = {longueur_tableau_init}")
                            for inc in range(inc_valeur * longueur_tableau_init, len(l_models), 1):
                                l_models[inc][key][sub_key][subsub_key] = valeur
                                l_models.append(copy.deepcopy(l_models[inc]))
                                #print("copie")
                                #print(f"inc = {inc}")
                                #print(f"valeur = {valeur}")
                                #print(str(l_models))
                        elif inc_valeur == len(kwargs[key][sub_key][subsub_key]) - 1 and \
                                not position + sub_position + subsub_position + inc_valeur == inc_valeur:
                            #print(f"longueur_tableau_init = {longueur_tableau_init}")
                            for inc in range(inc_valeur * longueur_tableau_init, len(l_models), 1):
                                l_models[inc][key][sub_key][subsub_key] = valeur
                                #print("deuxième")
                                #print(f"inc = {inc}")
                                #print(f"valeur = {valeur}")
                                #print(str(l_models))
                        #print("Fin boucle : " + str(l_models))
    return l_models


def bool_vente_scenario(index, dataframe, **kwargs):
    l_bool = list()
    #print(f"kwargs = {kwargs}")
    for key, value in kwargs.items():
        #print(f"key = {key},\nvalue = {value}")
        # if key == "pente": value => dico {'pente_key': [False, -1., -0.5, 0., 0.5, 1.]} par exemple
        # if key == "comparaison": value => dico {'data_to_compare': [False, delta_index1, delta_index2]} par exemple
        if key == "pente" or key == "comparaison":
            for data_key, data_value in value.items():
                #print(f"data_key = {data_key},\ndata_value = {data_value}")
                l_bool.append(bool_vente_scenario_type(index, dataframe, data_key, data_value, key))
        if key == "pente+comp":
            l_subBool = list()
            for penteComp_key, penteComp_value in value.items():
                for data_key, data_value in penteComp_value.items():
                    l_subBool.append(bool_vente_scenario_type(index, dataframe, data_key, data_value, penteComp_key))
            print(f"l_subBool : {l_subBool}")
            if True in l_subBool:
                l_bool.append(True)
            else:
                l_bool.append(False)
        #print(f"l_bool : {l_bool}")
        #print(f"l_bool.count(True) : {l_bool.count(True)}")
        #print(f"len(l_bool) : {len(l_bool)}")
        if 0 < l_bool.count(None) < len(l_bool):
            # Suppression des 'None' sauf si que des 'None' (car renvoie True sinon)
            while None in l_bool:
                l_bool.remove(None)
        #print(f"l_bool : {l_bool}")
        #print(f"l_bool.count(True) : {l_bool.count(True)}")
        #print(f"len(l_bool) : {len(l_bool)}")
        if len(l_bool) == l_bool.count(True):
            return True
        else:
            return False


def bool_vente_scenario_type(index, dataframe, data_key, data_value, data_type):
    if data_type == "pente":
        if not isinstance(data_value, bool):
            #print(f"key={data_key},\nindex={index},\ndataframe ,\nvalue={data_value}")
            #print(f"not bool_pente(key={data_key}, index={index}, dataframe , value={data_value}) = "
            #      f"{not bool_pente(data_key, index, dataframe, data_value)}")
            return not bool_pente(data_key, index, dataframe, data_value)
    if data_type == "comp":
        if not isinstance(data_value, bool):
            print(f"key={data_key},\nindex={index},\ndataframe ,\nvalue={data_value}")
            print(f"bool_comparison(key={data_key}, index={index}, dataframe , value={data_value}) = "
                  f"{bool_comparison(data_key, index, dataframe, data_value)}")
            return bool_comparison(data_key, index, dataframe, data_value)
    #     if not bool_pente('Close', i, my_df) and \
    #             not bool_pente('J2', i, my_df) and \
    #             not bool_pente('J3', i, my_df) and \
    #             not bool_pente('J4', i, my_df) and \
    #             not bool_pente('J7', i, my_df, -0.05) and \
    #             (my_df['Close'].values[i] <= my_df['Close'].values[i - 10] or
    #              not bool_pente('J2', i, my_df, -0.8)):
    #         vente = True
    #     else:  # on ne vend pas
    #         vente = False


def bool_achat_scenario(index, dataframe, **kwargs):
    l_bool = list()
    #print(f"kwargs = {kwargs}")
    for key, value in kwargs.items():
        #print(f"key = {key},\nvalue = {value}")
        # if key == "pente": value => dico {'pente_key': [False, -1., -0.5, 0., 0.5, 1.]} par exemple
        # if key == "comparaison": value => dico {'data_to_compare': [False, delta_index1, delta_index2]} par exemple
        if key == "pente" or key == "comparaison":
            for data_key, data_value in value.items():
                #print(f"data_key = {data_key},\ndata_value = {data_value}")
                l_bool.append(bool_achat_scenario_type(index, dataframe, data_key, data_value, key))
        if key == "pente+comp":
            l_subBool = list()
            for penteComp_key, penteComp_value in value.items():
                for data_key, data_value in penteComp_value.items():
                    l_subBool.append(bool_achat_scenario_type(index, dataframe, data_key, data_value, penteComp_key))
            print(f"l_subBool : {l_subBool}")
            if True in l_subBool:
                l_bool.append(True)
            else:
                l_bool.append(False)
        #print(f"l_bool : {l_bool}")
        #print(f"l_bool.count(True) : {l_bool.count(True)}")
        #print(f"len(l_bool) : {len(l_bool)}")
        if 0 < l_bool.count(None) < len(l_bool):
            # Suppression des 'None' sauf si que des 'None' (car renvoie True sinon)
            while None in l_bool:
                l_bool.remove(None)
        #print(f"l_bool : {l_bool}")
        #print(f"l_bool.count(True) : {l_bool.count(True)}")
        #print(f"len(l_bool) : {len(l_bool)}")
        if len(l_bool) == l_bool.count(True):
            return True
        else:
            return False


def bool_achat_scenario_type(index, dataframe, data_key, data_value, data_type):
    if data_type == "pente":
        if not isinstance(data_value, bool):
            #print(f"key={data_key},\nindex={index},\ndataframe ,\nvalue={data_value}")
            #print(f"not bool_pente(key={data_key}, index={index}, dataframe , value={data_value}) = "
            #      f"{not bool_pente(data_key, index, dataframe, data_value)}")
            return bool_pente(data_key, index, dataframe, data_value)
    if data_type == "comp":
        if not isinstance(data_value, bool):
            print(f"key={data_key},\nindex={index},\ndataframe ,\nvalue={data_value}")
            print(f"bool_comparison(key={data_key}, index={index}, dataframe , value={data_value}) = "
                  f"{bool_comparison(data_key, index, dataframe, data_value)}")
            return bool_comparison(data_key, index, dataframe, data_value)
    # if my_df['ValeurVente'].values[i] <= my_df['Close'].values[i] and not my_df['Vente'].values[i - 1] \
    #         or bool_pente('Close', i, my_df) and bool_pente('J2', i, my_df) and \
    #         bool_pente('J3', i, my_df):


# Simulation achat/vente sur 2019
date_debut = dt.datetime(2020, 1, 7)
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

# calcul des pentes max et min pour l'action et les moyennes
dico_extremum = {}
dico_loiNormale = {}
dico_vente = {"pente": dict()}
dico_achat = {"pente": dict()}
for value in ["Close", "J2", "J3", "J4", "J5", "J6", "J7"]:
    df_hist = pd.DataFrame(data=my_df[value] - my_df[value].shift())
    median_column = df_hist[value]
    median_column.plot(kind="hist")
    #plt.show()
    dico_extremum[value] = {"Max": float(pd.DataFrame(data=my_df[value] - my_df[value].shift()).max(0).values),
                            "Min": float(pd.DataFrame(data=my_df[value] - my_df[value].shift()).min(0).values)}
    dico_loiNormale[value] = {"Moy": float(pd.DataFrame(data=my_df[value] - my_df[value].shift()).mean(axis=0).values),
                              "Sig": float(pd.DataFrame(data=my_df[value] - my_df[value].shift()).std(axis=0).values)}
    if value == "Close":
        dico_vente["pente"][value] = [dico_loiNormale[value]["Moy"] - 1.2 * dico_loiNormale[value]["Sig"]]
    if value == "J3":
        dico_vente["pente"][value] = [dico_loiNormale[value]["Moy"] - 1.3 * dico_loiNormale[value]["Sig"]]
    if value == "J6":
        dico_vente["pente"][value] = [dico_loiNormale[value]["Moy"] - 1.2 * dico_loiNormale[value]["Sig"]]
        # dico_vente["pente"][value] = [False,
        #                               dico_loiNormale[value]["Moy"] - 3 * dico_loiNormale[value]["Sig"],
        #                               dico_loiNormale[value]["Moy"] - 2 * dico_loiNormale[value]["Sig"],
        #                               dico_loiNormale[value]["Moy"] - 1 * dico_loiNormale[value]["Sig"],
        #                               dico_loiNormale[value]["Moy"] - 0.5 * dico_loiNormale[value]["Sig"],
        #                               dico_loiNormale[value]["Moy"],
        #                               dico_loiNormale[value]["Moy"] + 0.5 * dico_loiNormale[value]["Sig"],
        #                               dico_loiNormale[value]["Moy"] + 1 * dico_loiNormale[value]["Sig"],
        #                               dico_loiNormale[value]["Moy"] + 2 * dico_loiNormale[value]["Sig"],
        #                               dico_loiNormale[value]["Moy"] + 3 * dico_loiNormale[value]["Sig"],
        #                               ]

    # elif value == "J3" or value == "J4" or value == "J5" or value == "J6": # or value == "J7":
    #     dico_vente["pente"][value] = [False, dico_loiNormale[value]["Moy"] - dico_loiNormale[value]["Sig"],
    #                                   dico_loiNormale[value]["Moy"],
    #                                   dico_loiNormale[value]["Moy"] + dico_loiNormale[value]["Sig"]]
    if value == "J4":
        dico_achat["pente"][value] = [dico_loiNormale[value]["Moy"]]
    if value == "J5":
        dico_achat["pente"][value] = [dico_loiNormale[value]["Moy"] - dico_loiNormale[value]["Sig"]]
    print(dico_loiNormale)
print(dico_extremum)
print(dico_loiNormale)
print(dico_vente)

# Rajout des valeurs specifiques
my_df['SansTransaction'] = nbr_action * my_df['Close']
df_final = pd.DataFrame()

#print(my_df.head(5))
#print(my_df.tail(5))

# Initialisation lancement Scenario
bool_Max = False
bool_Max_ssSecu = False
bool_Max_NbrActionCste = False
bool_S1 = True
bool_S1_ssSecu = False
bool_S1_NbrActionCste = False

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

# Iteration sur l'année 2019 Scenario1
if bool_S1:
    # Variables de génération des scenarii
    l_list_test = [False, -0.5, 0., 0.5]

    # dico_vente = {
    #     "pente": {
    #         #"J2": [-1.5, -1.05, -0.5],
    #         #"J6": [-0.1, -0.025, 0.05]
    #         "Close": [False, -1., -0.5, 0.],
    #         "J2": [False, -0.5, 0., 0.5],
    #         "J3": [False, -0.5, 0., 0.5],
    #         "J4": [False, -0.5, 0., 0.5],
    #         "J5": [False, -0.5, 0., 0.5],
    #         "J6": [False, -0.5, 0., 0.5],
    #         "J7": [False, -0.5, 0., 0.5]
        # "pente": {
        #     "Close": [False, -1., -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.,
        #               0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.],
        #     "J2": [False, -1., -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.,
        #            0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.],
        #     "J3": [False, -1., -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.,
        #            0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.],
        #     "J4": [False, -1., -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.,
        #            0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.],
        #     "J5": [False, -1., -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.,
        #            0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.],
        #     "J6": [False, -1., -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.,
        #            0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.],
        #     "J7": [False, -1., -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.,
        #            0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.]
        # },
        # "comparaison": {
        #     "Close": [False, 10],
        #     "J2": [False, 5, 10]
        # },
        # "pente+comp": {
        #     "pente": {
        #         "Close": [False, -1., -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.,
        #                   0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.],
        #         "J2": [False, -1., -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.,
        #                0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.],
        #         "J3": [False, -1., -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.,
        #                0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.],
        #         "J4": [False, -1., -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.,
        #                0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.],
        #         "J5": [False, -1., -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.,
        #                0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.],
        #         "J6": [False, -1., -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.,
        #                0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.],
        #         "J7": [False, -1., -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.,
        #                0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.]
        #     },
        #     "comparaison": {
        #         "Close": [False, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        #         "J2": [False, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        #         "J3": [False, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        #         "J4": [False, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        #         "J5": [False, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        #         "J6": [False, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        #         "J7": [False, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        #     },
        # }
    # }
    # dico_achat = {
    #     "pente": {
    #         "Close": [False]  #, dico_loiNormale["Close"]["Moy"] - 0.5 * dico_loiNormale[value]["Sig"]],
    #         #"J2": [False, -2., -1., -0.5, 0., 0.5, 1., 2.],
    #         #"J3": [False, -2., -1., -0.5, 0., 0.5, 1., 2.],
    #         #"J4": [False, -2., -1., -0.5, 0., 0.5, 1., 2.],
    #         #"J5": [False, -2., -1., -0.5, 0., 0.5, 1., 2.],
    #         #"J6": [False, -2., -1., -0.5, 0., 0.5, 1., 2.],
    #         #"J7": [False, -2., -1., -0.5, 0., 0.5, 1., 2.],
    #     }
    # }
    # Generation listing models
    l_models_vente = generation_listing_models(**dico_vente)
    print(f"Nombre de modèle = {str(len(l_models_vente))}")
    l_models_achat = generation_listing_models(**dico_achat)
    print(f"Nombre de modèle = {str(len(l_models_achat))}")

    nbr_S = - 1
    for model_vente in l_models_vente:
        for model_achat in l_models_achat:
            nbr_S += 1
            # Rajout des valeurs specifiques
            my_df['Mise'] = 100.
            my_df['Secu'] = 0.
            my_df['PorteFeuille'] = 0.
            my_df['NbrAction'] = 0.
            my_df['Vente'] = False
            my_df['Achat'] = False
            my_df['ValeurAchat'] = np.NaN
            my_df['ValeurVente'] = np.NaN
            my_df['Scenario'] = 0.

            # Initialisation du premier achat
            my_df['Mise'].values[0] = 0.
            my_df['PorteFeuille'].values[0] = nbr_action * my_df['Close'].values[0]
            my_df['NbrAction'].values[0] = nbr_action
            my_df['Achat'].values[0] = True
            my_df['ValeurAchat'].values[0] = valeur_action
            my_df['Scenario'].values[0] = my_df['Mise'].values[0] + my_df['Secu'].values[0] + \
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
                    my_df['Scenario'].values[i] = my_df['Mise'].values[i] + my_df['Secu'].values[i] + \
                                                                my_df['PorteFeuille'].values[i]

                #print(my_df.iloc[i])
                if achat:  # On possède des actions
                    # Regarde si vente
                    if i > 5:
                        # vente si diminution de l'action qui provoque diminution moyenne 2j, 3j, 4j et 7j (pente inf à -0,05) et
                        # valeur plus basse qu'il y a 14j ou pente négative de plus de 0,8
                        #print("Appel à la fonction pour vente")
                        if bool_vente_scenario(i, my_df, **model_vente):
                            vente = True
                        else:  # on ne vend pas
                            vente = False
                        #print(f"vente = {vente}")
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
                    my_df['Scenario'].values[i] = my_df['Mise'].values[i] + my_df['Secu'].values[i] + \
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
                    # if my_df['ValeurVente'].values[i] <= my_df['Close'].values[i] and not my_df['Vente'].values[i - 1] \
                    #         or bool_pente('Close', i, my_df) and bool_pente('J2', i, my_df) and \
                    #         bool_pente('J3', i, my_df):
                    if bool_achat_scenario(i, my_df, **model_achat) or \
                            (my_df['ValeurVente'].values[i] <= my_df['Close'].values[i] and
                             not my_df['Vente'].values[i - 1]):
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
                        my_df['Scenario'].values[i] = my_df['Mise'].values[i] + my_df['Secu'].values[i] + \
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

            # Stockage info de dataframe principal
            l_columns = list()
            l_values = list()
            l_values.append(list())
            # Param Vente
            for key, value in model_vente.items():
                if key == "pente" or key =="comparaison":
                    for sub_key, sub_value in value.items():
                        l_columns.append("Vente_" + key + "_" + sub_key)
                        l_values[0].append(sub_value)
                else:
                    for sub_key, sub_value in value.items():
                        for subsub_key, subsub_value in sub_value.items():
                            l_columns.append("Vente_" + key + "_" + sub_key + "_" + subsub_key)
                            l_values[0].append(subsub_value)
            # Param Achat
            for key, value in model_achat.items():
                if key == "pente" or key =="comparaison":
                    for sub_key, sub_value in value.items():
                        l_columns.append("Achat_" + key + "_" + sub_key)
                        l_values[0].append(sub_value)
                else:
                    for sub_key, sub_value in value.items():
                        for subsub_key, subsub_value in sub_value.items():
                            l_columns.append("Achat_" + key + "_" + sub_key + "_" + subsub_key)
                            l_values[0].append(subsub_value)
            # Rajout du total
            l_columns.append('Total')
            l_values[0].append(my_df['Scenario'].values[-1])
            #print(l_columns)
            #print(l_values)
            df_tempo = pd.DataFrame(data=l_values, index=['Scenario_' + str(nbr_S)], columns=l_columns)
            #print(df_tempo)
            df_final = df_final.append(df_tempo, ignore_index=False)
            #print(df_final)

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
             r'simu_surrogate.csv', index=True)

df_final.to_csv(r'/Users/stephanecau/PycharmProjects/StecauApps/FinancialApp/'
             r'simu_surrogate_sumup.csv', index=True)

# Visualisation
if 0:
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
        for num in range(0, nbr_S + 1, 1):
            ax.plot(my_df.index, my_df['Scenario_' + str(num)], label='Evolution du Total Scenario ' + str(num))
    if bool_S1_ssSecu:
        ax.plot(my_df.index, my_df['Scenario1_ssSecu'], label='Evolution du Total Scenario1 sans sécurisation')
    if bool_S1_NbrActionCste:
        ax.plot(my_df.index, my_df['Scenario1_NbrActionCste'], label='Evolution du Scenario1 avec Nbr Action cste')
    ax.set_xlabel('Date')
    ax.set_ylabel('Valeur de fermeture')
    ax.legend()
    plt.show()

if 1:
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.plot(df_final.index, df_final['Total'], label='Resultats scenarii')
    #ax.plot(my_df.index, my_df['Mise'], label='Evolution de la mise')
    #ax.plot(my_df.index, my_df['Secu'], label='Evolution de la Sécurisation')
    #ax.plot(my_df.index, my_df['PorteFeuille'], label='Evolution du PorteFeuille')
    #ax.plot(my_df.index, my_df['NbrAction'], label="Evolution du nombre d'actions")
    #ax.plot(my_df.index, my_df['SansTransaction'], label='Evolution du Total Sans Transaction')
    ax.set_xlabel('Scenarii')
    ax.set_ylabel('Valeur du résultats final')
    ax.legend()
    plt.show()

    # ## DataFrame from 2D-arrays
    # x_achat = X.reshape(1600)
    # y_vente = Y.reshape(1600)
    # z_resultats = df_final['Total']
    # df_plot = pd.DataFrame({'x': x, 'y': y, 'z': z}, index=range(len(x)))
    #
    # # Plot using `.trisurf()`:
    #
    # ax.plot_trisurf(df.x, df.y, df.z, cmap=cm.jet, linewidth=0.2)
    # plt.show()