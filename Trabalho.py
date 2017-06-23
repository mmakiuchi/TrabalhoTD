## FUNCIONAMENTO ##
# Este programa implementa um servidor proxy Web com as funcionalidades
# de filtro de conteudo e cache de paginas web.

#Caching


#Testa denyTerms
def denyTerms(data):
	import os.path
	import string
	import sys
	
	denied=-1 #nao ha denyTerms
	#print data
	if os.path.isfile("denyTerms.txt")==True:	
		fileObj=open("denyTerms.txt","r") #Abre arquivo contendo termos proibidos
		for line in fileObj:
			#line=line.decode('utf8')
			#print line
			found = data.find(line)			
			if(found!=-1): #encontrou o denyTerm em data
				print 'Achou deny term'				
				print line				
				denied=1						
				break
		fileObj.close()
	#print denied
	return denied

#Filtragem de requisicoes whitelist e blacklist
def blackWhite(endereco):
	import os.path
	import sys
	import string
	
	black=-1 #nem na whitelist nem na blacklist
	
	#Leitura de arquivos
	if os.path.isfile("whitelist.txt")==True: 	#encontrou arquivo whitelist
		fileObj=open("whitelist.txt","r")	#abrindo a whitelist
		whitelist=[]
		for line in fileObj:
			whitelist.append(line)
			found = line.find("\n")
			if(found!=-1):	#retira o enter no final de cada endereco caso exista
				line=line[0:found-1]	
			if(line==endereco):	#compara com o endereco que o cliente deseja conectar
				black=0 #encontrou na whitelist
				break
		fileObj.close() #finalizou leitura
		
	if os.path.isfile("blacklist.txt")==True:
		fileObj=open("blacklist.txt","r")
		blacklist=[]
		for line in fileObj:
			blacklist.append(line)
			found = line.find("\n")
			if(found!=-1): #retira o enter no final de cada endereco caso exista
				line=line[0:found]
			if(line==endereco):
				black=1 #encontrou na blacklist				
				break
		fileObj.close() #finalizou leitura
	
	#print black
	return black

def getAddress(data):
	import sys
	import string
	
	found = data.find('www.')
	if(found!=-1): #achou endereco
		endereco=data[found:] #pega os dados a partir do www. ate o fim
		endereco=endereco.split(" ")[0]
	return(endereco)
	
def separaLog(data):
	import sys
	import string
	
	dados=0
	found = data.find('HTTP/1.1')
	if(found!=-1):
		found = found+7
		dados = data[0:found]
	return dados


#Inicia a leitura da requisicao do usuario e chama as funcoes de teste de condicoes para 'BlackWhite' e 'DenyTerms'
def parserInfo(data):
	import sys
	import string
	response = data
	
	found = data.find('www.')
	if(found!=-1): #achou endereco
		endereco=data[found:] #pega os dados a partir do www. ate o fim
		endereco=endereco.split(" ")[0] #pega os endereco www.
		found = endereco.find('/')
		if(found!=-1):
			endereco=endereco[0:found]
		black = blackWhite(endereco)
		return black #retorna 0 para whitelist, 1 para blacklist e -1 para nem um nem outro
	else: #nao achou endereco www. nos dados
		found = 2
		return found #retorna 2
		
#Funcao do Proxy para escutar inicialmente o cliente
def listenToClient(client,address):	#captura os dados da conexao thread e trabalha eles
	import socket #importando biblioteca Socket para implementar a interface/porta de comunicacao entre proxy e cliente
	import threading
	import requests
	import sys
	import os.path
	import datetime
	import string
	size = 2048	#tamanho do buffer
	blacklistAnswer = '<!DOCTYPE html><html><body style="background-color:papayawhip;"><h1 style="font-family:verdana;text-align:center;">Pagina Bloqueada</h1></body></html>'
	denyAnswer = '<!DOCTYPE html><html><body style="background-color:papayawhip;"><h1 style="font-family:verdana;text-align:center;">Conteudo Bloqueado</h1></body></html>'
	
	while 1: #recebe dados do cliente
		try:
			data = client.recv(size) #recebe dados do cliente (info do pacote)
			if data: #se existem dados
				response = parserInfo(data)
				fileObj=open("log.txt","a") #abre o arquivo log.txt para adicionar info
				requisicao = separaLog(data) #pega a primeira linha da requisicao para compor o log (exemplo GET aprender.unb.br HTTP/1.1)
				now=datetime.datetime.now()
				fileObj.write(requisicao+str(now)+'\n') #guarda a linha da requisicao+hora atual
				fileObj.close()
				if(response==0): #whitelist
					address = getAddress(data)
					req = requests.get('http://'+address)
					client.send(req.content)
					client.close()
				else:
					if(response==1): #blacklist
						client.send(blacklistAnswer)
						client.close()
					else: #nao esta nem na whitelist nem na blacklitst
						#envia a requisicao e testa por denyTerms	
						address = getAddress(data)
						req = requests.get('http://'+address)					
						dados = req.content				
						if(dados.find('<!DOCTYPE html>')!=-1):				
							print 'testa denyterms'
							achouDeny=denyTerms(dados)
							if achouDeny==-1: #nao eh denyTerms
								#print 'nao tem deny terms'
								client.send(req.content)
								client.close()
							else: #eh denyTerms
								#print 'tem denyterms'
								client.send(denyAnswer)
								client.close()
						else:
							client.send(req.content)
							client.close()
			else:
				raise error('Client disconnected')
		except:
			client.close() #caso a conexao nao seja iniciada fecha a conexao
			return False

#Funcao de estabelecimento de conexao do proxy com cliente
def initConect(host,port): #inicializa o socket e cria threads
	import socket
	import threading
	import sys
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #cria um socket
		
	except s.error:
		print 'Nao foi possivel abrir o socket'
		sys.exit(1)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #define opcoes do socket
	s.bind((host, port)) #conecta o socket
	s.listen(60) #s pode guardar ate 5 conexoes antes de descartar alguma
	while 1: #loop infinito
		try:
			(client,address) = s.accept() #aceita conexao externa
			host1,port1 = address
			#s.connect((host,port))
			client.settimeout(60) #estabelece timeout de 60 segundos para cada thread
			t=threading.Thread(target = listenToClient,args = (client,address)) #define uma thread para ouvir o cliente
			#Thread => instancia a thread listenToClient e envia os parametros client e address	
			
			t.start() #inicia a thread
		#Interrupcao de teclado
		except KeyboardInterrupt:
			print 'Programa interrompido!'
			s.close()
			sys.exit(0)

if __name__ == '__main__':
	initConect('127.0.0.1',5005)
