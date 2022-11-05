import datetime as dt
import matplotlib.pyplot as plt
import pandas_datareader as web
import numpy as np
import pandas as pd

class Stock:
    
    def __init__(self, name, original_date, quantity):
        self.__stock = web.DataReader( name, 'yahoo', original_date, dt.date.today() )
        self.__quantity = quantity
        self.__name = name
        self.__memory = self.__stock['Close'].iat[0]
        # print(name)
        
    # Getters
    #--------------------------------------------------------------------------
    def get_stock(self):
        return self.__stock
    
    def get_quantity(self):
        return self.__quantity
    
    def get_memory(self):
        return self.__memory
    
    def set_memory(self, memory):
        self.__memory = memory
    
    def set_quantity(self, qt):
        self.__quantity = qt
    
    def get_name(self):
        return self.__name
    
    def get_price(self, time):
        return 0.5 * ( self.get_stock()['High'].iat[time] + self.get_stock()['Low'].iat[time] )
    
    def get_trade_value( self, date, nb ):
        time = 0
        for dates in self.get_stock().index:
            if dates.date() >= date:
                break
            time += 1
        
        return np.abs(nb) * self.get_stock()['Close'].iat[ time ]
        """
        if nb < 0:
            return - nb * self.get_stock()['Low'].iat[ time ]
        else:
            return nb * self.get_stock()['High'].iat[ time ]
        """
        
    def get_rolling_mean(self, date, days):
        mean_name = 'Mean' + str(days)
        time = 0
        for dates in self.get_stock().index:
            if dates.date() >= date:
                break
            time += 1
        
        if mean_name not in self.get_stock():
            self.rolling_mean( days )
        
        return self.get_stock()[mean_name].iat[time]
            
    
    
    # Functions
    #--------------------------------------------------------------------------
    def rolling_mean(self, days):
        name = 'Mean' + str(days)
        self.__stock[name] = self.get_stock()['Close'].rolling( window=int(days) ).mean()
    
    def rsi(self, period):
        
    
    def plot_datas(self):
        pass
    
    def transaction(self, qt):
        self.__quantity += qt
        
    def value(self, date):
        time = 0
        for dates in self.get_stock().index:
            if dates.date() >= date:
                break
            time += 1
        
        qt = self.get_quantity()
        maxv = self.get_stock()['High'].iat[time]
        minv = self.get_stock()['Low'].iat[time]
        return qt * 0.5 * ( maxv + minv )
    
    def plot_stock(self, mean=True):
        stock = self.get_stock()
        
        fig, ax = plt.subplots( 1, 1 )
        # ax.plot( stock.index, stock['High'], '-', color='red', label="High" )
        # ax.plot( stock.index, stock['Low'], '-', color='blue', label="Low" )
        ax.plot( stock.index, stock['Close'], '-', color='black', label="Close" )
        
        if mean == True:
            for name in stock.columns:
                if name.startswith('Mean'):
                    ax.plot( stock.index, stock[name], '--', label=name )
        
        ax.set_xlabel('date')
        ax.set_ylabel('value')
        ax.legend()
        ax.set_title( self.get_name() )
        
        fig.autofmt_xdate()
        
        figname = "Figures/" + self.get_name() + ".pdf"
        fig.savefig( figname )
        # plt.show(fig)
        plt.close(fig)
        
    
    # Analyse
    #--------------------------------------------------------------------------
    def fit_stock( self, start_date, end_date, fitname ):
        sub_stock = self.get_stock()[ self.get_stock().isin( pd.date_range( start_date, end_date ) ) ]
    
    
    name = property( get_name )
    stock = property( get_stock, transaction )
    quantity = property( get_quantity, set_quantity )    
    memory = property( get_memory, set_memory )