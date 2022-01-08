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
    #print(f"dataframe = \n{dataframe}")
    if index <= len(dataframe.index) - 1:
        pente = (dataframe[label].values[index] - dataframe[label].values[index - 1]) / (index - (index - 1))
        #print(f'pente : {pente}')
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


# Initialisation lancement Scenario
bool_Max = True
bool_Max_ssSecu = False
bool_Max_NbrActionCste = False
bool_S1 = True
bool_S1_ssSecu = False
bool_S1_NbrActionCste = False
dico_mem = dict()

for jour in range(0, 30, 1):
    # Simulation achat/vente sur 2019
    date_debut = dt.datetime(2019, 1, 7)
    df = web.DataReader('AAPL', 'yahoo', date_debut,
                        date_debut + dt.timedelta(days=+360 + jour))
    #print(df)
    if jour == 0:
        valeur_action = float(df['Close'].values[-1])
        mise_depart = 100.  # euros
        # Achat d'action au 2 Janvier 2020
        nbr_action = mise_depart / valeur_action
        print(f"Au {df.index[-1]}")
        print('valeur_action : ', valeur_action)
        print('nbr_action : ', nbr_action)

    #print(f"df.index[-1] = {df.index[-1]}")
    #print(f"date_debut + dt.timedelta(days=+360 + jour) = "
    #      f"{date_debut + dt.timedelta(days=+360 + jour)}")
    print(f"jour = {jour} ({date_debut + dt.timedelta(days=+360 + jour)})")

    if df.index[-1] == date_debut + dt.timedelta(days=+360 + jour):

        # Creation du dataframe
        my_df_full = pd.DataFrame(data=df['Close'])
        #print(f"df['Close'][(len(df['Close']) - jour - 20):(len(df['Close']) - jour)].values = {df['Close'][(len(df['Close']) - jour - 20):(len(df['Close']) - jour)].values}")
        #print(f"df.index[(len(df['Close']) - jour - 20):(len(df['Close']) - jour)] = {df.index[(len(df['Close']) - jour - 20):(len(df['Close']) - jour)]}")
        #print(f"my_df_full = \n{my_df_full}")

        # Rajout des moyennes
        my_df_full['J2'] = my_df_full['Close'].rolling(window=2).mean()
        my_df_full['J3'] = my_df_full['Close'].rolling(window=3).mean()
        my_df_full['J5'] = my_df_full['Close'].rolling(window=5).mean()
        my_df_full['J10'] = my_df_full['Close'].rolling(window=10).mean()
        my_df_full['J15'] = my_df_full['Close'].rolling(window=15).mean()
        my_df_full['J20'] = my_df_full['Close'].rolling(window=20).mean()
        #print(f"my_df_full = \n{my_df_full}")
        my_df_mois = pd.DataFrame(data=my_df_full[(len(my_df_full) - 21):(len(my_df_full))].values,
                                  index=my_df_full.index[(len(my_df_full) - 21):(len(my_df_full))],
                                  columns=['Close', 'J2', 'J3', 'J5', 'J10', 'J15', 'J20'])
        #print(f"my_df_mois = \n{my_df_mois}")
        my_df_jourJ = pd.DataFrame(data=my_df_mois[(len(my_df_mois) - 2):(len(df))].values,
                                   index=my_df_mois.index[(len(my_df_mois) - 2):(len(my_df_mois))],
                                   columns=['Close', 'J2', 'J3', 'J5', 'J10', 'J15', 'J20'])
        #print(f"my_df_jourJ = \n{my_df_jourJ}")

        # calcul des pentes max et min pour l'action et les moyennes et écart type
        # création des dictionnaire pour la vente et l'achat
        dico_extremum = {}
        dico_loiNormale = {}
        dico_vente = {"pente": dict()}
        dico_achat = {"pente": dict()}
        for value in ['Close', 'J2', 'J3', 'J5', 'J10', 'J15', 'J20']:
            df_hist = pd.DataFrame(data=my_df_full[value] - my_df_full[value].shift())
            median_column = df_hist[value]
            median_column.plot(kind="hist")
            #plt.show()
            dico_extremum[value] = {"Max": float(pd.DataFrame(data=my_df_full[value] -
                                                                   my_df_full[value].shift()).max(0).values),
                                    "Min": float(pd.DataFrame(data=my_df_full[value] -
                                                                   my_df_full[value].shift()).min(0).values)}
            dico_loiNormale[value] = {"Moy": float(pd.DataFrame(data=my_df_full[value] -
                                                                     my_df_full[value].shift()).mean(axis=0).values),
                                      "Sig": float(pd.DataFrame(data=my_df_full[value] -
                                                                     my_df_full[value].shift()).std(axis=0).values)}
            if value == "Close":
                dico_vente["pente"][value] = [0.]
            if value == "J5" or value == "J10" or value == "J15" or value == "J20":
                dico_vente["pente"][value] = [False,
                                              dico_loiNormale[value]["Moy"] - 1 * dico_loiNormale[value]["Sig"],
                                              dico_loiNormale[value]["Moy"] - 0.5 * dico_loiNormale[value]["Sig"],
                                              dico_loiNormale[value]["Moy"] - 0.25 * dico_loiNormale[value]["Sig"],
                                              dico_loiNormale[value]["Moy"] - 0.125 * dico_loiNormale[value]["Sig"],
                                              dico_loiNormale[value]["Moy"],
                                              dico_loiNormale[value]["Moy"] + 0.125 * dico_loiNormale[value]["Sig"],
                                              dico_loiNormale[value]["Moy"] + 0.25 * dico_loiNormale[value]["Sig"],
                                              dico_loiNormale[value]["Moy"] + 0.5 * dico_loiNormale[value]["Sig"],
                                              dico_loiNormale[value]["Moy"] + 1 * dico_loiNormale[value]["Sig"]]
            # if value == "J3":
            #     dico_vente["pente"][value] = [dico_loiNormale[value]["Moy"] - 1.3 * dico_loiNormale[value]["Sig"]]
            # if value == "J6":
            #     dico_vente["pente"][value] = [dico_loiNormale[value]["Moy"] - 1.2 * dico_loiNormale[value]["Sig"]]
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
            if value == "Close":
                dico_achat["pente"][value] = [0.]
            #print(dico_loiNormale)
        #print(dico_extremum)
        print(dico_loiNormale)
        #print(dico_vente)

        # Rajout des valeurs spécifiques
        my_df_jourJ['SansTransaction'] = nbr_action * my_df_jourJ['Close']
        df_final = pd.DataFrame()
        # Rajout du total
        l_columns = list()
        l_values = list()
        l_columns.append('Total')
        l_values.append(my_df_jourJ['SansTransaction'].values[1])
        # print(l_columns)
        # print(l_values)
        df_tempo = pd.DataFrame(data=l_values, index=['SansTransaction'], columns=l_columns)
        # print(df_tempo)
        df_final = df_final.append(df_tempo, ignore_index=False)
        # print(df_final)
        df_tempo = pd.DataFrame(data=my_df_jourJ['SansTransaction'].values[1],
                                index=[my_df_jourJ['SansTransaction'].index[1]], columns=['SansTransaction'])

        dico_my_df_graph = {'Close': my_df_jourJ['Close'].values[1],
                            'SansTransaction': my_df_jourJ['SansTransaction'].values[1]}

        #print(my_df_full.head(5))
        #print(my_df_full.tail(5))

        # Iteration sur l'année 2020 Rendement Max
        if bool_Max:
            # Rajout des valeurs specifiques
            my_df_jourJ['Mise'] = 100.
            my_df_jourJ['Secu'] = 0.
            my_df_jourJ['PorteFeuille'] = 0.
            my_df_jourJ['NbrAction'] = 0.
            my_df_jourJ['Vente'] = False
            my_df_jourJ['Achat'] = False
            my_df_jourJ['ValeurAchat'] = np.NaN
            my_df_jourJ['ValeurVente'] = np.NaN
            my_df_jourJ['MaxRendement'] = 0.
            if jour == 0:
                # Initialisation du premier achat
                my_df_jourJ['Close'].values[1] = valeur_action
                my_df_jourJ['Mise'].values[1] = 0.
                my_df_jourJ['PorteFeuille'].values[1] = nbr_action * my_df_jourJ['Close'].values[1]
                my_df_jourJ['NbrAction'].values[1] = nbr_action
                my_df_jourJ['Achat'].values[1] = True
                my_df_jourJ['ValeurAchat'].values[1] = valeur_action
                my_df_jourJ['MaxRendement'].values[1] = my_df_jourJ['Mise'].values[1] + my_df_jourJ['Secu'].values[1] + \
                                                        my_df_jourJ['PorteFeuille'].values[1]
                vente = False
                achat = True
            else:
                #print(f"dico_mem['MaxRendement'] = \n{dico_mem['MaxRendement']}")
                my_df_jourJ['Mise'].values[0] = dico_mem['MaxRendement']['DataFrame']['Mise'].values[1]
                my_df_jourJ['Secu'].values[0] = dico_mem['MaxRendement']['DataFrame']['Secu'].values[1]
                my_df_jourJ['NbrAction'].values[0] = dico_mem['MaxRendement']['DataFrame']['NbrAction'].values[1]
                my_df_jourJ['PorteFeuille'].values[0] = dico_mem['MaxRendement']['DataFrame']['PorteFeuille'].values[1]
                my_df_jourJ['ValeurAchat'].values[0] = dico_mem['MaxRendement']['DataFrame']['ValeurAchat'].values[1]
                my_df_jourJ['ValeurVente'].values[0] = dico_mem['MaxRendement']['DataFrame']['ValeurVente'].values[1]
                my_df_jourJ['MaxRendement'].values[0] = dico_mem['MaxRendement']['DataFrame']['Mise'].values[1] + \
                                                        dico_mem['MaxRendement']['DataFrame']['Secu'].values[1] + \
                                                        dico_mem['MaxRendement']['DataFrame']['PorteFeuille'].values[1]
                my_df_jourJ['Vente'].values[0] = dico_mem['MaxRendement']['DataFrame']['Vente'].values[0]
                my_df_jourJ['Achat'].values[0] = dico_mem['MaxRendement']['DataFrame']['Achat'].values[0]
                vente = dico_mem['MaxRendement']['vente']
                achat = dico_mem['MaxRendement']['achat']


                my_df_jourJ['Mise'].values[1] = my_df_jourJ['Mise'].values[0]
                my_df_jourJ['Secu'].values[1] = my_df_jourJ['Secu'].values[0]
                my_df_jourJ['NbrAction'].values[1] = my_df_jourJ['NbrAction'].values[0]
                my_df_jourJ['PorteFeuille'].values[1] = my_df_jourJ['Close'].values[1] * \
                                                        my_df_jourJ['NbrAction'].values[1]
                my_df_jourJ['ValeurAchat'].values[1] = my_df_jourJ['ValeurAchat'].values[0]
                my_df_jourJ['ValeurVente'].values[1] = my_df_jourJ['ValeurVente'].values[0]
                my_df_jourJ['MaxRendement'].values[1] = my_df_jourJ['Mise'].values[1] + \
                                                        my_df_jourJ['Secu'].values[1] + \
                                                        my_df_jourJ['PorteFeuille'].values[1]
            #print(f"my_df_jourJ = \n{my_df_jourJ}")

            #print(my_df_jourJ.iloc[i])
            if achat:  # On possède des actions
                # Regarde si vente
                if bool_pente('Close', 1, my_df_jourJ):  # Pas de vente l'action augmente ou stagne
                    vente = False
                else:  # on vend
                    #print("vente")
                    vente = True
            # print('Vente ?')
            if vente and achat:  # on va vendre, on ne possèdera plus d'action
                my_df_jourJ['Vente'].values[1] = True
                my_df_jourJ['Achat'].values[1] = False
                if my_df_jourJ['Close'].values[0] * my_df_jourJ['NbrAction'].values[0] > 100.:
                    my_df_jourJ['Mise'].values[1] = 100.
                    my_df_jourJ['Secu'].values[1] += my_df_jourJ['Close'].values[0] * my_df_jourJ['NbrAction'].values[0]\
                                                     - 100.
                else:
                    my_df_jourJ['Mise'].values[1] = my_df_jourJ['Close'].values[0] * my_df_jourJ['NbrAction'].values[0]
                    my_df_jourJ['Secu'].values[1] += 0.
                my_df_jourJ['PorteFeuille'].values[1] = 0.
                my_df_jourJ['NbrAction'].values[1] = 0.
                my_df_jourJ['ValeurVente'].values[1] = my_df_jourJ['Close'].values[0]
                my_df_jourJ['ValeurAchat'].values[1] = np.NaN
                my_df_jourJ['MaxRendement'].values[1] = my_df_jourJ['Mise'].values[1] + my_df_jourJ['Secu'].values[1] + \
                                                        my_df_jourJ['PorteFeuille'].values[1]
                #print(my_df_jourJ.iloc[i])
                #print(f"VENTE (Date : {my_df_jourJ.index[1]}) :\n     Mise : {my_df_jourJ['Mise'].values[1]}\n"
                #      f"     Sécurisé : {my_df_jourJ['Secu'].values[1]}\n"
                #      f"     Valeur d'achat : {my_df_jourJ['ValeurAchat'].values[0]}\n"
                #      f"     Valeur de vente : {my_df_jourJ['ValeurVente'].values[1]}")
                achat = False
            # print('achat ?')
            if vente and not achat and not my_df_jourJ['Vente'].values[1] and not my_df_jourJ['Achat'].values[1]:
                # On a vendu et pas encore racheté.
                # Conditions pour rachat
                if bool_pente('Close', 1, my_df_jourJ):  # On achète, car remonté au niveau vente
                    my_df_jourJ['Vente'].values[1] = False
                    my_df_jourJ['Achat'].values[1] = True
                    achat = True
                    #print("achat")
                    vente = False
                    my_df_jourJ['Mise'].values[1] = 0.
                    my_df_jourJ['Secu'].values[1] = my_df_jourJ['Secu'].values[0]
                    my_df_jourJ['NbrAction'].values[1] = my_df_jourJ['Mise'].values[0] / my_df_jourJ['Close'].values[0]
                    my_df_jourJ['PorteFeuille'].values[1] = my_df_jourJ['Close'].values[1] * \
                                                            my_df_jourJ['NbrAction'].values[1]
                    my_df_jourJ['ValeurAchat'].values[1] = my_df_jourJ['Close'].values[0]
                    my_df_jourJ['ValeurVente'].values[1] = np.NaN
                    my_df_jourJ['MaxRendement'].values[1] = my_df_jourJ['Mise'].values[1] + my_df_jourJ['Secu'].values[1]\
                                                            + my_df_jourJ['PorteFeuille'].values[1]
                    #print(my_df_jourJ.iloc[i])
                    #print(f"ACHAT (Date : {my_df_jourJ.index[1]}) :\n"
                    #      f"     PorteFeuille : {my_df_jourJ['PorteFeuille'].values[1]}\n"
                    #      f"     Sécurisé : {my_df_jourJ['Secu'].values[1]}\n"
                    #      f"     Nbr Action(s) : {my_df_jourJ['NbrAction'].values[1]}\n"
                    #      f"     Valeur d'achat : {my_df_jourJ['ValeurAchat'].values[1]}\n"
                    #      f"     Valeur de vente : {my_df_jourJ['ValeurVente'].values[0]}")

            #print(my_df_jourJ.tail(10))
            #print(f"A LA FIN (Date : {my_df_jourJ.index[1]}) :\n"
            #      f"     PorteFeuille : {my_df_jourJ['PorteFeuille'].values[1]}\n"
            #      f"     Nbr Action(s) : {my_df_jourJ['NbrAction'].values[1]}\n"
            #      f"     Sécurisé : {my_df_jourJ['Secu'].values[1]}\n"
            #      f"     Mise : {my_df_jourJ['Mise'].values[1]}")
            dico_mem['MaxRendement'] = {'DataFrame': my_df_jourJ.copy(deep=True), 'vente': vente, 'achat': achat}

            #print(f"dico_mem['MaxRendement'] = \n{dico_mem['MaxRendement']}")

            # Rajout du total
            l_columns = list()
            l_values = list()
            l_columns.append('Total')
            l_values.append(my_df_jourJ['MaxRendement'].values[1])
            # print(l_columns)
            # print(l_values)
            df_tempo = pd.DataFrame(data=l_values, index=['MaxRendement'], columns=l_columns)
            # print(df_tempo)
            df_final = df_final.append(df_tempo, ignore_index=False)
            # print(df_final)

            dico_my_df_graph['MaxRendement'] = my_df_jourJ['MaxRendement'].values[1]

        # Iteration sur l'année 2019 Rendement Max sans Sécurisation
        if bool_Max_ssSecu:
            # Rajout des valeurs specifiques
            my_df_jourJ['Mise'] = 100.
            my_df_jourJ['Secu'] = 0.
            my_df_jourJ['PorteFeuille'] = 0.
            my_df_jourJ['NbrAction'] = 0.
            my_df_jourJ['Vente'] = False
            my_df_jourJ['Achat'] = False
            my_df_jourJ['ValeurAchat'] = np.NaN
            my_df_jourJ['ValeurVente'] = np.NaN
            my_df_jourJ['MaxRendement_ssSecu'] = 0.
            if jour == 0:
                # Initialisation du premier achat
                my_df_jourJ['Close'].values[1] = valeur_action
                my_df_jourJ['Mise'].values[1] = 0.
                my_df_jourJ['PorteFeuille'].values[1] = nbr_action * my_df_jourJ['Close'].values[1]
                my_df_jourJ['NbrAction'].values[1] = nbr_action
                my_df_jourJ['Achat'].values[1] = True
                my_df_jourJ['ValeurAchat'].values[1] = valeur_action
                my_df_jourJ['MaxRendement_ssSecu'].values[1] = my_df_jourJ['Mise'].values[1] + \
                                                               my_df_jourJ['Secu'].values[1] + \
                                                               my_df_jourJ['PorteFeuille'].values[1]
                vente = False
                achat = True
            else:
                print(f"dico_mem['MaxRendement_ssSecu'] = \n{dico_mem['MaxRendement_ssSecu']}")
                my_df_jourJ['Mise'].values[0] = dico_mem['MaxRendement_ssSecu']['DataFrame']['Mise'].values[1]
                my_df_jourJ['Secu'].values[0] = dico_mem['MaxRendement_ssSecu']['DataFrame']['Secu'].values[1]
                my_df_jourJ['NbrAction'].values[0] = dico_mem['MaxRendement_ssSecu']['DataFrame']['NbrAction'].values[1]
                my_df_jourJ['PorteFeuille'].values[0] = \
                    dico_mem['MaxRendement_ssSecu']['DataFrame']['PorteFeuille'].values[1]
                my_df_jourJ['ValeurAchat'].values[0] = \
                    dico_mem['MaxRendement_ssSecu']['DataFrame']['ValeurAchat'].values[1]
                my_df_jourJ['ValeurVente'].values[0] = \
                    dico_mem['MaxRendement_ssSecu']['DataFrame']['ValeurVente'].values[1]
                my_df_jourJ['MaxRendement_ssSecu'].values[0] = \
                    dico_mem['MaxRendement_ssSecu']['DataFrame']['Mise'].values[1] + \
                    dico_mem['MaxRendement_ssSecu']['DataFrame']['Secu'].values[1] + \
                    dico_mem['MaxRendement_ssSecu']['DataFrame']['PorteFeuille'].values[1]
                my_df_jourJ['Vente'].values[0] = dico_mem['MaxRendement_ssSecu']['DataFrame']['Vente'].values[0]
                my_df_jourJ['Achat'].values[0] = dico_mem['MaxRendement_ssSecu']['DataFrame']['Achat'].values[0]
                vente = dico_mem['MaxRendement_ssSecu']['vente']
                achat = dico_mem['MaxRendement_ssSecu']['achat']

                my_df_jourJ['Mise'].values[1] = my_df_jourJ['Mise'].values[0]
                my_df_jourJ['Secu'].values[1] = my_df_jourJ['Secu'].values[0]
                my_df_jourJ['NbrAction'].values[1] = my_df_jourJ['NbrAction'].values[0]
                my_df_jourJ['PorteFeuille'].values[1] = my_df_jourJ['Close'].values[1] * \
                                                        my_df_jourJ['NbrAction'].values[1]
                my_df_jourJ['ValeurAchat'].values[1] = my_df_jourJ['ValeurAchat'].values[0]
                my_df_jourJ['ValeurVente'].values[1] = my_df_jourJ['ValeurVente'].values[0]
                my_df_jourJ['MaxRendement_ssSecu'].values[1] = my_df_jourJ['Mise'].values[1] + \
                                                        my_df_jourJ['Secu'].values[1] + \
                                                        my_df_jourJ['PorteFeuille'].values[1]
            print(f"my_df_jourJ = \n{my_df_jourJ}")

            #print(my_df_jourJ.iloc[i])
            if achat:  # On possède des actions
                # Regarde si vente
                if bool_pente('Close', 1, my_df_jourJ):  # Pas de vente l'action augmente ou stagne
                    vente = False
                else:  # on vend
                    vente = True
            # print('Vente ?')
            if vente and achat:  # on va vendre, on ne possèdera plus d'action
                my_df_jourJ['Vente'].values[1] = True
                my_df_jourJ['Achat'].values[1] = False
                my_df_jourJ['Mise'].values[1] = my_df_jourJ['Close'].values[0] * my_df_jourJ['NbrAction'].values[0]
                my_df_jourJ['Secu'].values[1] += 0.
                my_df_jourJ['PorteFeuille'].values[1] = 0.
                my_df_jourJ['NbrAction'].values[1] = 0.
                my_df_jourJ['ValeurVente'].values[1] = my_df_jourJ['Close'].values[0]
                my_df_jourJ['ValeurAchat'].values[1] = np.NaN
                my_df_jourJ['MaxRendement_ssSecu'].values[1] = my_df_jourJ['Mise'].values[1] + \
                                                               my_df_jourJ['Secu'].values[1] + \
                                                               my_df_jourJ['PorteFeuille'].values[1]
                #print(my_df_jourJ.iloc[i])
                print(f"VENTE (Date : {my_df_jourJ.index[1]}) :\n     Mise : {my_df_jourJ['Mise'].values[1]}\n"
                      f"     Sécurisé : {my_df_jourJ['Secu'].values[1]}\n"
                      f"     Valeur d'achat : {my_df_jourJ['ValeurAchat'].values[0]}\n"
                      f"     Valeur de vente : {my_df_jourJ['ValeurVente'].values[1]}")
                achat = False
            # print('achat ?')
            if vente and not achat and not my_df_jourJ['Vente'].values[1] and not my_df_jourJ['Achat'].values[1]:
                # On a vendu et pas encore racheté.
                # Conditions pour rachat
                if bool_pente('Close', 1, my_df_jourJ):  # On achète, car remonté au niveau vente
                    my_df_jourJ['Vente'].values[1] = False
                    my_df_jourJ['Achat'].values[1] = True
                    achat = True
                    vente = False
                    my_df_jourJ['Mise'].values[1] = 0.
                    my_df_jourJ['Secu'].values[1] = my_df_jourJ['Secu'].values[0]
                    my_df_jourJ['NbrAction'].values[1] = my_df_jourJ['Mise'].values[0] / my_df_jourJ['Close'].values[0]
                    my_df_jourJ['PorteFeuille'].values[1] = my_df_jourJ['Close'].values[1] * \
                                                            my_df_jourJ['NbrAction'].values[1]
                    my_df_jourJ['ValeurAchat'].values[1] = my_df_jourJ['Close'].values[0]
                    my_df_jourJ['ValeurVente'].values[1] = np.NaN
                    my_df_jourJ['MaxRendement_ssSecu'].values[1] = my_df_jourJ['Mise'].values[1] + \
                                                                   my_df_jourJ['Secu'].values[1] + \
                                                                   my_df_jourJ['PorteFeuille'].values[1]
                    #print(my_df_jourJ.iloc[i])
                    print(f"ACHAT (Date : {my_df_jourJ.index[1]}) :\n"
                          f"     PorteFeuille : {my_df_jourJ['PorteFeuille'].values[1]}\n"
                          f"     Sécurisé : {my_df_jourJ['Secu'].values[1]}\n"
                          f"     Nbr Action(s) : {my_df_jourJ['NbrAction'].values[1]}\n"
                          f"     Valeur d'achat : {my_df_jourJ['ValeurAchat'].values[1]}\n"
                          f"     Valeur de vente : {my_df_jourJ['ValeurVente'].values[0]}")

            #print(my_df_jourJ.tail(10))
            print(f"A LA FIN (Date : {my_df_jourJ.index[1]}) :\n"
                  f"     PorteFeuille : {my_df_jourJ['PorteFeuille'].values[1]}\n"
                  f"     Nbr Action(s) : {my_df_jourJ['NbrAction'].values[1]}\n"
                  f"     Sécurisé : {my_df_jourJ['Secu'].values[1]}\n"
                  f"     Mise : {my_df_jourJ['Mise'].values[1]}")
            dico_mem['MaxRendement_ssSecu'] = {'DataFrame': my_df_jourJ.copy(deep=True), 'vente': vente, 'achat': achat}

            print(f"dico_mem['MaxRendement_ssSecu'] = \n{dico_mem['MaxRendement_ssSecu']}")

            # Rajout du total
            l_columns = list()
            l_values = list()
            l_columns.append('Total')
            l_values.append(my_df_jourJ['MaxRendement_ssSecu'].values[1])
            # print(l_columns)
            # print(l_values)
            df_tempo = pd.DataFrame(data=l_values, index=['MaxRendement_ssSecu'], columns=l_columns)
            # print(df_tempo)
            df_final = df_final.append(df_tempo, ignore_index=False)
            # print(df_final)

            dico_my_df_graph['MaxRendement_ssSecu'] = my_df_jourJ['MaxRendement_ssSecu'].values[1]

        # Iteration sur l'année 2019 Rendement Max Nbr Action Constante
        if bool_Max_NbrActionCste:
            # Rajout des valeurs specifiques
            my_df_jourJ['Mise'] = 100.
            my_df_jourJ['Secu'] = 0.
            my_df_jourJ['PorteFeuille'] = 0.
            my_df_jourJ['NbrAction'] = 0.
            my_df_jourJ['Vente'] = False
            my_df_jourJ['Achat'] = False
            my_df_jourJ['ValeurAchat'] = np.NaN
            my_df_jourJ['ValeurVente'] = np.NaN
            my_df_jourJ['MaxRendement_NbrActionCste'] = 0.
            if jour == 0:
                # Initialisation du premier achat
                my_df_jourJ['Close'].values[1] = valeur_action
                my_df_jourJ['Mise'].values[1] = 0.
                my_df_jourJ['PorteFeuille'].values[1] = nbr_action * my_df_jourJ['Close'].values[1]
                my_df_jourJ['NbrAction'].values[1] = nbr_action
                my_df_jourJ['Achat'].values[1] = True
                my_df_jourJ['ValeurAchat'].values[1] = valeur_action
                my_df_jourJ['MaxRendement_NbrActionCste'].values[1] = my_df_jourJ['Mise'].values[1] + \
                                                                      my_df_jourJ['Secu'].values[1] + \
                                                                      my_df_jourJ['PorteFeuille'].values[1]
                vente = False
                achat = True
            else:
                print(f"dico_mem['MaxRendement_NbrActionCste'] = \n{dico_mem['MaxRendement_NbrActionCste']}")
                my_df_jourJ['Mise'].values[0] = dico_mem['MaxRendement_NbrActionCste']['DataFrame']['Mise'].values[1]
                my_df_jourJ['Secu'].values[0] = dico_mem['MaxRendement_NbrActionCste']['DataFrame']['Secu'].values[1]
                my_df_jourJ['NbrAction'].values[0] = \
                    dico_mem['MaxRendement_NbrActionCste']['DataFrame']['NbrAction'].values[1]
                my_df_jourJ['PorteFeuille'].values[0] = \
                    dico_mem['MaxRendement_NbrActionCste']['DataFrame']['PorteFeuille'].values[1]
                my_df_jourJ['ValeurAchat'].values[0] = \
                    dico_mem['MaxRendement_NbrActionCste']['DataFrame']['ValeurAchat'].values[1]
                my_df_jourJ['ValeurVente'].values[0] = \
                    dico_mem['MaxRendement_NbrActionCste']['DataFrame']['ValeurVente'].values[1]
                my_df_jourJ['MaxRendement_NbrActionCste'].values[0] = \
                    dico_mem['MaxRendement_NbrActionCste']['DataFrame']['Mise'].values[1] + \
                    dico_mem['MaxRendement_NbrActionCste']['DataFrame']['Secu'].values[1] + \
                    dico_mem['MaxRendement_NbrActionCste']['DataFrame']['PorteFeuille'].values[1]
                my_df_jourJ['Vente'].values[0] = dico_mem['MaxRendement_NbrActionCste']['DataFrame']['Vente'].values[0]
                my_df_jourJ['Achat'].values[0] = dico_mem['MaxRendement_NbrActionCste']['DataFrame']['Achat'].values[0]
                vente = dico_mem['MaxRendement_NbrActionCste']['vente']
                achat = dico_mem['MaxRendement_NbrActionCste']['achat']

                my_df_jourJ['Mise'].values[1] = my_df_jourJ['Mise'].values[0]
                my_df_jourJ['Secu'].values[1] = my_df_jourJ['Secu'].values[0]
                my_df_jourJ['NbrAction'].values[1] = my_df_jourJ['NbrAction'].values[0]
                my_df_jourJ['PorteFeuille'].values[1] = my_df_jourJ['Close'].values[1] * \
                                                        my_df_jourJ['NbrAction'].values[1]
                my_df_jourJ['ValeurAchat'].values[1] = my_df_jourJ['ValeurAchat'].values[0]
                my_df_jourJ['ValeurVente'].values[1] = my_df_jourJ['ValeurVente'].values[0]
                my_df_jourJ['MaxRendement_NbrActionCste'].values[1] = my_df_jourJ['Mise'].values[1] + \
                                                                      my_df_jourJ['Secu'].values[1] + \
                                                                      my_df_jourJ['PorteFeuille'].values[1]
            print(f"my_df_jourJ = \n{my_df_jourJ}")

            #print(my_df_jourJ.iloc[i])
            if achat:  # On possède des actions
                # Regarde si vente
                if bool_pente('Close', 1, my_df_jourJ):  # Pas de vente l'action augmente ou stagne
                    vente = False
                else:  # on vend
                    vente = True
            # print('Vente ?')
            if vente and achat:  # on va vendre, on ne possèdera plus d'action
                my_df_jourJ['Vente'].values[1] = True
                my_df_jourJ['Achat'].values[1] = False
                my_df_jourJ['Mise'].values[1] = my_df_jourJ['Close'].values[0] * my_df_jourJ['NbrAction'].values[0]
                my_df_jourJ['Secu'].values[1] += 0.
                my_df_jourJ['PorteFeuille'].values[1] = 0.
                my_df_jourJ['NbrAction'].values[1] = 0.
                my_df_jourJ['ValeurVente'].values[1] = my_df_jourJ['Close'].values[0]
                my_df_jourJ['ValeurAchat'].values[1] = np.NaN
                my_df_jourJ['MaxRendement_NbrActionCste'].values[1] = my_df_jourJ['Mise'].values[1] + \
                                                                      my_df_jourJ['Secu'].values[1] + \
                                                                      my_df_jourJ['PorteFeuille'].values[1]
                #print(my_df_jourJ.iloc[i])
                print(f"VENTE (Date : {my_df_jourJ.index[1]}) :\n     Mise : {my_df_jourJ['Mise'].values[1]}\n"
                      f"     Sécurisé : {my_df_jourJ['Secu'].values[1]}\n"
                      f"     Valeur d'achat : {my_df_jourJ['ValeurAchat'].values[0]}\n"
                      f"     Valeur de vente : {my_df_jourJ['ValeurVente'].values[1]}")
                achat = False
            # print('achat ?')
            if vente and not achat and not my_df_jourJ['Vente'].values[1] and not my_df_jourJ['Achat'].values[1]:
                # On a vendu et pas encore racheté.
                # Conditions pour rachat
                if bool_pente('Close', 1, my_df_jourJ):  # On achète, car remonté au niveau vente
                    my_df_jourJ['Vente'].values[1] = False
                    my_df_jourJ['Achat'].values[1] = True
                    achat = True
                    vente = False
                    if my_df_jourJ['Mise'].values[0] + my_df_jourJ['Secu'].values[0] >= nbr_action * \
                            my_df_jourJ['Close'].values[0]:
                        my_df_jourJ['Secu'].values[1] = my_df_jourJ['Mise'].values[0] + my_df_jourJ['Secu'].values[0] -\
                                                        (nbr_action * my_df_jourJ['Close'].values[0])
                        my_df_jourJ['Mise'].values[1] = 0.
                        my_df_jourJ['NbrAction'].values[1] = nbr_action
                    else:
                        my_df_jourJ['NbrAction'].values[1] = (my_df_jourJ['Mise'].values[0] +
                                                              my_df_jourJ['Secu'].values[0]) / \
                                                             my_df_jourJ['Close'].values[0]
                        my_df_jourJ['Secu'].values[1] = 0.
                        my_df_jourJ['Mise'].values[1] = 0.
                    my_df_jourJ['PorteFeuille'].values[1] = my_df_jourJ['Close'].values[1] * \
                                                            my_df_jourJ['NbrAction'].values[1]
                    my_df_jourJ['ValeurAchat'].values[1] = my_df_jourJ['Close'].values[0]
                    my_df_jourJ['ValeurVente'].values[1] = np.NaN
                    my_df_jourJ['MaxRendement_NbrActionCste'].values[1] = my_df_jourJ['Mise'].values[1] + \
                                                                          my_df_jourJ['Secu'].values[1] + \
                                                                          my_df_jourJ['PorteFeuille'].values[1]
                    #print(my_df_jourJ.iloc[i])
                    print(f"ACHAT (Date : {my_df_jourJ.index[1]}) :\n"
                          f"     PorteFeuille : {my_df_jourJ['PorteFeuille'].values[1]}\n"
                          f"     Sécurisé : {my_df_jourJ['Secu'].values[1]}\n"
                          f"     Nbr Action(s) : {my_df_jourJ['NbrAction'].values[1]}\n"
                          f"     Valeur d'achat : {my_df_jourJ['ValeurAchat'].values[1]}\n"
                          f"     Valeur de vente : {my_df_jourJ['ValeurVente'].values[0]}")

            #print(my_df_jourJ.tail(10))
            print(f"A LA FIN (Date : {my_df_jourJ.index[1]}) :\n"
                  f"     PorteFeuille : {my_df_jourJ['PorteFeuille'].values[1]}\n"
                  f"     Nbr Action(s) : {my_df_jourJ['NbrAction'].values[1]}\n"
                  f"     Sécurisé : {my_df_jourJ['Secu'].values[1]}\n"
                  f"     Mise : {my_df_jourJ['Mise'].values[1]}")
            dico_mem['MaxRendement_NbrActionCste'] = \
                {'DataFrame': my_df_jourJ.copy(deep=True), 'vente': vente, 'achat': achat}

            print(f"dico_mem['MaxRendement_NbrActionCste'] = \n{dico_mem['MaxRendement_NbrActionCste']}")

            # Rajout du total
            l_columns = list()
            l_values = list()
            l_columns.append('Total')
            l_values.append(my_df_jourJ['MaxRendement_NbrActionCste'].values[1])
            # print(l_columns)
            # print(l_values)
            df_tempo = pd.DataFrame(data=l_values, index=['MaxRendement_NbrActionCste'], columns=l_columns)
            # print(df_tempo)
            df_final = df_final.append(df_tempo, ignore_index=False)
            # print(df_final)

            dico_my_df_graph['MaxRendement_NbrActionCste'] = my_df_jourJ['MaxRendement_NbrActionCste'].values[1]

        # Iteration sur l'année 2019 Scenario1
        if bool_S1:
            # Generation listing models
            l_models_vente = generation_listing_models(**dico_vente)
            print(f"Nombre de modèle = {str(len(l_models_vente))}")
            l_models_achat = generation_listing_models(**dico_achat)
            print(f"Nombre de modèle = {str(len(l_models_achat))}")

            nbr_S = - 1
            for model_vente in l_models_vente:
                for model_achat in l_models_achat:
                    nbr_S += 1
                    #print(f"Modèle N° : {nbr_S + 1}")
                    # Rajout des valeurs specifiques
                    my_df_jourJ['Mise'] = 100.
                    my_df_jourJ['Secu'] = 0.
                    my_df_jourJ['PorteFeuille'] = 0.
                    my_df_jourJ['NbrAction'] = 0.
                    my_df_jourJ['Vente'] = False
                    my_df_jourJ['Achat'] = False
                    my_df_jourJ['ValeurAchat'] = np.NaN
                    my_df_jourJ['ValeurVente'] = np.NaN
                    my_df_jourJ['Scenario'] = 0.
                    if jour == 0:
                        # Initialisation du premier achat
                        my_df_jourJ['Close'].values[1] = valeur_action
                        my_df_jourJ['Mise'].values[1] = 0.
                        my_df_jourJ['PorteFeuille'].values[1] = nbr_action * my_df_jourJ['Close'].values[1]
                        my_df_jourJ['NbrAction'].values[1] = nbr_action
                        my_df_jourJ['Achat'].values[1] = True
                        my_df_jourJ['ValeurAchat'].values[1] = valeur_action
                        my_df_jourJ['Scenario'].values[1] = my_df_jourJ['Mise'].values[1] + \
                                                            my_df_jourJ['Secu'].values[1] + \
                                                            my_df_jourJ['PorteFeuille'].values[1]
                        vente = False
                        achat = True
                    else:
                        #print(f"dico_mem['Scenario_' + str(nbr_S)] = \n{dico_mem['Scenario_' + str(nbr_S)]}")
                        my_df_jourJ['Mise'].values[0] = \
                            dico_mem['Scenario_' + str(nbr_S)]['DataFrame']['Mise'].values[1]
                        my_df_jourJ['Secu'].values[0] = \
                            dico_mem['Scenario_' + str(nbr_S)]['DataFrame']['Secu'].values[1]
                        my_df_jourJ['NbrAction'].values[0] = \
                            dico_mem['Scenario_' + str(nbr_S)]['DataFrame']['NbrAction'].values[1]
                        my_df_jourJ['PorteFeuille'].values[0] = \
                            dico_mem['Scenario_' + str(nbr_S)]['DataFrame']['PorteFeuille'].values[1]
                        my_df_jourJ['ValeurAchat'].values[0] = \
                            dico_mem['Scenario_' + str(nbr_S)]['DataFrame']['ValeurAchat'].values[1]
                        my_df_jourJ['ValeurVente'].values[0] = \
                            dico_mem['Scenario_' + str(nbr_S)]['DataFrame']['ValeurVente'].values[1]
                        my_df_jourJ['Scenario'].values[0] = \
                            dico_mem['Scenario_' + str(nbr_S)]['DataFrame']['Mise'].values[1] + \
                            dico_mem['Scenario_' + str(nbr_S)]['DataFrame']['Secu'].values[1] + \
                            dico_mem['Scenario_' + str(nbr_S)]['DataFrame']['PorteFeuille'].values[1]
                        my_df_jourJ['Vente'].values[0] = \
                            dico_mem['Scenario_' + str(nbr_S)]['DataFrame']['Vente'].values[0]
                        my_df_jourJ['Achat'].values[0] = \
                            dico_mem['Scenario_' + str(nbr_S)]['DataFrame']['Achat'].values[0]
                        vente = dico_mem['Scenario_' + str(nbr_S)]['vente']
                        achat = dico_mem['Scenario_' + str(nbr_S)]['achat']

                        my_df_jourJ['Mise'].values[1] = my_df_jourJ['Mise'].values[0]
                        my_df_jourJ['Secu'].values[1] = my_df_jourJ['Secu'].values[0]
                        my_df_jourJ['NbrAction'].values[1] = my_df_jourJ['NbrAction'].values[0]
                        my_df_jourJ['PorteFeuille'].values[1] = my_df_jourJ['Close'].values[1] * \
                                                                my_df_jourJ['NbrAction'].values[1]
                        my_df_jourJ['ValeurAchat'].values[1] = my_df_jourJ['ValeurAchat'].values[0]
                        my_df_jourJ['ValeurVente'].values[1] = my_df_jourJ['ValeurVente'].values[0]
                        my_df_jourJ['Scenario'].values[1] = my_df_jourJ['Mise'].values[1] + \
                                                            my_df_jourJ['Secu'].values[1] + \
                                                            my_df_jourJ['PorteFeuille'].values[1]
                    #print(f"my_df_jourJ = \n{my_df_jourJ}")

                    # print(my_df_jourJ.iloc[i])
                    if achat and jour > 0:  # On possède des actions
                        # Regarde si vente
                        if bool_vente_scenario(1, my_df_jourJ, **model_vente):
                            vente = True
                        else:  # on ne vend pas
                            vente = False
                    # print('Vente ?')
                    if vente and achat:  # on va vendre, on ne possèdera plus d'action
                        my_df_jourJ['Vente'].values[1] = True
                        my_df_jourJ['Achat'].values[1] = False
                        if my_df_jourJ['Close'].values[1] * my_df_jourJ['NbrAction'].values[1] > 100.:
                            my_df_jourJ['Mise'].values[1] = 100.
                            my_df_jourJ['Secu'].values[1] += my_df_jourJ['Close'].values[1] * \
                                                             my_df_jourJ['NbrAction'].values[1] - 100.
                        else:
                            my_df_jourJ['Mise'].values[1] = my_df_jourJ['Close'].values[1] * \
                                                            my_df_jourJ['NbrAction'].values[1]
                            my_df_jourJ['Secu'].values[1] += 0.
                        my_df_jourJ['PorteFeuille'].values[1] = 0.
                        my_df_jourJ['NbrAction'].values[1] = 0.
                        my_df_jourJ['ValeurVente'].values[1] = my_df_jourJ['Close'].values[1]
                        my_df_jourJ['ValeurAchat'].values[1] = np.NaN
                        my_df_jourJ['Scenario'].values[1] = my_df_jourJ['Mise'].values[1] + \
                                                            my_df_jourJ['Secu'].values[1] + \
                                                            my_df_jourJ['PorteFeuille'].values[1]
                        # print(my_df_jourJ.iloc[i])
                        #print(f"VENTE (Date : {my_df_jourJ.index[1]}) :\n     Mise : {my_df_jourJ['Mise'].values[1]}\n"
                        #      f"     Sécurisé : {my_df_jourJ['Secu'].values[1]}\n"
                        #      f"     Valeur d'achat : {my_df_jourJ['ValeurAchat'].values[0]}\n"
                        #      f"     Valeur de vente : {my_df_jourJ['ValeurVente'].values[1]}")
                        achat = False
                    # print('achat ?')
                    if vente and not achat and not my_df_jourJ['Vente'].values[1] and not my_df_jourJ['Achat'].values[1]:
                        # On a vendu et pas encore racheté.
                        # Conditions pour rachat
                        if bool_achat_scenario(1, my_df_jourJ, **model_achat) or \
                                (my_df_jourJ['ValeurVente'].values[1] <= my_df_jourJ['Close'].values[1] and
                                 not my_df_jourJ['Vente'].values[0]):
                            my_df_jourJ['Vente'].values[1] = False
                            my_df_jourJ['Achat'].values[1] = True
                            achat = True
                            vente = False
                            my_df_jourJ['Mise'].values[1] = 0.
                            my_df_jourJ['Secu'].values[1] = my_df_jourJ['Secu'].values[0]
                            my_df_jourJ['NbrAction'].values[1] = \
                                my_df_jourJ['Mise'].values[0] / my_df_jourJ['Close'].values[1]
                            my_df_jourJ['PorteFeuille'].values[1] = my_df_jourJ['Close'].values[1] * \
                                                                    my_df_jourJ['NbrAction'].values[1]
                            my_df_jourJ['ValeurAchat'].values[1] = my_df_jourJ['Close'].values[1]
                            my_df_jourJ['ValeurVente'].values[1] = np.NaN
                            my_df_jourJ['Scenario'].values[1] = my_df_jourJ['Mise'].values[1] + \
                                                                my_df_jourJ['Secu'].values[1] + \
                                                                my_df_jourJ['PorteFeuille'].values[1]
                            # print(my_df_jourJ.iloc[i])
                            #print(f"ACHAT (Date : {my_df_jourJ.index[1]}) :\n"
                            #      f"     PorteFeuille : {my_df_jourJ['PorteFeuille'].values[1]}\n"
                            #      f"     Sécurisé : {my_df_jourJ['Secu'].values[1]}\n"
                            #      f"     Nbr Action(s) : {my_df_jourJ['NbrAction'].values[1]}\n"
                            #      f"     Valeur d'achat : {my_df_jourJ['ValeurAchat'].values[1]}\n"
                            #      f"     Valeur de vente : {my_df_jourJ['ValeurVente'].values[0]}")

                    # print(my_df_jourJ.tail(10))
                    #print(f"A LA FIN (Date : {my_df_jourJ.index[1]}) :\n"
                    #      f"     PorteFeuille : {my_df_jourJ['PorteFeuille'].values[1]}\n"
                    #      f"     Nbr Action(s) : {my_df_jourJ['NbrAction'].values[1]}\n"
                    #      f"     Sécurisé : {my_df_jourJ['Secu'].values[1]}\n"
                    #      f"     Mise : {my_df_jourJ['Mise'].values[1]}")
                    dico_mem['Scenario_' + str(nbr_S)] = \
                        {'DataFrame': my_df_jourJ.copy(deep=True), 'vente': vente, 'achat': achat}

                    #print(f"dico_mem['Scenario_' + str(nbr_S)] = \n{dico_mem['Scenario_' + str(nbr_S)]}")

                    # Enregistrement evolution des scenarii
                    if jour == 0:
                        my_df_jourJ.to_csv(r'/Users/stephanecau/PycharmProjects/StecauApps/FinancialApp/tmp/'
                                           r'surrogate_model_' + str(nbr_S) + '.csv', index=True)
                    else:
                        #print(f"data =\n{my_df_jourJ.values[1]}")
                        #print(f"index =\n{my_df_jourJ.index[1]}")
                        #print(f"columns =\n{l_columns}")
                        my_df_jourJ_tmp = pd.DataFrame(data=[my_df_jourJ.values[1]], index=[my_df_jourJ.index[1]],
                                                       columns=my_df_jourJ.columns)
                        #print(f"my_df_jourJ_tmp = \n{my_df_jourJ_tmp}")
                        my_df_jourJ_fromCSV = pd.read_csv(r'/Users/stephanecau/PycharmProjects/StecauApps/FinancialApp/'
                                                          r'tmp/surrogate_model_' + str(nbr_S) + '.csv', index_col=0)
                        #print(f"my_df_jourJ = \n{my_df_jourJ}")
                        my_df_jourJ_fromCSV = my_df_jourJ_fromCSV.append(my_df_jourJ_tmp, ignore_index=False)
                        #print(f"my_df_jourJ = \n{my_df_jourJ}")
                        my_df_jourJ_fromCSV.to_csv(r'/Users/stephanecau/PycharmProjects/StecauApps/FinancialApp/tmp/'
                                                   r'surrogate_model_' + str(nbr_S) + '.csv', index=True)

                    # Stockage info de dataframe principal
                    l_columns = list()
                    l_values = list()
                    l_values.append(list())
                    # Param Vente
                    for key, value in model_vente.items():
                        if key == "pente" or key == "comparaison":
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
                        if key == "pente" or key == "comparaison":
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
                    l_values[0].append(my_df_jourJ['Scenario'].values[-1])
                    #print(l_columns)
                    #print(l_values)
                    df_tempo = pd.DataFrame(data=l_values, index=['Scenario_' + str(nbr_S)], columns=l_columns)
                    #print(df_tempo)
                    df_final = df_final.append(df_tempo, ignore_index=False)
                    #print(df_final)

                    dico_my_df_graph['Scenario_' + str(nbr_S)] = my_df_jourJ['Scenario'].values[1]

        # Iteration sur l'année 2019 Scenario1 sans Sécurisation
        if bool_S1_ssSecu:
            # Rajout des valeurs specifiques
            my_df_jourJ['Mise'] = 100.
            my_df_jourJ['Secu'] = 0.
            my_df_jourJ['PorteFeuille'] = 0.
            my_df_jourJ['NbrAction'] = 0.
            my_df_jourJ['Vente'] = False
            my_df_jourJ['Achat'] = False
            my_df_jourJ['ValeurAchat'] = np.NaN
            my_df_jourJ['ValeurVente'] = np.NaN
            my_df_jourJ['Scenario1_ssSecu'] = 0.

            # Initialisation du premier achat
            my_df_jourJ['Mise'].values[0] = 0.
            my_df_jourJ['PorteFeuille'].values[0] = nbr_action * my_df_jourJ['Close'].values[0]
            my_df_jourJ['NbrAction'].values[0] = nbr_action
            my_df_jourJ['Achat'].values[0] = True
            my_df_jourJ['ValeurAchat'].values[0] = valeur_action
            my_df_jourJ['Scenario1_ssSecu'].values[0] = my_df_jourJ['Mise'].values[0] + my_df_jourJ['Secu'].values[0] + my_df_jourJ['PorteFeuille'].values[0]
            vente = False
            achat = True
            inc = 0
            for i, my_ligne in enumerate(my_df_jourJ.index):
                if i > 0:
                    my_df_jourJ['Mise'].values[i] = my_df_jourJ['Mise'].values[i - 1]
                    my_df_jourJ['Secu'].values[i] = my_df_jourJ['Secu'].values[i - 1]
                    my_df_jourJ['NbrAction'].values[i] = my_df_jourJ['NbrAction'].values[i - 1]
                    my_df_jourJ['PorteFeuille'].values[i] = my_df_jourJ['Close'].values[i] * my_df_jourJ['NbrAction'].values[i]
                    my_df_jourJ['ValeurAchat'].values[i] = my_df_jourJ['ValeurAchat'].values[i - 1]
                    my_df_jourJ['ValeurVente'].values[i] = my_df_jourJ['ValeurVente'].values[i - 1]
                    my_df_jourJ['Scenario1_ssSecu'].values[i] = my_df_jourJ['Mise'].values[i] + my_df_jourJ['Secu'].values[i] + \
                                                   my_df_jourJ['PorteFeuille'].values[i]

                #print(my_df_jourJ.iloc[i])
                if achat:  # On possède des actions
                    # Regarde si vente
                    if i > 5:
                        # vente si diminution de l'action qui provoque diminution moyenne 2j, 3j, 4j et 7j (pente inf à -0,05) et
                        # valeur plus basse qu'il y a 14j ou pente négative de plus de 0,8
                        if not bool_pente('Close', i, my_df_jourJ) and \
                                not bool_pente('J2', i, my_df_jourJ) and \
                                not bool_pente('J3', i, my_df_jourJ) and \
                                not bool_pente('J4', i, my_df_jourJ) and \
                                not bool_pente('J7', i, my_df_jourJ, -0.05) and \
                                (my_df_jourJ['Close'].values[i] <= my_df_jourJ['Close'].values[i - 10] or
                                 not bool_pente('J2', i, my_df_jourJ, -0.8)):
                            vente = True
                        else:  # on ne vend pas
                            vente = False
                # print('Vente ?')
                if vente and achat:  # on va vendre, on ne possèdera plus d'action
                    my_df_jourJ['Vente'].values[i] = True
                    my_df_jourJ['Achat'].values[i] = False
                    my_df_jourJ['Mise'].values[i] = my_df_jourJ['Close'].values[i] * my_df_jourJ['NbrAction'].values[i]
                    my_df_jourJ['Secu'].values[i] += 0.
                    my_df_jourJ['PorteFeuille'].values[i] = 0.
                    my_df_jourJ['NbrAction'].values[i] = 0.
                    my_df_jourJ['ValeurVente'].values[i] = my_df_jourJ['Close'].values[i]
                    my_df_jourJ['ValeurAchat'].values[i] = np.NaN
                    my_df_jourJ['Scenario1_ssSecu'].values[i] = my_df_jourJ['Mise'].values[i] + my_df_jourJ['Secu'].values[i] + \
                                                   my_df_jourJ['PorteFeuille'].values[i]
                    #print(my_df_jourJ.iloc[i])
                    print(f"VENTE (Date : {my_df_jourJ.index[i]}) :\n     Mise : {my_df_jourJ['Mise'].values[i]}\n"
                          f"     Sécurisé : {my_df_jourJ['Secu'].values[i]}\n"
                          f"     Valeur d'achat : {my_df_jourJ['ValeurAchat'].values[i - 1]}\n"
                          f"     Valeur de vente : {my_df_jourJ['ValeurVente'].values[i]}")
                    achat = False
                # print('achat ?')
                if vente and not achat and not my_df_jourJ['Vente'].values[i] and not my_df_jourJ['Achat'].values[i]:
                    # On a vendu et pas encore racheté.
                    # Conditions pour rachat:
                    # La valeur de vente <= à la valeur de l'action et on n'a pas vendu le jour d'avant OU
                    # La pente de l'action ainsi que J2 et J3 sont positives
                    if my_df_jourJ['ValeurVente'].values[i] <= my_df_jourJ['Close'].values[i] and not my_df_jourJ['Vente'].values[i - 1] \
                            or bool_pente('Close', i, my_df_jourJ) and bool_pente('J2', i, my_df_jourJ) and bool_pente('J3', i, my_df_jourJ):
                        my_df_jourJ['Vente'].values[i] = False
                        my_df_jourJ['Achat'].values[i] = True
                        achat = True
                        vente = False
                        my_df_jourJ['Mise'].values[i] = 0.
                        my_df_jourJ['Secu'].values[i] = my_df_jourJ['Secu'].values[i - 1]
                        my_df_jourJ['NbrAction'].values[i] = my_df_jourJ['Mise'].values[i - 1] / my_df_jourJ['Close'].values[i]
                        my_df_jourJ['PorteFeuille'].values[i] = my_df_jourJ['Close'].values[i] * my_df_jourJ['NbrAction'].values[i]
                        my_df_jourJ['ValeurAchat'].values[i] = my_df_jourJ['Close'].values[i]
                        my_df_jourJ['ValeurVente'].values[i] = np.NaN
                        my_df_jourJ['Scenario1_ssSecu'].values[i] = my_df_jourJ['Mise'].values[i] + my_df_jourJ['Secu'].values[i] + \
                                                       my_df_jourJ['PorteFeuille'].values[i]
                        #print(my_df_jourJ.iloc[i])
                        print(f"ACHAT (Date : {my_df_jourJ.index[i]}) :\n     PorteFeuille : {my_df_jourJ['PorteFeuille'].values[i]}\n"
                              f"     Sécurisé : {my_df_jourJ['Secu'].values[i]}\n"
                              f"     Nbr Action(s) : {my_df_jourJ['NbrAction'].values[i]}\n"
                              f"     Valeur d'achat : {my_df_jourJ['ValeurAchat'].values[i]}\n"
                              f"     Valeur de vente : {my_df_jourJ['ValeurVente'].values[i - 1]}")
                inc += 1

            #print(my_df_jourJ.tail(10))
            print(f"A LA FIN (Date : {my_df_jourJ.index[-1]}) :\n     PorteFeuille : {my_df_jourJ['PorteFeuille'].values[-1]}\n"
                  f"     Nbr Action(s) : {my_df_jourJ['NbrAction'].values[-1]}\n"
                  f"     Sécurisé : {my_df_jourJ['Secu'].values[-1]}\n"
                  f"     Mise : {my_df_jourJ['Mise'].values[-1]}")

        # Iteration sur l'année 2019 Scenario1 Nbr Action Constante
        if bool_S1_NbrActionCste:
            # Rajout des valeurs specifiques
            my_df_jourJ['Mise'] = 100.
            my_df_jourJ['Secu'] = 0.
            my_df_jourJ['PorteFeuille'] = 0.
            my_df_jourJ['NbrAction'] = 0.
            my_df_jourJ['Vente'] = False
            my_df_jourJ['Achat'] = False
            my_df_jourJ['ValeurAchat'] = np.NaN
            my_df_jourJ['ValeurVente'] = np.NaN
            my_df_jourJ['Scenario1_NbrActionCste'] = 0.

            # Initialisation du premier achat
            my_df_jourJ['Mise'].values[0] = 0.
            my_df_jourJ['PorteFeuille'].values[0] = nbr_action * my_df_jourJ['Close'].values[0]
            my_df_jourJ['NbrAction'].values[0] = nbr_action
            my_df_jourJ['Achat'].values[0] = True
            my_df_jourJ['ValeurAchat'].values[0] = valeur_action
            my_df_jourJ['Scenario1_NbrActionCste'].values[0] = my_df_jourJ['Mise'].values[0] + my_df_jourJ['Secu'].values[0] + \
                                                         my_df_jourJ['PorteFeuille'].values[0]
            vente = False
            achat = True
            inc = 0
            for i, my_ligne in enumerate(my_df_jourJ.index):
                if i > 0:
                    my_df_jourJ['Mise'].values[i] = my_df_jourJ['Mise'].values[i - 1]
                    my_df_jourJ['Secu'].values[i] = my_df_jourJ['Secu'].values[i - 1]
                    my_df_jourJ['NbrAction'].values[i] = my_df_jourJ['NbrAction'].values[i - 1]
                    my_df_jourJ['PorteFeuille'].values[i] = my_df_jourJ['Close'].values[i] * my_df_jourJ['NbrAction'].values[i]
                    my_df_jourJ['ValeurAchat'].values[i] = my_df_jourJ['ValeurAchat'].values[i - 1]
                    my_df_jourJ['ValeurVente'].values[i] = my_df_jourJ['ValeurVente'].values[i - 1]
                    my_df_jourJ['Scenario1_NbrActionCste'].values[i] = my_df_jourJ['Mise'].values[i] + my_df_jourJ['Secu'].values[i] + \
                                                                 my_df_jourJ['PorteFeuille'].values[i]

                #print(my_df_jourJ.iloc[i])
                if achat:  # On possède des actions
                    # Regarde si vente
                    if i > 5:
                        # vente si diminution de l'action qui provoque diminution moyenne 2j, 3j, 4j et 7j (pente inf à -0,05) et
                        # valeur plus basse qu'il y a 14j ou pente négative de plus de 0,8
                        if not bool_pente('Close', i, my_df_jourJ) and \
                                not bool_pente('J2', i, my_df_jourJ) and \
                                not bool_pente('J3', i, my_df_jourJ) and \
                                not bool_pente('J4', i, my_df_jourJ) and \
                                not bool_pente('J7', i, my_df_jourJ, -0.05) and \
                                (my_df_jourJ['Close'].values[i] <= my_df_jourJ['Close'].values[i - 10] or
                                 not bool_pente('J2', i, my_df_jourJ, -0.8)):
                            vente = True
                        else:  # on ne vend pas
                            vente = False
                # print('Vente ?')
                if vente and achat:  # on va vendre, on ne possèdera plus d'action
                    my_df_jourJ['Vente'].values[i] = True
                    my_df_jourJ['Achat'].values[i] = False
                    my_df_jourJ['Mise'].values[i] = my_df_jourJ['Close'].values[i] * my_df_jourJ['NbrAction'].values[i]
                    my_df_jourJ['Secu'].values[i] += 0.
                    my_df_jourJ['PorteFeuille'].values[i] = 0.
                    my_df_jourJ['NbrAction'].values[i] = 0.
                    my_df_jourJ['ValeurVente'].values[i] = my_df_jourJ['Close'].values[i]
                    my_df_jourJ['ValeurAchat'].values[i] = np.NaN
                    my_df_jourJ['Scenario1_NbrActionCste'].values[i] = my_df_jourJ['Mise'].values[i] + my_df_jourJ['Secu'].values[i] + \
                                                                 my_df_jourJ['PorteFeuille'].values[i]
                    #print(my_df_jourJ.iloc[i])
                    print(f"VENTE (Date : {my_df_jourJ.index[i]}) :\n     Mise : {my_df_jourJ['Mise'].values[i]}\n"
                          f"     Sécurisé : {my_df_jourJ['Secu'].values[i]}\n"
                          f"     Valeur d'achat : {my_df_jourJ['ValeurAchat'].values[i - 1]}\n"
                          f"     Valeur de vente : {my_df_jourJ['ValeurVente'].values[i]}")
                    achat = False
                # print('achat ?')
                if vente and not achat and not my_df_jourJ['Vente'].values[i] and not my_df_jourJ['Achat'].values[i]:
                    # On a vendu et pas encore racheté.
                    # Conditions pour rachat:
                    # La valeur de vente <= à la valeur de l'action et on n'a pas vendu le jour d'avant OU
                    # La pente de l'action ainsi que J2 et J3 sont positives
                    if my_df_jourJ['ValeurVente'].values[i] <= my_df_jourJ['Close'].values[i] and not my_df_jourJ['Vente'].values[i - 1] \
                            or bool_pente('Close', i, my_df_jourJ) and bool_pente('J2', i, my_df_jourJ) and bool_pente('J3', i, my_df_jourJ):
                        my_df_jourJ['Vente'].values[i] = False
                        my_df_jourJ['Achat'].values[i] = True
                        achat = True
                        vente = False
                        if my_df_jourJ['Mise'].values[i] + my_df_jourJ['Secu'].values[i] >= nbr_action * my_df_jourJ['Close'].values[i]:
                            my_df_jourJ['Secu'].values[i] = my_df_jourJ['Mise'].values[i] + my_df_jourJ['Secu'].values[i] - \
                                                      (nbr_action * my_df_jourJ['Close'].values[i])
                            my_df_jourJ['Mise'].values[i] = 0.
                            my_df_jourJ['NbrAction'].values[i] = nbr_action
                        else:
                            my_df_jourJ['NbrAction'].values[i] = (my_df_jourJ['Mise'].values[i] + my_df_jourJ['Secu'].values[i]) / \
                                                           my_df_jourJ['Close'].values[i]
                            my_df_jourJ['Secu'].values[i] = 0.
                            my_df_jourJ['Mise'].values[i] = 0.
                        my_df_jourJ['PorteFeuille'].values[i] = my_df_jourJ['Close'].values[i] * my_df_jourJ['NbrAction'].values[i]
                        my_df_jourJ['ValeurAchat'].values[i] = my_df_jourJ['Close'].values[i]
                        my_df_jourJ['ValeurVente'].values[i] = np.NaN
                        my_df_jourJ['Scenario1_NbrActionCste'].values[i] = my_df_jourJ['Mise'].values[i] + my_df_jourJ['Secu'].values[i] + \
                                                                     my_df_jourJ['PorteFeuille'].values[i]
                        #print(my_df_jourJ.iloc[i])
                        print(f"ACHAT (Date : {my_df_jourJ.index[i]}) :\n     PorteFeuille : {my_df_jourJ['PorteFeuille'].values[i]}\n"
                              f"     Sécurisé : {my_df_jourJ['Secu'].values[i]}\n"
                              f"     Nbr Action(s) : {my_df_jourJ['NbrAction'].values[i]}\n"
                              f"     Valeur d'achat : {my_df_jourJ['ValeurAchat'].values[i]}\n"
                              f"     Valeur de vente : {my_df_jourJ['ValeurVente'].values[i - 1]}")
                inc += 1

            #print(my_df_jourJ.tail(10))
            print(f"A LA FIN (Date : {my_df_jourJ.index[-1]}) :\n     PorteFeuille : {my_df_jourJ['PorteFeuille'].values[-1]}\n"
                  f"     Nbr Action(s) : {my_df_jourJ['NbrAction'].values[-1]}\n"
                  f"     Sécurisé : {my_df_jourJ['Secu'].values[-1]}\n"
                  f"     Mise : {my_df_jourJ['Mise'].values[-1]}")

        if jour == 0:
            my_df_graph = pd.DataFrame(data=dico_my_df_graph,
                                       index=[my_df_jourJ['SansTransaction'].index[1]])
        else:
            my_df_graph_temp = pd.DataFrame(data=dico_my_df_graph,
                                       index=[my_df_jourJ['SansTransaction'].index[1]])
            my_df_graph = my_df_graph.append(my_df_graph_temp)
        #print(f"my_df_graph :\n{my_df_graph}")

