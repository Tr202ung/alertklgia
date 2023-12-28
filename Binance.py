from binance.client import Client
import binance

#Credential data
"""
Create a Binance API and remember to allow futures trading
"""
api_key = 'YOUR API_KEY'
api_secret = 'YOUR API_SECRET'

client = Client(api_key, api_secret)
