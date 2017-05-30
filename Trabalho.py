## FUNCIONAMENTO ##
# Este programa implementa um servidor proxy Web com as funcionalidades
# de filtro de conteudo e cache de paginas web.

#Filtragem de requisicoes
def filtragem():
	import os.path
	if os.path.isfile("whitelist.txt")==True:
		print("Whitelist found")
		fileObj=open("whitelist.txt","r")
		whitelist=[]
		for line in fileObj:
			whitelist.append(line)
		fileObj.close()
	if os.path.isfile("blacklist.txt")==True:
		print("Blacklist found")
		fileObj=open("blacklist.txt","r")
		blacklist=[]
		for line in fileObj:
			blacklist.append(line)
		fileObj.close()
	if os.path.isfile("denyTerms.txt")==True:
		print("denyTerms found")
		fileObj=open("denyTerms.txt","r")
		denyTerms=[]
		for line in fileObj:
			denyTerms.append(line)
		fileObj.close()
	print whitelist
	
#Caching


#Proxy Basico
def proxy():
	import socket
	import sys
	import signal
	
	TCP_IP = '127.0.0.1'
	TCP_PORT = 5005
	BUFFER_SIZE = 20  # Normally 1024, but we want fast response
	
	socket.setdefaulttimeout = 0.50
	#signal.signal(signal.SIGINT,self.shutdown)
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	if s is None:
		print 'could not open socket'
		sys.exit(1)
	
	s.bind((TCP_IP, TCP_PORT))
	s.listen(1)
	
	conn, addr = s.accept()
	print 'Connection address:', addr
	
	while 1:
		data = conn.recv(BUFFER_SIZE)
		if not data: break
		print "received data:", data
		conn.send(data)  # echo
	conn.close()
		
proxy()