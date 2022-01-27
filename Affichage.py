import matplotlib.pyplot as plt
import pandas as pd

from Action import Action


class Affichage:
    def __init__(self):
        pass

    @staticmethod
    def affichage_actions():
        l_df = list()
        for action in Action.l_actions:
            l_df.append(action.df)
        df = pd.concat(l_df, axis=1)
        df.plot()
        plt.show()

    @staticmethod
    def affichage_selections(df, **kwargs):
        fig, ax = plt.subplots(figsize=(16, 7.5))
        for data, label in kwargs.items():
            ax.plot(df.index, df[data], label=label)
        ax.set_xlabel('Date')
        ax.set_ylabel('Valeur')
        ax.legend()
        plt.show()

    @staticmethod
    def affichage_classement(classement):
        l_df = list()
        for action, value in classement.items():
            # print(f"key = {key}")
            # print(f"value = {value}")
            df = pd.DataFrame(data=value['Classement'], index=[action])
            l_df.append(df)
        df = pd.concat(l_df, axis=0)
        df.plot()
        plt.show()

