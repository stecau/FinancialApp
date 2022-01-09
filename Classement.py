import pandas as pd


class Classement:
    def __init__(self, l_actions):
        pt_init = 50.
        self.classement = dict()
        self.total = pt_init * len(l_actions)
        dico_extremum = dict()
        for action in l_actions:
            self.classement[action.nom] = {"Classement": pt_init}
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
            total += value['Classement']
            print(action, value['Classement'])
        print(total)

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
            if value['J5'] == moyenne.at['J5']:
                value['Classement'] = moyenne.at['Classement']
            elif value['J5'] < moyenne.at['J5'] - 6 * sigma.at['J5']:
                value['Classement'] = 0
            elif moyenne.at['J5'] - 6 * sigma.at['J5'] < value['J5'] <= moyenne.at['J5'] - 5 * sigma.at['J5']:
                value['Classement'] = pt_init - 6 * (nbr_pt_datakey / 12)
            elif moyenne.at['J5'] - 5 * sigma.at['J5'] < value['J5'] <= moyenne.at['J5'] - 4 * sigma.at['J5']:
                value['Classement'] = pt_init - 5 * (nbr_pt_datakey / 12)
            elif moyenne.at['J5'] - 4 * sigma.at['J5'] < value['J5'] <= moyenne.at['J5'] - 3 * sigma.at['J5']:
                value['Classement'] = pt_init - 4 * (nbr_pt_datakey / 12)
            elif moyenne.at['J5'] - 3 * sigma.at['J5'] < value['J5'] <= moyenne.at['J5'] - 2 * sigma.at['J5']:
                value['Classement'] = pt_init - 3 * (nbr_pt_datakey / 12)
            elif moyenne.at['J5'] - 2 * sigma.at['J5'] < value['J5'] <= moyenne.at['J5'] - 1 * sigma.at['J5']:
                value['Classement'] = pt_init - 2 * (nbr_pt_datakey / 12)
            elif moyenne.at['J5'] - 1 * sigma.at['J5'] < value['J5'] < moyenne.at['J5']:
                value['Classement'] = pt_init - 1 * (nbr_pt_datakey / 12)
            elif moyenne.at['J5'] < value['J5'] < moyenne.at['J5'] + 1 * sigma.at['J5']:
                value['Classement'] = pt_init + 1 * (nbr_pt_datakey / 12)
            elif moyenne.at['J5'] + 1 * sigma.at['J5'] <= value['J5'] < moyenne.at['J5'] + 2 * sigma.at['J5']:
                value['Classement'] = pt_init + 2 * (nbr_pt_datakey / 12)
            elif moyenne.at['J5'] + 2 * sigma.at['J5'] <= value['J5'] < moyenne.at['J5'] + 3 * sigma.at['J5']:
                value['Classement'] = pt_init + 3 * (nbr_pt_datakey / 12)
            elif moyenne.at['J5'] + 3 * sigma.at['J5'] <= value['J5'] < moyenne.at['J5'] + 4 * sigma.at['J5']:
                value['Classement'] = pt_init + 4 * (nbr_pt_datakey / 12)
            elif moyenne.at['J5'] + 4 * sigma.at['J5'] <= value['J5'] < moyenne.at['J5'] + 5 * sigma.at['J5']:
                value['Classement'] = pt_init + 5 * (nbr_pt_datakey / 12)
            elif moyenne.at['J5'] + 5 * sigma.at['J5'] <= value['J5'] < moyenne.at['J5'] + 6 * sigma.at['J5']:
                value['Classement'] = pt_init + 6 * (nbr_pt_datakey / 12)
            elif value['J5'] > moyenne.at['J5'] + 6 * sigma.at['J5']:
                value['Classement'] = 100

    def dataframe_datakey(self):
        l_df = list()
        for key, value in self.classement.items():
            #print(f"key = {key}")
            #print(f"value = {value}")
            df = pd.DataFrame(data=value, index=[key])
            l_df.append(df)
        df = pd.concat(l_df, axis=0)
        #print(df)
        return df

