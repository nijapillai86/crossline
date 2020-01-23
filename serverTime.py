import datetime
import os
import requests

class serverTime:
	def getTime(self):

		i = datetime.datetime.now()

		# Split the string based on space delimiter
		list_string = str(i).split(' ')
		 
		part1 = list_string[0].split('-')
		part1 = part1[::-1]

		part2 = list_string[1].split(':')

		# Join the string based on '-' delimiter
		dateVar = ''.join(part1)
		timeVar = (''.join(part2).split('.'))[0]
		dateTime = dateVar+timeVar
		return dateTime

	def currentDateandTime(self):
		dt 		 = datetime.datetime.now()
		string 		 = str(dt).split('.')
		date_time 	 = string[0].split(' ')
		return date_time
