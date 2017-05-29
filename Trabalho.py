## FUNCIONAMENTO ##
# Este programa implementa um servidor proxy Web com as funcionalidades
# de filtro de conteudo e cache de paginas web.

#Filtragem de requisicoes Tulio
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

		
filtragem()
