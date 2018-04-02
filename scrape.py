import requests
import json
import datetime
import pprint
from stock_db import db,stock,ohlc
from sqlalchemy import desc
from sqlalchemy.sql import exists

db.create_all()

# outputsize=full&
r = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=AMD&apikey=W6AM2QBIJ0LXP631")
av_stock_json = r.json()

symbol = av_stock_json['Meta Data']['2. Symbol']
d = datetime.datetime(int(2017),int(11),int(01))
s = stock(symbol=symbol,maxDate=d,minDate=d)
db.session.add(s)
db.session.commit()

for i in av_stock_json['Time Series (Daily)']:
	print i
	o = ohlc(oCode=symbol+str(i)
		, symbol = symbol
		, Date=datetime.datetime(int(i[0:4]),int(i[5:7]),int(i[8:10]))
		, Open = av_stock_json['Time Series (Daily)'][i]['1. open']
		, High = av_stock_json['Time Series (Daily)'][i]['2. high']
		, Low = av_stock_json['Time Series (Daily)'][i]['3. low']
		, Close = av_stock_json['Time Series (Daily)'][i]['4. close']
		, Volume =av_stock_json['Time Series (Daily)'][i]['6. volume']
		, AdjClose = av_stock_json['Time Series (Daily)'][i]['5. adjusted close']
		, stock_symbol = s) 
	db.session.add(o)
	db.session.commit()
	print av_stock_json['Time Series (Daily)'][i]['1. open']
	print av_stock_json['Time Series (Daily)'][i]['2. high']
	print av_stock_json['Time Series (Daily)'][i]['3. low']
	print av_stock_json['Time Series (Daily)'][i]['4. close']
	print av_stock_json['Time Series (Daily)'][i]['5. adjusted close']
	print av_stock_json['Time Series (Daily)'][i]['6. volume']


