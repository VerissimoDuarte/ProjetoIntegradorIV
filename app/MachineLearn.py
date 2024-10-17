from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import itertools
import numpy as np
import warnings
from datetime import datetime

class MachineLearn(object):
    def __init__(self) -> None:
        self.modelo = None
        self.scaler =  MinMaxScaler()
        warnings.filterwarnings("ignore", category=UserWarning)
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        
    def escalar_dados(self, df: pd.DataFrame) -> pd.DataFrame: 
        df['Valor'] = self.scaler.fit_transform(df[['Valor']])
        return df
        
    def reverter_escalonamento(self, df: pd.DataFrame, coluna_escalada: str) -> pd.DataFrame:
        df[coluna_escalada] = self.scaler.inverse_transform(df[[coluna_escalada]])
        return df
        
    def convertQueryToDateframe(self, query: list, columns: list, periodo: str) -> pd.DataFrame:
        df = pd.DataFrame(query, columns=columns)
        df.rename(columns={'NFDate': 'Date', 'NFValue': 'Valor'}, inplace=True)
        df.set_index('Date', inplace=True)
        df = df.resample(periodo).sum()
        return df
    
    def get_eixos(self, df: pd.DataFrame, xname, yname):
        df = df.round(2)    
        df.reset_index(inplace=True)    
        y = []
        x = []
        for v in df[yname].tolist():
            y.append(v)  
        for data in df[xname].dt.date.tolist():
            x.append(datetime.strftime(data, "%Y-%m-%d"))    
        return x, [y]
             
    def otmizar_modelo(self, df_train: pd.DataFrame):
        p = d = q = range(0, 3)
        sazonal_pdq = [(x[0], x[1], x[2], 12) for x in itertools.product(p, d, q)]

        melhor_aic = np.inf
    
        for param in itertools.product(p, d, q):
            for param_sazonal in sazonal_pdq:
                try:
                    modelo = SARIMAX(df_train['Valor'],
                                    order=param,
                                    seasonal_order=param_sazonal,
                                    enforce_stationarity=False,
                                    enforce_invertibility=False)
                    resultado = modelo.fit(disp=False)
                    if resultado.aic < melhor_aic:
                        melhor_aic = resultado.aic
                        melhor_modelo = resultado
                except:
                    continue

        return melhor_modelo
    
    def getPrevision(self, query: list, columns: list, periodo: str, amostra: int, quantPrevisao: int):
        df_train = self.convertQueryToDateframe(query=query, columns=columns, periodo=periodo)
        df_train = self.escalar_dados(df_train.tail(amostra))
        self.modelo = self.otmizar_modelo(df_train)
        previsao = self.modelo.get_forecast(steps=quantPrevisao)
        mean = previsao.predicted_mean
        mean.index.name = 'Date'
        mean = self.reverter_escalonamento(pd.DataFrame(mean), 'predicted_mean')
        return self.get_eixos(mean, 'Date', 'predicted_mean')