#!/usr/bin/python
import os
import datetime
import requests
import pymongo
from pymongo import MongoClient

#import tinyDB and the required submodules:
# from tinydb import TinyDB, Query

# #Next we need to declare a storage location for our database:
# db = TinyDB('db.json')
client = MongoClient('localhost', 27017, connect=False)

db = client['quaryproject']
collection = db['record']

class test:

	def events(self, event, evtTime,evttype):
		print "trip occurs" + event + 'evttype' + evttype
		dt = datetime.datetime.now()
		string = str(dt).split('.')
		date_time = string[0].split(' ')
		time_arr  =date_time[1].split(':') 		

		#select event from cam1 and type is Tripwire
		if event == "100100" and evttype == '02':
			print 'Object crossed at',date_time[1]
			if int(time_arr[0]) >= 9 and int(time_arr[0]) < 18:
				 print 'Object time cross'
			         data = {'Object':'crossed','date' : date_time[0], 'time': date_time[1]}
			         collection.insert(data)
		


		
