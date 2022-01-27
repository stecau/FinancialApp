import pandas as pd
from Action import Action
from Affichage import Affichage


class Classement:
    def __init__(self, l_actions):
        pt_init = 50.
        self.classement = dict()
        self.total = pt_init * len(l_actions)
        dico_extremum = dict()
        for action in l_actions:
            self.classement[action.nom] = {"Classement": {"Total": 0}}
            for label in action.l_labels:
                data_key = label.replace(action.nom + '_', '')
                delta = 5  # evaluation sur 5 jours glissants
                self.classement[action.nom][data_key] = action.comparaison_valeur_x_delta(label, delta)
                if action == l_actions[0]:
                    dico_extremum[data_key] = dict()
                    dico_extremum[data_key]['max'] = action.comparaison_valeur_x_delta(label, delta)
                    dico_extremum[data_key]['min'] = action.comparaison_valeur_x_delta(label, delta)
                else:
                    if dico_extremum[data_key]['max'] < action.comparaison_valeur_x_delta(label, delta):
                        dico_extremum[data_key]['max'] = action.comparaison_valeur_x_delta(label, delta)
                    if dico_extremum[data_key]['min'] > action.comparaison_valeur_x_delta(label, delta):
                        dico_extremum[data_key]['min'] = action.comparaison_valeur_x_delta(label, delta)
        self.calcul_classement(pt_init)
        print(self.total)
        total = 0
        for action, value in self.classement.items():
            total += value['Classement']['Total']
            print(action, value['Classement']['Total'])
        print(total)
        Affichage.affichage_classement(self.classement)

    def calcul_classement(self, pt_init):
        df = self.dataframe_datakey()
        #nbr_datakey = len(df.columns)
        nbr_datakey = 1
        nbr_pt_datakey = pt_init / nbr_datakey
        moyenne = df.mean(axis=0)
        sigma = df.std(axis=0)
        #print(f"moyenne = {moyenne}")
        #print(f"moyenne = {moyenne.at['J5']}")
        #print(f"sigma = {sigma}")
        #print(f"nbr_pt_datakey = {nbr_pt_datakey}")
        # Répartition des points
        for action, value in self.classement.items():
            #print(action, value['J5'], moyenne.at['J5'], sigma.at['J5'])
            #print(f"Action.l_actions[Action.action_index(action)].l_labels = {Action.l_actions[Action.action_index(action)].l_labels}")
            for label in Action.l_actions[Action.action_index(action)].l_labels:
                label = label.replace(Action.l_actions[Action.action_index(action)].nom + '_', '')
                print(f"Action = {Action.l_actions[Action.action_index(action)].nom}")
                print(f"label = {label}")
                if value[label] == moyenne.at[label]:
                    value['Classement'][label] = moyenne.at['Classement']
                elif value[label] < moyenne.at[label] - 6 * sigma.at[label]:
                    value['Classement'][label] = 0
                elif moyenne.at[label] - 6 * sigma.at[label] < value[label] <= moyenne.at[label] - 5 * sigma.at[label]:
                    value['Classement'][label] = pt_init - 6 * (nbr_pt_datakey / 12)
                elif moyenne.at[label] - 5 * sigma.at[label] < value[label] <= moyenne.at[label] - 4 * sigma.at[label]:
                    value['Classement'][label] = pt_init - 5 * (nbr_pt_datakey / 12)
                elif moyenne.at[label] - 4 * sigma.at[label] < value[label] <= moyenne.at[label] - 3 * sigma.at[label]:
                    value['Classement'][label] = pt_init - 4 * (nbr_pt_datakey / 12)
                elif moyenne.at[label] - 3 * sigma.at[label] < value[label] <= moyenne.at[label] - 2 * sigma.at[label]:
                    value['Classement'][label] = pt_init - 3 * (nbr_pt_datakey / 12)
                elif moyenne.at[label] - 2 * sigma.at[label] < value[label] <= moyenne.at[label] - 1 * sigma.at[label]:
                    value['Classement'][label] = pt_init - 2 * (nbr_pt_datakey / 12)
                elif moyenne.at[label] - 1 * sigma.at[label] < value[label] < moyenne.at[label]:
                    value['Classement'][label] = pt_init - 1 * (nbr_pt_datakey / 12)
                elif moyenne.at[label] < value[label] < moyenne.at[label] + 1 * sigma.at[label]:
                    value['Classement'][label] = pt_init + 1 * (nbr_pt_datakey / 12)
                elif moyenne.at[label] + 1 * sigma.at[label] <= value[label] < moyenne.at[label] + 2 * sigma.at[label]:
                    value['Classement'][label] = pt_init + 2 * (nbr_pt_datakey / 12)
                elif moyenne.at[label] + 2 * sigma.at[label] <= value[label] < moyenne.at[label] + 3 * sigma.at[label]:
                    value['Classement'][label] = pt_init + 3 * (nbr_pt_datakey / 12)
                elif moyenne.at[label] + 3 * sigma.at[label] <= value[label] < moyenne.at[label] + 4 * sigma.at[label]:
                    value['Classement'][label] = pt_init + 4 * (nbr_pt_datakey / 12)
                elif moyenne.at[label] + 4 * sigma.at[label] <= value[label] < moyenne.at[label] + 5 * sigma.at[label]:
                    value['Classement'][label] = pt_init + 5 * (nbr_pt_datakey / 12)
                elif moyenne.at[label] + 5 * sigma.at[label] <= value[label] < moyenne.at[label] + 6 * sigma.at[label]:
                    value['Classement'][label] = pt_init + 6 * (nbr_pt_datakey / 12)
                elif value[label] > moyenne.at[label] + 6 * sigma.at[label]:
                    value['Classement'][label] = 100
                value['Classement']['Total'] += value['Classement'][label]

    def dataframe_datakey(self):
        l_df = list()
        for key, value in self.classement.items():
            #print(f"key = {key}")
            #print(f"value = {value}")
            df = pd.DataFrame(data=value, index=[key])
            l_df.append(df)
        df = pd.concat(l_df, axis=0)
        print(df)
        return df

