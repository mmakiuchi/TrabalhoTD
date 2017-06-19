## FUNCIONAMENTO ##
# Este programa implementa um servidor proxy Web com as funcionalidades
# de filtro de conteudo e cache de paginas web.

#Caching


#Testa denyTerms
def denyTerms(data):
	denied=-1 #nao ha denyTerms

	if os.path.isfile("denyTerms.txt")==True:	
		fileObj=open("denyTerms.txt","r")		#Abre arquivo contendo termos proibidos
		denyTerms=[]					#Lista para adicionar os termos proibidos

		#Temos que inserir uma comparacao para testar se o item ja existe dentro da lista ou para que essa funcao seja chamada apenas uma vez

		for line in fileObj:
			denyTerms.append(line)	#Adiciona  termo na lista
			if(data.find(line)!=-1): 		#encontrou o denyTerm em data
				denied=line  			#armazena o termo proibido
				break				#caso seja um termo proibido a funcao retorna para a chamada com a linha que contem o termo proibido
		fileObj.close()
	
	#print denied
	return denied

#Filtragem de requisicoes whitelist e blacklist
def blackWhite(endereco):
	import os.path
	
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
	response = data
	
	found = data.find('www.')
	if(found!=-1): #achou endereco
		endereco=data[found:] #pega os dados a partir do www. ate o fim
		endereco=endereco.split(" ")[0]
	return(endereco)
	
#Inicia a leitura da requisicao do usuario e chama as funcoes de teste de condicoes para 'BlackWhite' e 'DenyTerms'
def parserInfo(data):
	response = data
	
	#print data
	
	found = data.find('www.')
	#print found
	if(found!=-1): #achou endereco
		endereco=data[found:] #pega os dados a partir do www. ate o fim
		endereco=endereco.split(" ")[0] #pega os endereco www.
		found = endereco.find('/')
		if(found!=-1):
			endereco=endereco[0:found]
		black = blackWhite(endereco)
		return black
	else: #nao achou endereco www. nos dados
		
		#O que retornar?
		return found #retorna -1 que foi configurado dentro da funcao blackwhite
		
#Funcao do Proxy para escutar inicialmente o cliente
def listenToClient(client,address):	#captura os dados da conexao thread e trabalha eles
	import socket #importando biblioteca Socket para implementar a interface/porta de comunicacao entre proxy e cliente
	import threading
	import requests
	size = 2048	#tamanho do buffer
	while 1: #recebe dados do cliente
		try:
			data = client.recv(size) #recebe dados do cliente (info do pacote)
			if data: #se existem dados
				response = parserInfo(data)
				if(response==0): #whitelist
					address = getAddress(data)
					req = requests.get('http://'+address)
					#print 'oi'
					client.send(req.content)
					#print 'passou'
					client.close()
				else:
					if(response==1): #blacklist
						client.send('Erro! Pagina bloqueada')
					else: #nao esta nem na whitelist nem na blacklitst
						#envia a requisicao e testa por denyTerms	
						k=1
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
	s.listen(5) #s pode guardar ate 5 conexoes antes de descartar alguma
	while 1: #loop infinito
		try:
			
			(client,address) = s.accept() #aceita conexao externa
			host1,port1 = address
			print host
			print port
			print host1
			print port1
			#s.connect((host,port))
			client.settimeout(30) #estabelece timeout de 30 segundos para cada thread
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
