import pandas_datareader.data as web


class Internet:
    def __init__(self):
        pass

    @staticmethod
    def get_actions_df(d_tickers, debut, fin):
        tickers = list()
        for key in d_tickers.keys():
            tickers.append(key)
        df = web.DataReader(tickers, 'yahoo', debut, fin)
        return df
