#!/usr/bin/env python
# coding: utf-8

from binance import Client
from datetime import datetime
import pandas as pd 
import pickle
import numpy as np


class AI_1():
    def __init__(self): 
        self.Symbols = pd.read_csv('Symbols.csv')
        print('Symbols Successfully loaded!')
        self.api_key = "b7rLZVf2d60CvEsCEodkRVhNEMHRSRhc4Fxl8zsisz6t8m6YljuOb4JVa6LNjiVm"
        self.api_secret = "3avj294r39BIIUjJJU2IWJv8qGa2eOeH7rUW3fpsWoZkdtWp6lQcigOnPvDyI4EG"
        
        self.model = pickle.load(open('model1.pkl', 'rb'))
        print('Model Loaded Sucsessfully!')  
    
    def makeRawDs(self):
        client = Client(api_key=self.api_key, api_secret= self.api_secret)
        DS = list()
        for symbol in self.Symbols['Symbols'] :
            klines = client.get_historical_klines(symbol, client.KLINE_INTERVAL_1DAY, '12 days ago UTC')
            for Candle in klines :
                date = int(Candle[0]) / 1000
                date = datetime.utcfromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
                Open = Candle[1]
                High = Candle[2]
                Low = Candle[3]
                Close = Candle[4]
                Volume = Candle[5]
                TradeNumber = Candle[8]
                DS.append([symbol, date, Open, High, Low, Close, Volume, TradeNumber])
            DS.pop()
            
        Data = pd.DataFrame(data= DS, columns=['Symbol', 'date', 'Open', 'High', 'Low', 'Close', 'Volume', 'TradeNumber'])
        Data['Open'] = Data['Open'].astype('float')
        Data['High'] = Data['High'].astype('float')
        Data['Low'] = Data['Low'].astype('float')
        Data['Close'] = Data['Close'].astype('float')
        Data['Volume'] = Data['Volume'].astype('float')
        Data['TradeNumber'] = Data['TradeNumber'].astype('float')
        
        return Data
    
    def preProcessDs(self, Data):
        new_datat = []
        num_features = 10
        for x in Data['Symbol'].unique():
            tmpData = Data[Data['Symbol'] == x][['Open', 'High', 'Low','Close', 'Volume', 'TradeNumber']]

            tmpData = tmpData.pct_change() + 1
            tmpData.dropna(inplace=True)
            new_row = tmpData.values.flatten()
            new_datat.append(new_row)

        Columns = []
        for i in range(num_features):
            Columns.append(f'Open_{i}')
            Columns.append(f'High_{i}')
            Columns.append(f'Low_{i}')
            Columns.append(f'Close_{i}')
            Columns.append(f'Volume_{i}')
            Columns.append(f'TN_{i}')
        # Create the new DataFrame with ten features
        new_datasett = pd.DataFrame(new_datat, columns=Columns)
        
        return new_datasett
    
    def predict_today(self, numbers): 
        Data = self.makeRawDs()
        Data = self.preProcessDs(Data)
        predicts = self.model.predict_proba(Data.values)
        
        dic ={}
        i = 0
        for symbol in self.Symbols['Symbols']: 
            dic[symbol] = list(predicts[i])
            i+=1
        sorted_keys = sorted(dic, key=lambda x: dic[x][1], reverse=True)

        #print(sorted_keys[:numbers])
        return sorted_keys[:numbers]   


