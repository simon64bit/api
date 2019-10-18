# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 19:10:03 2019

@author: Simon Mei
"""


import requests 
import signal
from time import sleep


# this class definition allows us to print error messages and stop the program when needed
class ApiException(Exception):
    pass

# this signal handler allows for a graceful shutdown when CTRL+C is pressed
def signal_handler(signum, frame):
    global shutdown
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    shutdown = True

API_KEY = {'X-API-Key': '6NU20MOO'}
shutdown = False

# this helper method returns the current 'tick' of the running case
def get_tick(session):
    resp = session.get('http://localhost:9999/v1/case')
    if resp.ok:
        case = resp.json()
        return case['tick']
    raise ApiException('The API key provided in this Python code must match that in the RIT client (please refer to the API hyperlink in the client toolbar and/or the RIT – User Guide – REST API Documentation.pdf)')

def get_tickers(session):
    resp = session.get('http://localhost:9999/v1/securities')
    tickers = []
    for dictionary in resp.json():
        tickers.append(dictionary['ticker'])
    return tickers

def pbal(session,ticker): #gets position, bid, ask, last for a security
    resp = session.get('http://localhost:9999/v1/securities?ticker='+ticker)
    sec = resp.json()
    sec = sec[0]
    return [sec['position'],sec['bid'],sec['ask'],sec['last']]


def security_bid_ask(session,ticker):
    payload={'ticker':ticker}
    resp=session.get('http://localhost:9999/v1/securities/book', params=payload)
    if resp.ok:
        book=resp.json()
        return book['bids'][0]['price'], book['asks'][0]['price']



def main():
    with requests.Session() as s:
        s.headers.update(API_KEY)
        tick = get_tick(s)
        tickers = get_tickers(s)
        tenders = s.get('http://localhost:9999/v1/tenders').json()
        while tick > 1 and tick < 299 and not shutdown:
            
            stock1_name='CRKL'
            stock2_name='GOOD'
            stock3_name='LEIA'
            stock4_name='BARU'
            
            stock1_bid, stock1_ask = security_bid_ask(s, stock1_name)
            stock2_bid, stock2_ask = security_bid_ask(s, stock2_name)
            stock3_bid, stock3_ask = security_bid_ask(s, stock3_name)
            stock4_bid, stock4_ask = security_bid_ask(s, stock4_name)
            
            
            c1 = (2*0.05)+0.02
            c2 = (2*0.05)+0.02 
            c3 = (2*0.03)+0.02
            c4 = (2*0.02)+0.02      #commissions

            
#            if stock1_bid-c1 < stock1_ask:
#                s.post('http://localhost:9999/v1/orders', params={'ticker': stock1_name, 'type': 'MARKET', 'quantity': 1000,'action': 'BUY'})
#                s.post('http://localhost:9999/v1/orders', params={'ticker': stock1_name, 'type': 'MARKET', 'quantity': 1000,'action':'SELL'})
#                sleep(0.1)
#            if stock2_bid-c2 < stock2_ask:
#                s.post('http://localhost:9999/v1/orders', params={'ticker': stock2_name, 'type': 'MARKET', 'quantity': 1000,'action': 'BUY'})
#                s.post('http://localhost:9999/v1/orders', params={'ticker': stock2_name, 'type': 'MARKET', 'quantity': 1000,'action':'SELL'})
#                sleep(0.1)
#            if stock3_bid-c3 < stock3_ask:
#                s.post('http://localhost:9999/v1/orders', params={'ticker': stock3_name, 'type': 'MARKET', 'quantity': 1000,'action': 'BUY'})
#                s.post('http://localhost:9999/v1/orders', params={'ticker': stock3_name, 'type': 'MARKET', 'quantity': 1000,'action':'SELL'})
#                sleep(0.1)
#            if stock4_bid-c4 < stock4_ask:
#                s.post('http://localhost:9999/v1/orders', params={'ticker': stock4_name, 'type': 'MARKET', 'quantity': 1000,'action': 'BUY'})
#                s.post('http://localhost:9999/v1/orders', params={'ticker': stock4_name, 'type': 'MARKET', 'quantity': 1000,'action':'SELL'})
#                sleep(0.1)

           
            

            for i in range(len(tenders)):
                tender_id = tenders[i]['tender_id']
                tender_action = tenders[i]['action']
                tender_price = tenders[i]['price']
                tender_fixedbid = tenders[i]['is_fixed_bid']
                tender_ticker = tenders[i]['ticker']
                
                if tender_fixedbid == True:
                    if tender_action == 'BUY' and tender_ticker == stock1_name and stock1_ask+0.05 > tender_price:
                        payload={'id':tender_id,'price':1}
                        s.post('http://localhost:9999/v1/tenders/'+str(tender_id),params=payload)
                        sleep(0.01)
                    if tender_action == 'SELL' and tender_ticker == stock1_name and stock1_bid < tender_price + 0.05:
                        payload={'id':tender_id,'price':1}
                        s.post('http://localhost:9999/v1/tenders/'+str(tender_id),params=payload)
                        sleep(0.01)
                        
                    if tender_action == 'BUY' and tender_ticker == stock2_name and stock2_ask+0.05 > tender_price:
                        payload={'id':tender_id,'price':1}
                        s.post('http://localhost:9999/v1/tenders/'+str(tender_id),params=payload)
                        sleep(0.01)
                        
                    if tender_action == 'SELL' and tender_ticker == stock2_name and stock2_bid < tender_price + 0.05:
                        payload={'id':tender_id,'price':1}
                        s.post('http://localhost:9999/v1/tenders/'+str(tender_id),params=payload)
                        sleep(0.01)
                    
                    if tender_action == 'BUY' and tender_ticker == stock3_name and stock3_ask+0.05 > tender_price:
                        payload={'id':tender_id,'price':1}
                        s.post('http://localhost:9999/v1/tenders/'+str(tender_id),params=payload)
                        sleep(0.01)
                        
                    if tender_action == 'SELL' and tender_ticker == stock3_name and stock3_bid < tender_price + 0.05:
                        payload={'id':tender_id,'price':1}
                        s.post('http://localhost:9999/v1/tenders/'+str(tender_id),params=payload)
                        sleep(0.01)
                        
                    if tender_action == 'BUY' and tender_ticker == stock4_name and stock4_ask+0.05 > tender_price:
                        payload={'id':tender_id,'price':1}
                        s.post('http://localhost:9999/v1/tenders/'+str(tender_id),params=payload)
                        sleep(0.01)
                        
                    if tender_action == 'SELL' and tender_ticker == stock4_name and stock4_bid < tender_price + 0.05:
                        payload={'id':tender_id,'price':1}
                        s.post('http://localhost:9999/v1/tenders/'+str(tender_id),params=payload)
                        sleep(0.01)
                        
                        
                        
                        
                        
                        

            
            
            
            for ticker in tickers:
                position = pbal(s,ticker)[0]
                if abs(position) > 1000:
                    size = 1000
                else:
                    size = abs(position)
                if position > 0:
                    action = 'SELL'
                else:
                    action = 'BUY'
                    payload = {'ticker': ticker, 'quantity': size, 'type': 'MARKET', 'action': action}
                    s.post('http://localhost:9999/v1/orders',params=payload)

                    tick = get_tick(s)
                    tenders = s.get('http://localhost:9999/v1/tenders').json()
           

if __name__ == '__main__':
    # register the custom signal handler for graceful shutdowns
    signal.signal(signal.SIGINT, signal_handler)
    main()



