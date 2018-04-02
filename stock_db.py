from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

with open('rds_credentials.txt', 'r') as f:
    qcreds = [x.strip() for x in f]

#if you want a local db uncomment below (sqlite) and comment the mysql+pymysql out 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/stock_db_test'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+qcreds[0]+':'+qcreds[1]+'@'+qcreds[2]+'/'+qcreds[3]
db = SQLAlchemy(app)

class hammers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), unique=False)
    xDate = db.Column(db.DateTime, unique=False)

    def __init__(self, symbol,xDate):
        self.symbol = symbol
        self.xDate = xDate

    def __repr__(self):
        return '<test %r>' % self.xDate.strftime("%Y-%m-%d") + " " + self.symbol 

class stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), unique=True)
    maxDate = db.Column(db.DateTime, unique=False)
    minDate = db.Column(db.DateTime, unique=False)
    exists_quandl = db.Column(db.Boolean, unique=False)
    exists_av = db.Column(db.Boolean, unique=False)
    ohlcs = db.relationship('ohlc', backref='stock_symbol', lazy='dynamic')

    def __init__(self, symbol):
        self.symbol = symbol

	def __repr__(self):
		return '<test %r>' % self.symbol 

class ohlc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(50), unique=False)
    oCode = db.Column(db.String(50), unique=True)
    Date = db.Column(db.DateTime, unique=False)
    Open = db.Column(db.Float(asdecimal=True), unique=False)
    High = db.Column(db.Float(asdecimal=True), unique=False)
    Low = db.Column(db.Float(asdecimal=True), unique=False)
    Close = db.Column(db.Float(asdecimal=True), unique=False)
    Volume = db.Column(db.Float(asdecimal=True), unique=False)
    AdjClose = db.Column(db.Float(asdecimal=True), unique=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'))

    def __init__(self,oCode,symbol, Date, Open, High, Low, Close, Volume,AdjClose,stock_symbol):
        self.oCode = oCode
        self.symbol = symbol
        self.Date = Date
        self.Open = Open
        self.High = High
        self.Low = Low
        self.Close = Close
        self.Volume = Volume
        self.AdjClose = AdjClose
        self.stock_symbol = stock_symbol

    def __repr__(self):
        return '<ohlc %r>' % self.Date.strftime("%Y-%m-%d") + " " + self.symbol
		

