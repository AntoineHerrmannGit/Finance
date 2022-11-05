import datetime as dt
# import math
from Objects.Portfolio.portfolio import Portfolio
from Objects.Stock.stock import Stock

class Rolling_mean__strategy:
    
    def __init__(self, tickers, date, period, initial_wallet):
        self.__period = period
        
        self.init_market( tickers, date )
        
        self.__portfolio = Portfolio( [], [], date, initial_wallet )
        
        self.__time = 0
        self.__date = date
        self.__original_date = date
        self.__dates = self.get_market()[0].get_stock()['Close'].index.date.tolist()
        
        self.__daily_count = 1
        self.__weekly_count = 3
        self.__delays = [0, 0]
        self.__efficiency_memory = 0
        self.__memory_counter = 3
        
    # Getters
    #--------------------------------------------------------------------------
    def get_portfolio(self):
        return self.__portfolio
    
    def get_market(self):
        return self.__market
    
    def get_time(self):
        return self.__time
    
    def get_date(self):
        return self.__date
    
    def get_original_date(self):
        return self.__original_date
    
    def get_dates(self):
        return self.__dates
    
    def get_period(self):
        return self.__period
    
    def get_daily_counter(self):
        return self.__daily_count
    
    def get_weekly_counter(self):
        return self.__weekly_count
    
    def get_delays(self):
        return self.__delays
    
    def get_efficiency_memory(self):
        return self.__efficiency_memory
    
    def get_memory_counter(self):
        return self.__memory_counter
    
    
    # Setters
    #--------------------------------------------------------------------------
    def push_daily_counter(self):
        self.__daily_count += 1
    
    def push_weekly_counter(self):
        self.__weekly_count += 1
    
    def set_delays(self, day, week):
        self.__delays = [day, week]
    
    def push_memory_counter(self):
        self.__memory_counter -= 1
    
    def set_efficiency_memory(self, value):
        self.__efficiency_memory = value
    
    # Functions
    #--------------------------------------------------------------------------
    def update_time(self):
        self.__time += 1
        if self.__time < len( self.__dates ):
            self.__date = self.__dates[self.__time]
        self.get_portfolio().update_date(self.get_date())
        
    def update_counters(self, cond):
        if cond and self.get_daily_counter() == 0:
            self.push_daily_counter(1)
            self.set_delays(1, self.get_delays()[1])
        if cond and self.get_weekly_counter() == 0 and self.get_delays()[1] == 0:
            self.push_weekly_counter(1)
            self.set_delays(self.get_delays()[0], 7)
        if self.get_delays()[0] != 0:
            self.set_delays( self.get_delays(self)[0] - 1, self.get_delays(self)[1] )
        if self.get_delays()[1] != 0:
            self.set_delays( self.get_delays(self)[0], self.get_delays(self)[1] - 1 )
        if self.get_memory_counter() != 0:
            self.push_memory_counter()
         
    def plot_stocks(self):
        for stocks in self.get_market():
            stocks.plot_stock()
         
    def init_market(self, tickers, date):
        self.__market = []
        for name in tickers:
            stock = Stock( name, date - dt.timedelta( self.get_period() + 2 ), 0 ) 
            stock.rolling_mean( self.get_period() )
            self.__market.append( stock )
    
    def market_analysis(self, days):
        # cond = False
        # candidate = []
        # efficiency_buy = 0
        # efficiency_sell = 0
        for stocks in self.get_market():
            
            old_buy_value = stocks.get_trade_value( self.get_date() - dt.timedelta(1), 1 )
            old_sell_value = stocks.get_trade_value( self.get_date() - dt.timedelta(1), -1 )
            old_rolling_mean = stocks.get_rolling_mean( self.get_date() - dt.timedelta(1), self.get_period() )
            
            buy_value = stocks.get_trade_value( self.get_date(), 1 )
            sell_value = stocks.get_trade_value( self.get_date(), -1 )
            rolling_mean = stocks.get_rolling_mean( self.get_date(), self.get_period() )
            
            # min_acceptable_value = ( 2*self.get_portfolio().get_charges() * stocks.get_trade_value( self.get_date(), 1 ) - 2*self.get_portfolio().get_fees() )
            min_acceptable_value = 0
            
            qt = 4
            
            if self.get_date() >= self.__original_date and self.get_daily_counter()!= 0 and self.get_weekly_counter() != 0:
                if ( sell_value < min_acceptable_value ) or ( old_sell_value >= old_rolling_mean and sell_value <= rolling_mean ):
                    # self.get_portfolio().trade( stocks, -qt )
                    self.get_portfolio().sell_all_stock( stocks )
                    # print( stocks.get_name() + " sold at " + str( sell_value ) + " on",  self.get_date() )
                    # print( "Stock " + stocks.get_name() + " = ", self.get_portfolio().get_stock( stocks ).get_quantity() )
                    # print( stocks.get_name() + " sold at " + str( sell_value ) )
                
                elif old_buy_value <= old_rolling_mean and buy_value >= rolling_mean:
                    self.get_portfolio().trade( stocks, qt )
                    self.push_memory_counter()
                    self.push_daily_counter()
                    self.push_weekly_counter()
                    self.update_counters(True)
                    # print( stocks.get_name() + " bought at " + str( buy_value ) + " on",  self.get_date() )
                    # print( "Stock " + stocks.get_name() + " = ", self.get_portfolio().get_stock( stocks ).get_quantity() )
                    
                # elif old_sell_value >= old_rolling_mean and sell_value <= rolling_mean:
                #     self.get_portfolio().trade( stocks, -qt )
                #     print( stocks.get_name() + " sold at " + str( sell_value ) + " on",  self.get_date() )
    
    def run(self):
        max_date = self.get_market()[0].get_stock()['Close'].index[-1].date()
        while self.get_date() < max_date:
            print( self.get_date() )
            self.market_analysis( self.get_period() )
            self.update_time()
            
        self.get_portfolio().make_dataframe()
        print( "\n" )
        
    
    market = property( get_market, market_analysis )
    portfolio = property( get_portfolio )
    
    date = property( get_date, update_time )
    original_date = property( get_original_date, market_analysis )
    dates = property( get_dates, update_time )
    time = property( get_time, update_time )
    
    period = property( get_period )
    
    daily_count = property( get_daily_counter, push_daily_counter )
    weekly_count = property( get_weekly_counter, push_weekly_counter )
    delays = property( get_delays, set_delays )
    
    efficiency_memory = property( get_efficiency_memory, set_efficiency_memory )
    memory_counter = property( push_memory_counter )
    
