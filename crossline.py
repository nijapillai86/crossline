#python server main page

import multiprocessing

import socket
import sys
import requests
import os
from serverTime import serverTime
from test import test


classObj = test()
timeObj  = serverTime()

def eventDetect(rcvData, serTime):
  	diffTime = -1
	rcv_arr = rcvData.split('\x1e')
  	
  	evtArr = []
  	event_count = 0
  	evtLine = (rcv_arr[8].split('00'))[0]
  	
  	#only select event on its start state
  	if rcv_arr[7] == '1' :
  		#print rcv_arr
  		classObj.events(rcv_arr[2], serTime, rcv_arr[5])

def handle(connection, address):
	import logging
	import datetime

	global pipe
	global data
	global magic_header_version
	global stream_started
	global first_stream
	global did_value
	global did_arr
	global clt_arr
	 

	logging.basicConfig(level=logging.DEBUG)
	logger = logging.getLogger("process-%r" % (address,))
	counter = 0
	checksumvalue = '';
	

	try:
		logger.debug("Connected %r at %r", connection, address)

		client_id = unicode(connection)
		client_id = client_id.split("at",1)[1][:-1].strip()

		while True:
			try:
				#get buffer data from connection
				buf = connection.recv(1024)
			except socket.error, e:
				err = e.args[0]
				if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
					sleep(1)
					print 'No data available'
					continue
				else:
					print e
					sys.exit(1)
			else:
				pass    
			
			
			
			
			#if buf == "":
			#    print " null value buffer"
				#logger.debug("Socket closed remotely")
			#    break
			
			#reading the action from buf from position 1 till 8
			if buf != "":
				
				#if buf value not null
				action = buf[1:8]
				
				#if action is register camera
				if action == "REG_LOG":

					#extract mac address from bufffer
					mac_address = buf[21:38].replace(':', '').upper()
					
					did_value = '100100'

					starttime = datetime.datetime.now()    
					#did_value = '100100'
					talkback  = chr(1) + 'ACK_LOG' + chr(30) + '0' + chr(30) + did_value + chr(30) + '3' + chr(30) + '5' + chr(30) + chr(4)
					connection.sendall(talkback)

				#action = REQ_POL (Polling)
				#extract did, if local variable req_pol == 1, status 0 (do nothing) otherwise 1 (open new port)
				if action == "REQ_POL":
					did_extracted = buf[10:16]
					did_value     = int(did_extracted)

					if did_value in did_arr:
						talkback = chr(1) + 'ACK_POL' + chr(30) + '0' + chr(30) + chr(4)

					else:
						clt_arr.append(client_id)
						talkback = chr(1) + 'ACK_POL' + chr(30) + '1' + chr(30) + chr(4)
						did_arr.append(did_value)

					connection.sendall(talkback)
					logger.debug("Sent REQ_POL response")
					cTime = timeObj.currentDateandTime()
					time_arr =  cTime[1].split(':')
					if (time_arr[0]+':'+time_arr[1])== '18:18' :
						os.system('python daily_report_gen.py')
					
				
				#Action - ACK_DID
				#set the stream_started variable to 1
				#Initiate to start the live stream from camera
				if action == "ACK_DID":
					#print "ack did"
					did_extracted = buf[9:15]
					did_value     = int(did_extracted)
				if action == 'RCV_EVT':
					# get server time
  					sTime = timeObj.getTime()
					eventDetect(buf,sTime)
					print "process breaks here"
					break

					

	except:
		logger.exception("Problem handling request")
	finally:
		#logger.debug("Closing socket")
		#connection.close()
		pass

#server class for configuring and starting server
class Server(object):
	def __init__(self, hostname, port):
		import logging
		self.logger   = logging.getLogger("server")
		self.hostname = hostname
		self.port     = port
		
	def start(self):
		self.logger.debug("listening")
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind((self.hostname, self.port))
		self.socket.listen(1)

		while True:
			conn, address  = self.socket.accept()
			self.logger.debug("Got connection")

			#starting multi process
			process        = multiprocessing.Process(target=handle, args=(conn, address))           
			process.daemon = True
			process.start()
			self.logger.debug("Started process %r", process)


#main function which is called ao load
if __name__ == "__main__":
	import logging
	
	pipe = {}
	data = ''
	did_value = 0
	stream_started = 0
	first_stream = 0
	magic_header_version = ''
	# temp = 5
	# q = Queue.Queue()
	# test = 56

	did_arr  = []
	clt_arr  = []
	
	


	logging.basicConfig(level=logging.DEBUG)

	#server ip and port configuration
	server = Server("0.0.0.0", 8051)

	
	try:
		#server start to listen socket
		logging.info("Listening")
		server.start()
	except:
		logging.exception("Unexpected exception")
	finally:
		logging.info("Shutting down")
		for process in multiprocessing.active_children():
			logging.info("Shutting down process %r", process)
			process.terminate()
			process.join()
logging.info("All done")
