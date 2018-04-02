import datetime
import pprint
from stock_db import db,stock,ohlc
from sqlalchemy import desc
from quandl import Quandl
from alpha_vantage import AlphaVantage

db.create_all()

class Stock:
	def __init__ (self):
		self.q = Quandl()
		self.av = AlphaVantage()
		self.new_max = ''
		self.new_min = ''

	def grab_range(self,symbol,start_date,end_date):
		sd = datetime.datetime(int(start_date[0:4]),int(start_date[5:7]),int(start_date[8:10]))
		ed = datetime.datetime(int(end_date[0:4]),int(end_date[5:7]),int(end_date[8:10]))
		e = db.session.query(stock.id).filter_by(symbol=symbol).scalar() is not None
	
		if e:
			stock_range = self.range_exists(symbol,sd,ed)
		else:
			s = stock(symbol=symbol)
			self.commit_stock(s)
			t = self.scrape_date_range(symbol,sd,ed)	
			stock_range=self.return_range(symbol,sd,ed)
		return stock_range

	def commit_stock(self,stock):
		db.session.add(stock)
		db.session.commit()
		pass

	def range_exists(self,symbol,sd,ed):
		s = stock.query.filter_by(symbol=symbol).first()
		if s.exists_av == False and s.exists_quandl == False:
			stock_range =['cant scrape']
		else:

			if sd < s.minDate and ed > s.maxDate: 
				data_scrape1 = self.scrape_date_range(symbol,s.maxDate + datetime.timedelta(days=1),ed)
				data_scrape2 = self.scrape_date_range(symbol,sd,s.minDate + datetime.timedelta(days=-1))
				stock_range=self.return_range(symbol,sd,ed)
			elif sd < s.minDate and ed <= s.maxDate:
				data_scrape = self.scrape_date_range(symbol,sd,s.minDate + datetime.timedelta(days=-1))
				stock_range=self.return_range(symbol,sd,ed)
			elif sd >= s.minDate and ed > s.maxDate:
				data_scrape = self.scrape_date_range(symbol,s.maxDate + datetime.timedelta(days=1),ed)
				stock_range=self.return_range(symbol,sd,ed)
			else:
				stock_range=self.return_range(symbol,sd,ed)
			
		return stock_range

	def scrape_date_range(self,symbol,start_date,end_date):
		s = stock.query.filter_by(symbol=symbol).first()
		if s.exists_quandl == True and (s.exists_av == False or s.exists_av == None):
			stock_scrape = self.q.scrape_date_range(symbol,start_date.strftime('%Y-%m-%d'),end_date.strftime('%Y-%m-%d'))
		elif s.exists_quandl == False and s.exists_av == True:
			stock_scrape = self.av.scrape(symbol,start_date.strftime('%Y-%m-%d'),end_date.strftime('%Y-%m-%d'))
		elif s.exists_quandl == None and s.exists_av == None:
			stock_scrape = self.q.scrape_date_range(symbol,start_date.strftime('%Y-%m-%d'),end_date.strftime('%Y-%m-%d'))
			if stock_scrape == False:
				stock_scrape = self.av.scrape(symbol,start_date.strftime('%Y-%m-%d'),end_date.strftime('%Y-%m-%d'))

		if stock_scrape != False:
			s.minDate = ohlc.query.filter_by(symbol = symbol).order_by(ohlc.Date).first().Date
			s.maxDate = ohlc.query.filter_by(symbol = symbol).order_by(desc(ohlc.Date)).first().Date
			self.commit_stock(s)

		return stock_scrape

	def return_range(self,symbol,start_date,end_date):
		arr=[]
		rr = ohlc.query.filter(ohlc.symbol==symbol).filter(ohlc.Date >=start_date).filter(ohlc.Date <=end_date).order_by(desc(ohlc.Date))
		for i in rr:
			arr.append(i)
		return arr



		
