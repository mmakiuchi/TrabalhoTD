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



class ThreadedServer(object):
	def __init__(self,host,port):
		import socket
		import threading
		self.host = host #o host da thread
		self.port = port #a porta da thread
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error:
			print 'Nao foi possivel abrir o socket'
			sys.exit(1)
		
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind((self.host, self.port)) #faz a conexao

	def listen(self):
		import socket
		import threading
		self.sock.listen(5) #sock pode guardar ate 5 conexoes antes de descartar alguma
		while True: #loop infinito
			(client,address) = self.sock.accept() #aceita conexao externa
			client.settimeout(60) #estabelece timeout de 60 segundos para cada thread
			threading.Thread(target = self.listenToClient,args = (client,address)).start() #inicializa a thread para cada novo cliente
			
	def listenToClient(self,client,address):
		import socket
		import threading
		size = 1024 #tamanho do buffer
		while True:
			try:
				data = client.recv(size) #recebe dados do cliente
				if data:
					response = data  #Set the response to echo back the recieved data 
					client.send(response)
				else:
					raise error('Client disconnected')
			except:
				client.close()
				return False

				
#Proxy Basico
def proxy():
	import socket
	import sys
	import signal
	import threading
	
	TCP_IP = '127.0.0.1'
	TCP_PORT = 5005
	BUFFER_SIZE = 1024
	
	socket.setdefaulttimeout = 0.50
	#signal.signal(signal.SIGINT,self.shutdown)
	
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error:
		print 'Nao foi possivel abrir o socket'
		sys.exit(1)
	
	s.bind((TCP_IP, TCP_PORT)) #s ouve do host TCP_IP na porta TCP_PORT
	s.listen(4) #s pode guardar ate 4 conexoes antes de descartar alguma
		
	while 1:
		(conn, addr) = s.accept() #aceita conexoes exteriores
		print 'Connection address:', addr
		data = conn.recv(BUFFER_SIZE)
		if not data: break
		print "received data:", data
		#conn.send(data)  # echo
	conn.close()

if __name__ == '__main__':
	ThreadedServer('127.0.0.1',5005).listen() #inicia uma main thread e faz ela escutar
	#proxy() #proxy basico antigo. Nao eh multi-thread