from stock_db import db,stock,ohlc,hammers

o = ohlc.query.all()

s = stock.query.all()

h = hammers.query.all()


print o
# for i in s:
# 	print i.symbol

for p in s:
# 	print p.symbol
# # 	print p.exists_quandl
	db.session.delete(p)
	
for j in o:
	db.session.delete(j)

for i in h:
	db.session.delete(i)

db.session.commit()