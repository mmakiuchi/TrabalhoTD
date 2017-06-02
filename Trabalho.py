## FUNCIONAMENTO ##
# Este programa implementa um servidor proxy Web com as funcionalidades
# de filtro de conteudo e cache de paginas web.

#Caching ????


#Testa denyTerms

def denyTerms(data):
	denied=-1

	if os.path.isfile("denyTerms.txt")==True:	
		#print("denyTerms found")
		fileObj=open("denyTerms.txt","r")		#Abre arquivo contendo termos proibidos
		denyTerms=[]					#Lista para adicionar os termos proibidos

		#Temos que inserir uma comparacao para testar se o item ja existe dentro da lista ou para que essa funcao seja chamada apenas uma vez

		for line in fileObj:
			denyTerms.append(line)			#Adiciona  termo na lista
			if(data.find(line)!=-1): 		#encontrou o denyTerm em data
				denied=line  			#armazena o termo proibido
				break				#caso seja um termo proibido a funcao retorna para a chamada com a linha que contem o termo proibido
		fileObj.close()
	
	return denied



#Filtragem de requisicoes whitelist e blacklist

def blackWhite(endereco):
	import os.path					#Biblioteca para uso de funcoes de abertura de arquivos e pastas
	
	black=-1 					#nem na whitelist nem na blacklist
	
	#Leitura de arquivos

	if os.path.isfile("whitelist.txt")==True: 	#encontrou arquivo whitelist
		fileObj=open("whitelist.txt","r")	#abrindo a whitelist

		#Temos que inserir uma comparacao para testar se o item ja existe dentro da lista ou para que essa funcao seja chamada apenas uma vez

		whitelist=[]				#inicia a estrutura da lista a ser usada para a whitelist
		for line in fileObj:			#anda nos itens da lista
			whitelist.append(line)		#adiciona os dados na estrutura da lista
			found = line.find("\n")
			if(found!=-1):			#retira o enter no final de cada endereco caso exista
				line=line[0:found-1]	
				if(line==endereco):		#compara com o endereco que o cliente deseja conectar
					black=0 		#encontrou na whitelist
					print "teste whitelist"
					break
		fileObj.close() 			#finalizou leitura
		
	if os.path.isfile("blacklist.txt")==True: 	#encontrou arquivo blacklist
		fileObj=open("blacklist.txt","r")	#abrindo a blacklist

		#Temos que inserir uma comparacao para testar se o item ja existe dentro da lista


		blacklist=[]				#inicia a estrutura da lista a ser usada para a blacklist
		for line in fileObj:			#anda nos itens da lista
			blacklist.append(line)		#adiciona os dados na estrutura da lista
			found = line.find("\n")
			if(found!=-1):			#retira o enter no final de cada endereco caso exista
				line=line[0:found]
				if(line==endereco):		#compara com o endereco que o cliente deseja conectar
					black=1 		#encontrou na blacklist
					print "teste blacklist"					
					break
		fileObj.close() 			#finalizou leitura
	
	print black
	return black


#Inicia a leitura da requisicao do usuario e chama as funcoes de teste de condicoes para 'BlackWhite' e 'DenyTerms'

def parserInfo(data):
	response = data
	
	found = data.find('www.')
	if(found!=-1): 					#achou endereco
		endereco=data[found:] 			#pega os dados a partir do www. ate o fim
		endereco=endereco.split(" ")[0] 	#pega os endereco www.
		print endereco
		found = endereco.find('/')
		print found
		if(found!=-1):
			endereco=endereco[0:found]
		#print 'endereco '
		#print endereco
		black = blackWhite(endereco)
		if(black==1):
			response = 'Pagina bloqueada! Acesso nao permitido'		#Mensagem caso tenha esteja na Blacklist
			print response
			return response							#mensagem de erro
		else: 									#pagina nao bloqueada
			if(black==0): 							#esta na whitelist
				return response 					#resposta direta (whitelist)
			elif(black==-1): 						#nao esta nem na whitelist nem na blacklist
				print 'DenyTerms'
				response=denyTerms(data) 				#testa denyTerms	
				return response		
	else:
		return found 					#retorna -1 que foi configurado dentro da funcao blackwhite
		


#Funcao do Proxy para escutar inicialmente o cliente

def listenToClient(client,address):	#captura os dados da conexao thread e trabalha eles
	import socket		#importando biblioteca Socket para implementar a interface/porta de comunicacao entre proxy e cliente
	import threading
	size = 1024			#tamanho do buffer
	while 1:			#loop infinito para receber dados do cliente
		try:
			data = client.recv(size)	#recebe dados do cliente (info do pacote)
			if data:			#Se existem dados
				response = parserInfo(data)
				client.send(response)	#Envia a resposta
			else: 				#se nao existem dados
				raise error('Client disconnected')
		except:
			client.close()			#caso a conexao nao seja iniciada fecha a conexao
			return False



#Funcao de estabelecimento de conexao do proxy com cliente

def initConect(host,port): 						#inicializa o socket e cria threads
	import socket
	import threading		#???
	import sys
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 	#cria um socket
	except s.error:
		print 'Nao foi possivel abrir o socket'			#erro de saida
		sys.exit(1)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 	#define opcoes do socket
	s.bind((host, port)) 						#conecta o socket
	s.listen(5) 							#sock pode guardar ate 5 conexoes antes de descartar alguma
	while 1: 					#loop infinito
		try:
			(client,address) = s.accept() 	#aceita conexao externa
			client.settimeout(30) 		#estabelece timeout de 30 segundos para cada thread
			t=threading.Thread(target = listenToClient,args = (client,address)) 	#define uma thread para ouvir o cliente
			
			#Thread => instancia a thread listenToClient e envia os parametros client e address

			t.start() 			#inicializa a thread para cada novo cliente
		except KeyboardInterrupt:		#Para o Programa
			print 'Programa interrompido!'
			s.close()
			sys.exit(0)



#Programa Principal

if __name__ == '__main__':				#Programa Principal
	initConect('127.0.0.1',5005)			#Chamada de funcao de conexao passando o endereco IP e porta de Socket







