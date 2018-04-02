import requests
import json
import datetime
from stock_db import db,stock,ohlc
from sqlalchemy import desc

db.create_all()

class Quandl:
	def __init__ (self):
		self.first_part = "https://www.quandl.com/api/v3/datasets/WIKI/"
		self.mid_part =  "/data.json?start_date="
		self.mid_part2 = "&end_date="
		self.last_part = "&order=asc&api_key=Q7DSNVGYPQ9WnMmxEgVb"
	def scrape_date_range(self,symbol,start_date,end_date):
		link = self.first_part + symbol + self.mid_part + start_date + self.mid_part2+ end_date +self.last_part
		r = requests.get(link)
		quandl_stock_json = r.json()
		s = stock.query.filter_by(symbol=symbol).first()
		try:
			data = quandl_stock_json['dataset_data']['data']
				
			for i in range(0,len(data)):
				o = ohlc(oCode=symbol+str(data[i][0])
					, symbol = symbol
					, Date=datetime.datetime(int(data[i][0][0:4]),int(data[i][0][5:7]),int(data[i][0][8:10]))
					, Open = data[i][1]
					, High = data[i][2]
					, Low = data[i][3]
					, Close = data[i][4]
					, Volume =data[i][5]
					, AdjClose = data[i][11]
					, stock_symbol = s) 
				db.session.add(o)
				try:
					db.session.commit()	
					s.exists_quandl = True
				except Exception,e:
					db.session.rollback()
					print str(e)
					pass

		except Exception,e:
			print str(e)
			s.exists_quandl = False
			print("stock doesn't exist with quandl")
			return False

		return True