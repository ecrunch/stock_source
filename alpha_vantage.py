import requests
import json
import datetime
import pprint
from stock_db import db,stock,ohlc
from sqlalchemy import desc
from sqlalchemy.sql import exists

db.create_all()

class AlphaVantage:
	def __init__ (self):
		self.first_part = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol="
		self.last_part= "&apikey=W6AM2QBIJ0LXP631"
		self.full = "&outputsize=full"
	def scrape(self,symbol,start_date,end_date):
		if ohlc.query.filter(ohlc.symbol==symbol).count() == 0:
			link = self.first_part + symbol + self.full +self.last_part
		else:
			link = self.first_part + symbol + self.last_part

		r = requests.get(link)
		av_stock_json = r.json()
		s=stock.query.filter_by(symbol=symbol).first()

		try:
			# print datetime.datetime(int(i[0:4]),int(i[5:7]),int(i[8:10]))
			for i in av_stock_json['Time Series (Daily)']:
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

		except Exception,e:
				db.session.rollback()
				print str(e)
				s.exists_av = False
				db.session.add(s)
				db.session.commit()
				return False

		s.exists_av = True
		db.session.add(s)
		db.session.commit()
		return True


