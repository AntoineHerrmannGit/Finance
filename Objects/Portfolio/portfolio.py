import datetime as dt
import pandas as pd
import numpy as np

from Objects.Stock.stock import Stock

class Portfolio:
    
    def __init__(self, tickers, quantities, original_date, value):
        self.__time = 0
        self.__date = original_date
        self.__dates = []
        self.__dates_initialized = False
        
        self.__wallet = value
        self.__fees = 0
        self.__charges = 1
        
        self.__initial_wallet = value
        self.__security = 0.15 * value
        
        self.init_stocks( tickers, quantities )
        
        self.__wallet_history = [  ]
        self.__value_history = [  ]
        
    
    # Getters
    #--------------------------------------------------------------------------
    def get_time(self):
        return self.__time
    
    def get_date(self):
        return self.__date
    
    def set_date(self, date):
        self.__date = date
    
    def get_dates(self):
        return self.__dates
    
    def get_stocks(self):
        return self.__stocks
    
    def get_stock(self, stock):
        for stocks in self.get_stocks():
            if stocks.get_name() == stock.get_name():
                return stocks
    
    def get_wallet(self):
        return self.__wallet
    
    def get_fees(self):
        return self.__fees
    
    def get_charges(self):
        return self.__charges
    
    def get_value(self):
        value = self.get_wallet()
        for stock in self.get_stocks():
            value += stock.value( self.get_date() )
        return value
    
    def get_wallet_history(self):
        return self.__wallet_history
    
    def get_value_history(self):
        return self.__value_history
    
    # Functions
    #--------------------------------------------------------------------------
    def update_date(self, date):
        self.check_security()
        self.set_date(date)
        self.__value_history.append( [ self.get_date(), self.get_value() ] )
        self.__wallet_history.append( [ self.get_date(), self.get_wallet() ] )
    
    def update_time(self):
        if self.__dates == [] and len( self.get_stocks() ) != 0 and self.__dates_initialized == False:
            self.__dates = self.get_stocks()[0].get_stock()['Close'].index.date.tolist()
            self.__dates_initialized = True
            
        self.__time += 1
        
        if self.__dates != [] and self.__time < len( self.__dates ):
            self.__date = self.__dates[self.__time]
            
        self.check_security()
                
        # if self.get_stocks() != []:
        self.__value_history.append( [ self.get_date(), self.get_value() ] )
        self.__wallet_history.append( [ self.get_date(), self.get_wallet() ] )
        
    def check_security(self):
        if self.get_value() < self.__security:
            for stocks in self.get_stocks():
                self.trade( stocks, -stocks.get_quantity() )
                
                self.delete_stock( stocks.get_name() )
        # for stocks in self.get_stocks():
        #     if stocks.get_trade_value( self.get_date(), 1 ) < stocks.get_memory():
        #         self.trade( stocks, -stocks.get_quantity() )
        
    def init_stocks( self, tickers, quantities ):
        self.__stocks = []
        i = 0
        for name in tickers:
            stock = Stock(name, self.get_date(), quantities[i])
            self.add_stock( stock, quantities[i] )
            i += 1
    
    def contains_stock(self, stock):
        for stocks in self.get_stocks():
            if stocks.get_name == stock.get_name():
                return True
        return False
    
    def add_stock(self, stock, quantity):
        transaction = ( np.sign( quantity ) * self.get_charges() * stock.get_trade_value( self.get_date(), quantity ) + self.get_fees() )
        if self.get_wallet() - transaction >= self.__security:
            stock.set_quantity( quantity )
            stock.set_memory( stock.get_trade_value( self.get_date(), 1 ) )
            self.__stocks.append( stock )
            self.__wallet -= transaction
        # else:
        #     print( "Inadequate funds to trade " + str(ticker) )
    
    def delete_stock(self, ticker):
        i = 0
        for stock in self.__stocks:
            if stock.get_name() == ticker:
                self.__stocks.pop(i)
            i+=1
            
    def sell_all_stock(self, stock):
        for stocks in self.get_stocks():
            if stocks.get_name() == stock.get_name():
                qt = stocks.get_quantity()
                transaction = ( np.sign( qt ) * self.get_charges() * stock.get_trade_value( self.get_date(), qt ) + self.get_fees() )
                stocks.transaction( -qt )
                self.__wallet += transaction
                self.delete_stock( stocks.get_name() )
    
    def trade(self, stock, qt):
        exist = False
        transaction = ( np.sign( qt ) * self.get_charges() * stock.get_trade_value( self.get_date(), qt ) + self.get_fees() )
        for stocks in self.__stocks:
            if stock.get_name() == stocks.get_name():
                exist = True
                if qt >= -stocks.get_quantity() and self.get_wallet() - transaction >= self.__security:
                    stocks.transaction( qt )
                    self.__wallet -= transaction
                    if qt >= 0:
                        stock.set_memory( stock.get_trade_value( self.get_date(), 1 ) )
                    if stocks.get_quantity() == 0:
                        self.delete_stock( stock.get_name() )
                # else:
                #     print( "Not enough stocks to sell" )
                break
        
        if exist == False and qt >= 0:
            self.add_stock(stock, qt)
            
    def make_dataframe(self):
        self.__wallet_history = np.array( self.__wallet_history ).T.tolist()
        self.__wallet_history = pd.DataFrame( self.__wallet_history[1], index=self.__wallet_history[0], columns=['Value'] )
        self.__wallet_history.index.name = 'Date'
        
        self.__value_history = np.array( self.__value_history ).T.tolist()
        self.__value_history = pd.DataFrame( self.__value_history[1], index=self.__value_history[0], columns=['Value'] )
        self.__value_history.index.name = 'Date'
        
    wallet = property( get_wallet, trade, add_stock )
    
    date = property( get_date, set_date, update_time )
    dates = property( update_time )
    dates_initialized = property( get_dates, update_time )
    time = property( get_time, update_time )
    
    security = property( check_security )
    
    stocks = property( get_stocks, init_stocks, add_stock, delete_stock )
    
    fees = property( get_fees )
    charges = property( get_charges )
    
    wallet_history = property( get_wallet_history, update_time, make_dataframe )
    value_history = property( get_value_history, update_time, make_dataframe )