class Naive_strategy:
    
    def __init__(self, tickers, date, period, initial_wallet):
        self.__period = period
        
        self.init_market( tickers, date )
        
        self.__portfolio = Portfolio( [], [], date, initial_wallet )
        
        self.__time = 0
        self.__date = date
        self.__original_date = date
        self.__dates = self.get_market()[0].get_stock()['Close'].index.date.tolist()
        
        self.__daily_count = 1
        self.__weekly_count = 3
        self.__delays = [0, 0]
        self.__efficiency_memory = 0
        self.__memory_counter = 3
        
    # Getters
    #--------------------------------------------------------------------------
    def get_portfolio(self):
        return self.__portfolio
    
    def get_market(self):
        return self.__market
    
    def get_time(self):
        return self.__time
    
    def get_date(self):
        return self.__date
    
    def get_original_date(self):
        return self.__original_date
    
    def get_dates(self):
        return self.__dates
    
    def get_period(self):
        return self.__period
    
    def get_daily_counter(self):
        return self.__daily_count
    
    def get_weekly_counter(self):
        return self.__weekly_count
    
    def get_delays(self):
        return self.__delays
    
    def get_efficiency_memory(self):
        return self.__efficiency_memory
    
    def get_memory_counter(self):
        return self.__memory_counter
    
    
    # Setters
    #--------------------------------------------------------------------------
    def push_daily_counter(self):
        self.__daily_count += 1
    
    def push_weekly_counter(self):
        self.__weekly_count += 1
    
    def set_delays(self, day, week):
        self.__delays = [day, week]
    
    def push_memory_counter(self):
        self.__memory_counter -= 1
    
    def set_efficiency_memory(self, value):
        self.__efficiency_memory = value
    
    # Functions
    #--------------------------------------------------------------------------
    def update_time(self):
        self.__time += 1
        if self.__time < len( self.__dates ):
            self.__date = self.__dates[self.__time]
        self.get_portfolio().update_date(self.get_date())
        
    def update_counters(self, cond):
        if cond and self.get_daily_counter() == 0:
            self.push_daily_counter(1)
            self.set_delays(1, self.get_delays()[1])
        if cond and self.get_weekly_counter() == 0 and self.get_delays()[1] == 0:
            self.push_weekly_counter(1)
            self.set_delays(self.get_delays()[0], 7)
        if self.get_delays()[0] != 0:
            self.set_delays( self.get_delays(self)[0] - 1, self.get_delays(self)[1] )
        if self.get_delays()[1] != 0:
            self.set_delays( self.get_delays(self)[0], self.get_delays(self)[1] - 1 )
        if self.get_memory_counter() != 0:
            self.push_memory_counter()
         
    def plot_stocks(self):
        for stocks in self.get_market():
            stocks.plot_stock()
         
    def init_market(self, tickers, date):
        self.__market = []
        for name in tickers:
            stock = Stock( name, date - dt.timedelta( self.get_period() + 2 ), 0 ) 
            stock.rolling_mean( self.get_period() )
            self.__market.append( stock )
    
    def be_naive(self):
        qt = 4
        for stock in self.get_market():
            if stock.get_trade_value( self.get_date() - dt.timedelta(1), 1 ) > stock.get_trade_value( self.get_date(), 1 ):
                self.get_portfolio().trade( stock, -qt )
            elif stock.get_trade_value( self.get_date() - dt.timedelta(1), 1 ) < stock.get_trade_value( self.get_date(), 1 ):
                self.get_portfolio().trade( stock, qt )
    
    def run(self):
        max_date = self.get_market()[0].get_stock()['Close'].index[-1].date()
        while self.get_date() < max_date:
            print( self.get_date() )
            self.be_naive()
            self.update_time()
            
        self.get_portfolio().make_dataframe()
        print( "\n" )
        
    
    market = property( get_market )
    portfolio = property( get_portfolio )
    
    date = property( get_date, update_time )
    original_date = property( get_original_date )
    dates = property( get_dates, update_time )
    time = property( get_time, update_time )
    
    period = property( get_period )
    
    daily_count = property( get_daily_counter, push_daily_counter )
    weekly_count = property( get_weekly_counter, push_weekly_counter )
    delays = property( get_delays, set_delays )
    
    efficiency_memory = property( get_efficiency_memory, set_efficiency_memory )
    memory_counter = property( push_memory_counter )
        
