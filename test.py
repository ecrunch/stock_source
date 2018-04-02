from datetime import datetime, timedelta
import pprint
from stock_db import db,stock,ohlc,hammers
from sqlalchemy import desc
from stock import Stock
from quandl import Quandl

db.create_all()


s = Stock()
q = Quandl()

sym = 'SPY'
sd = '2017-01-01'
ed = '2018-02-15'

test = s.grab_range(sym,sd,ed)
total_cash = 3000
total_pnl = 0

for i in test:
	stock_movement = i.High -i.Low
	stock_open = i.Open - i.Low
	stock_close = i.Close - i.Low

	if stock_open > stock_close:
		stock_high = stock_open
		stock_low = stock_close
	elif stock_open < stock_close:
		stock_high = stock_close
		stock_low = stock_open
	else:
		stock_high = stock_close
		stock_low = stock_open

	stock_oc_movement = stock_high - stock_low


	if (stock_high/stock_movement) > .6 and (stock_low/stock_movement) > .6:
		h = hammers(sym,i.Date)
		print(i.Date)
		db.session.add(h)
		db.session.commit()
		# print i
		# back_date = str(i.Date - timedelta(days=4))
		# end_date = str(i.Date -timedelta(days=1))
		# sed = s.grab_range(sym,back_date,end_date)
		# for j in sed:
		# 	print (j.Date)
		# 	print (j.Open + j.Close)/2
		# back_date = str(i.Date + timedelta(days=1))
		# end_date = str(i.Date +timedelta(days=4))
		# ted = s.grab_range(sym,back_date,end_date)
		# count = 0

		# print "pre_cash"
		# print total_cash

		# for k in reversed(ted):
			
		# 	print k.Date
		# 	count +=1
		# 	if count ==1:
		# 		buy=k.Open
		# 		print "buy_price"
		# 		print buy
		# 	elif count == 2:
		# 		sell_high = k.High
		# 		sell_open= k.Open
		# 		sell = (sell_high+sell_high+sell_high+sell_open)/4
		# 		print "sell_price"
		# 		print sell

# 		try:
# 			trade_2 = total_cash
# 			trade_1 = sell *(total_cash/buy)
# 			trade_pnl = trade_1 - trade_2

# 			total_cash = total_cash + trade_pnl

# 			total_pnl = total_pnl + trade_pnl
			
# 		except NameError:
# 			pass
# 		else:
			
# 			print "trade_pnl"
# 			print trade_pnl

# 			print "total_profit"
# 			print total_pnl

# 			print "total_cash"
# 			print total_cash

# 			print "   "

# print total_pnl
# print total_cash
	



