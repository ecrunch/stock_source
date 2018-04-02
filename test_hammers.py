from datetime import datetime, timedelta
import pprint
from stock_db import db,stock,ohlc,hammers
from sqlalchemy import desc
from stock import Stock
from quandl import Quandl

db.create_all()

s = Stock()

h = hammers.query.filter_by().order_by(hammers.xDate)

total_cash = 1000
original_cash = total_cash
total_pnl = 0

for i in h:
	print i
	back_date = str(i.xDate + timedelta(days=1))
	end_date = str(i.xDate +timedelta(days=7))
	ted = s.grab_range(i.symbol,back_date,end_date)
	count = 0

	print "pre_cash"
	print total_cash

	for k in reversed(ted):
		
		print k.Date
		count +=1
		if count ==1:
			buy=k.Open
			print "buy_price"
			print buy
		elif count == 2:
			sell_high = k.High
			# print sell_high
			sell_open= k.Open
			# print sell_open
			sell = (sell_high+sell_open)/2
			print "sell_price"
			print sell

	try:
		
		trade_2 = total_cash
		trade_1 = sell *(total_cash/buy)
		trade_pnl = trade_1 - trade_2

		total_cash = total_cash + trade_pnl

		total_pnl = total_pnl + trade_pnl
		
	except NameError:
		pass
	else:
		
		print "trade_pnl"
		print trade_pnl

		print "total_profit"
		print total_pnl

		print "total_cash"
		print total_cash

		print "   "

print total_pnl
print total_cash
print total_cash/original_cash
