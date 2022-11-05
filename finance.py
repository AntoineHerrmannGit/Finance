import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pandas_datareader as web
import inspect

from Objects.Portfolio.portfolio import Portfolio
from Objects.Strategy.strategy import *

def retrieve_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    var_names = [var_name for var_name, var_val in callers_local_vars if var_val is var]
    return [nem for nem in var_names if not nem.startswith('_')][0]

if __name__ == "__main__":
    
    # import starting and ending dates for datas
    # start = dt.date( 2022, 1, 1 )
    # end = dt.date.today()
    
    # list of stocks to import
    tickers = [ # 'EUR/USD', 'EUR/CHF', 'CHF/USD', 'BTC/USD', 'USD/EUR', 'CHF/EUR', 'USD/BTC', 'ETH/USD', 'USD/ETH', 
                # 'S&P 500', 'CAC 40', 'NASDAQ',  
                'AAPL', 'MSFT', 'GOOGL', 'TWTR', 'META', 'AMZN', 'SONY', 'DIS', 
                'CS', 'ACA', 'HSBC', 'BLK', 'BAC', 'JPM', 'WU', 'MA', 
                'OR', 'BABA', 
                'AI', 'DG', 'MT', 
                'FORD', 'MBGYY', 'TM', 'ML', 
                'TTE', 'SHEL', 
                'UBER', 'LYFT', 'SBUX', 'MCD', 'KO', 
                'TMUS', 
                'HPQ', 'DELL', 'INTC', 'AMD', 'NVDA', 'WDC', 'STX', 
                'WMT', 'TGT', 
                'ADP', 'AIR', 'RYAAY', 'BA', 
                'SAN'
              ]
    
    # import datas from yahoo finance
    # datas = web.DataReader( tickers, 'yahoo', start, end )
    
    # quantities = [ 1 for i in tickers ]
    # portfolio = Portfolio( tickers, quantities, dt.date(2010, 1, 1), 10000 )
    
    initial_wallet = 2000
    
    print( "Running brutal strategy... \n")
    roll = Rolling_mean__strategy(tickers, dt.date.today() - dt.timedelta(365), 5, initial_wallet)
    roll.run()
    roll_value = roll.get_portfolio().get_value_history()
    
    print( "Running naive strategy... \n")
    naive = Naive_strategy(tickers, dt.date.today() - dt.timedelta(365), 5, initial_wallet)
    naive.run()
    naive_value = naive.get_portfolio().get_value_history()
    
    print( "Running freak waiter strategy... \n")
    freak = Freak_waiter_strategy(tickers, dt.date.today() - dt.timedelta(365), 5, initial_wallet)
    freak.run()
    freak_value = freak.get_portfolio().get_value_history()
    
    print( "Plotting \n")
    ref = np.array( [ [ i, initial_wallet ] for i in roll_value.index ] ).T.tolist()
    ref = pd.DataFrame( ref[1], index=ref[0], columns=['Initial wallet'] )
    ref.index.name = 'Date'
    
    fig, ax = plt.subplots( 1, 1 )
    # ax.plot( wallet.index, wallet['Value'], label="Wallet" )
    ax.plot( roll_value.index, roll_value['Value'], label="Rolling Mean Strategy" )
    ax.plot( naive_value.index, naive_value['Value'], label="Naive Strategy" )
    ax.plot( freak_value.index, freak_value['Value'], label="Freak waiter Strategy" )
    ax.plot( ref.index, ref['Initial wallet'], color = 'black', label="Initial Deposit" )
    ax.set_xlabel('date')
    ax.set_ylabel('')
    # ax.set_ylim( 0.9*wallet['Value'].min(), 1.1*wallet['Value'].max() )
    ax.legend()
    fig.autofmt_xdate()
    fig.savefig( "Figures/Portfolio.pdf" )
    plt.close(fig)
    
    """
    # plot datas
    # datas['Close'].plot()
    
    # compute rolling average over 10 days
    datas['Mean10'] = datas['Close'].rolling( window=10 ).mean()
    
    # plot datas and rolling average
    fig, ax = plt.subplots( 1, 1 )
    ax.plot( datas.index, datas['Close'], label="AAPL" )
    ax.plot( datas.index, datas['Mean10'], label="Mean10" )
    ax.set_xlabel('date')
    ax.set_ylabel('closing value')
    ax.legend()
    """
    
    