my_df_graph.to_csv(r'/Users/stephanecau/PycharmProjects/StecauApps/FinancialApp/'
                   r'simu_surrogate_small.csv', index=True)

df_final.to_csv(r'/Users/stephanecau/PycharmProjects/StecauApps/FinancialApp/'
                r'simu_surrogate_small_sumup.csv', index=True)

# Visualisation
if 1:
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.plot(my_df_graph.index, my_df_graph['Close'], label='Action Apple')
    #ax.plot(my_df_jourJ.index, my_df_jourJ['Mise'], label='Evolution de la mise')
    #ax.plot(my_df_jourJ.index, my_df_jourJ['Secu'], label='Evolution de la Sécurisation')
    #ax.plot(my_df_jourJ.index, my_df_jourJ['PorteFeuille'], label='Evolution du PorteFeuille')
    #ax.plot(my_df_jourJ.index, my_df_jourJ['NbrAction'], label="Evolution du nombre d'actions")
    ax.plot(my_df_graph.index, my_df_graph['SansTransaction'], label='Evolution du Total Sans Transaction')
    if bool_Max:
        ax.plot(my_df_graph.index, my_df_graph['MaxRendement'], label='Evolution du Total Rendement Max')
    if bool_Max_ssSecu:
        ax.plot(my_df_graph.index, my_df_graph['MaxRendement_ssSecu'], label='Evolution du Total Rendement Max sans sécurisation')
    if bool_Max_NbrActionCste:
        ax.plot(my_df_graph.index, my_df_graph['MaxRendement_NbrActionCste'], label='Evolution du Total Rendement Max '
                                                                        'avec Nbr Action cste')
    if bool_S1:
        for num in range(0, nbr_S + 1, 1):
            ax.plot(my_df_graph.index, my_df_graph['Scenario_' + str(num)], label='Evolution du Total Scenario ' + str(num))
    if bool_S1_ssSecu:
        ax.plot(my_df_graph.index, my_df_graph['Scenario1_ssSecu'], label='Evolution du Total Scenario1 sans sécurisation')
    if bool_S1_NbrActionCste:
        ax.plot(my_df_graph.index, my_df_graph['Scenario1_NbrActionCste'], label='Evolution du Scenario1 avec Nbr Action cste')
    ax.set_xlabel('Date')
    ax.set_ylabel('Valeur de fermeture')
    ax.legend()
    plt.show()