class Freak_waiter_strategy:
    
    def __init__(self, tickers, date, period, initial_wallet):
        self.__period = period
        
        self.init_market( tickers, date )
        
        self.__portfolio = Portfolio( [], [], date, initial_wallet )
        
        self.__time = 0
        self.__date = date
        self.__original_date = date
        self.__dates = self.get_market()[0].get_stock()['Close'].index.date.tolist()
        
        self.__daily_count = 1
        self.__weekly_count = 3
        self.__delays = [0, 0]
        self.__efficiency_memory = 0
        self.__memory_counter = 3
        
    # Getters
    #--------------------------------------------------------------------------
    def get_portfolio(self):
        return self.__portfolio
    
    def get_market(self):
        return self.__market
    
    def get_time(self):
        return self.__time
    
    def get_date(self):
        return self.__date
    
    def get_original_date(self):
        return self.__original_date
    
    def get_dates(self):
        return self.__dates
    
    def get_period(self):
        return self.__period
    
    def get_daily_counter(self):
        return self.__daily_count
    
    def get_weekly_counter(self):
        return self.__weekly_count
    
    def get_delays(self):
        return self.__delays
    
    def get_efficiency_memory(self):
        return self.__efficiency_memory
    
    def get_memory_counter(self):
        return self.__memory_counter
    
    
    # Setters
    #--------------------------------------------------------------------------
    def push_daily_counter(self):
        self.__daily_count += 1
    
    def push_weekly_counter(self):
        self.__weekly_count += 1
    
    def set_delays(self, day, week):
        self.__delays = [day, week]
    
    def push_memory_counter(self):
        self.__memory_counter -= 1
    
    def set_efficiency_memory(self, value):
        self.__efficiency_memory = value
    
    # Functions
    #--------------------------------------------------------------------------
    def update_time(self):
        self.__time += 1
        if self.__time < len( self.__dates ):
            self.__date = self.__dates[self.__time]
        self.get_portfolio().update_date(self.get_date())
        
    def update_counters(self, cond):
        if cond and self.get_daily_counter() == 0:
            self.push_daily_counter(1)
            self.set_delays(1, self.get_delays()[1])
        if cond and self.get_weekly_counter() == 0 and self.get_delays()[1] == 0:
            self.push_weekly_counter(1)
            self.set_delays(self.get_delays()[0], 7)
        if self.get_delays()[0] != 0:
            self.set_delays( self.get_delays(self)[0] - 1, self.get_delays(self)[1] )
        if self.get_delays()[1] != 0:
            self.set_delays( self.get_delays(self)[0], self.get_delays(self)[1] - 1 )
        if self.get_memory_counter() != 0:
            self.push_memory_counter()
         
    def plot_stocks(self):
        for stocks in self.get_market():
            stocks.plot_stock()
         
    def init_market(self, tickers, date):
        self.__market = []
        for name in tickers:
            stock = Stock( name, date - dt.timedelta( self.get_period() + 2 ), 0 ) 
            stock.rolling_mean( self.get_period() )
            self.__market.append( stock )
    
    def be_freak(self):
        qt = 4
        for stock in self.get_market():
            if stock.get_trade_value( self.get_date() - dt.timedelta(1), 1 ) > stock.get_trade_value( self.get_date(), 1 ):
                self.get_portfolio().trade( stock, -qt )
            elif ( stock.get_trade_value( self.get_date() - dt.timedelta(1), 1 ) < stock.get_trade_value( self.get_date(), 1 ) ) and ( self.get_portfolio().contains_stock(stock) == False ):
                self.get_portfolio().trade( stock, qt )
    
    def run(self):
        max_date = self.get_market()[0].get_stock()['Close'].index[-1].date()
        while self.get_date() < max_date:
            print( self.get_date() )
            self.be_freak()
            self.update_time()
            
        self.get_portfolio().make_dataframe()
        print( "\n" )

    
    market = property( get_market )
    portfolio = property( get_portfolio )
    
    date = property( get_date, update_time )
    original_date = property( get_original_date )
    dates = property( get_dates, update_time )
    time = property( get_time, update_time )
    
    period = property( get_period )
    
    daily_count = property( get_daily_counter, push_daily_counter )
    weekly_count = property( get_weekly_counter, push_weekly_counter )
    delays = property( get_delays, set_delays )
    
    efficiency_memory = property( get_efficiency_memory, set_efficiency_memory )
    memory_counter = property( push_memory_counter )




