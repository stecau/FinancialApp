import pandas as pd


class Action:
    l_actions = list()

    def __init__(self, nom, label, code, df):
        self.nom = nom
        self.code = code
        self.label = label

        # Extraction du dataframe spécifique à l'action
        self.df = pd.DataFrame(data=df[label][code].values,
                               index=df.index,
                               columns=['_'.join([self.nom, self.label])])

        # Changement du label de la colonne
        self.label = '_'.join([self.nom, self.label])
        self.l_labels = [self.label]

        # Rajout de l'action dans la liste des actions
        Action.l_actions.append(self)

        # Calcul des moyennes glissantes et rajout dans le dataframe de l'action
        self.calcul_moyenne_glissante(2, self.nom + '_' + 'J2')
        self.calcul_moyenne_glissante(3, self.nom + '_' + 'J3')
        self.calcul_moyenne_glissante(5, self.nom + '_' + 'J5')
        self.calcul_moyenne_glissante(10, self.nom + '_' + 'J10')
        self.calcul_moyenne_glissante(15, self.nom + '_' + 'J15')
        self.calcul_moyenne_glissante(20, self.nom + '_' + 'J20')

    def get_valeur(self, label=None, unique=False, debut=0, fin=0):
        if label is None:
            label = self.label
        if unique:  # return un float
            return float(self.df[label].values[-1])
        else:  # return une liste pandas
            if fin != 0:
                return self.df[label].values[debut:fin]
            return self.df[label].values[debut:]

    def calcul_moyenne_glissante(self, periode, name):
        self.l_labels.append(name)
        self.df[name] = self.df[self.label].rolling(window=periode).mean()

    def bool_pente(self, index, colonne_label, limite=0.):
        # print(index)
        # print(len(dataframe.index) - 1)
        # print(f"dataframe = \n{dataframe}")
        if index <= len(self.df.index) - 1:
            pente = (self.df[colonne_label].values[index] - self.df[colonne_label].values[index - 1]) \
                    / (index - (index - 1))
            # print(f'pente : {pente}')
            if pente >= limite:
                return True
        return False

    def comparaison_valeur_x_delta(self, label, delta):
        return self.df[label].values[-1] - self.df[label].values[-1 - delta]

    # Fonction pour la récupération de l'index de l'action dans la liste des actions à partir de son nom
    @staticmethod
    def action_index(nom):
        for action in Action.l_actions:
            if action.nom == nom:
                return Action.l_actions.index(action)

    # Fonction pour la récupération de l'index du label dans la liste des labels à partir de son nom
    def label_index(self, label):
        for label_action in self.l_labels:
            if label_action == label:
                return self.l_labels.index(label_action)

    # Fonction pour représentation de l'action
    def __str__(self):
        return f"\nL'action : {self.nom} =\n     Code : {self.code}\n     Label : {self.label}\n" \
               f"     N° : {Action.l_actions.index(self) + 1}\n" \
               f"     Dataframe :\n{self.df.head(2)}\n...{self.df.tail(2)}\n"

    def __repr__(self):
        return self.__str__()