if 1:
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.plot(my_df_full.index, my_df_full['Close'], label='Apple')
    ax.plot(my_df_full.index, my_df_full['J2'], label='Apple moyenne sur 2 jours')
    ax.plot(my_df_full.index, my_df_full['J3'], label='Apple moyenne sur 3 jours')
    ax.plot(my_df_full.index, my_df_full['J5'], label='Apple moyenne sur 5 jours')
    ax.plot(my_df_full.index, my_df_full['J10'], label='Apple moyenne sur 10 jours')
    ax.plot(my_df_full.index, my_df_full['J15'], label='Apple moyenne sur 15 jours')
    ax.plot(my_df_full.index, my_df_full['J20'], label='Apple moyenne sur 20 jours')
    ax.set_xlabel('Date')
    ax.set_ylabel('Valeur de fermeture')
    ax.legend()
    plt.show()

if 0:
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.plot(df_final.index, df_final['Total'], label='Resultats scenarii')
    #ax.plot(my_df_jourJ.index, my_df_jourJ['Mise'], label='Evolution de la mise')
    #ax.plot(my_df_jourJ.index, my_df_jourJ['Secu'], label='Evolution de la Sécurisation')
    #ax.plot(my_df_jourJ.index, my_df_jourJ['PorteFeuille'], label='Evolution du PorteFeuille')
    #ax.plot(my_df_jourJ.index, my_df_jourJ['NbrAction'], label="Evolution du nombre d'actions")
    #ax.plot(my_df_jourJ.index, my_df_jourJ['SansTransaction'], label='Evolution du Total Sans Transaction')
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