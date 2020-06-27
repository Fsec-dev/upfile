#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Coded by Fsec-Dev

import sys, os, random
import requests
import hashlib
import json
from argparse import ArgumentParser

# Sequencia de colores (Solo para Linux)
R = "\033[1;31m"	#Rojo
G = "\033[1;32m"	#Verde
B = "\033[1m"		#Negrita
N = "\033[0m"		#Cancelar secuencia de colores

# Funcion para limpiar la terminal (Linux)
clear = lambda:os.system("clear")

# Lista de Hostings
hostings = {'anonfile':'https://api.anonfiles.com/upload',
	    'uplovd':'https://api.uplovd.com/upload'
}

 # banner
def banner():
	print G + """
	 _   _   ____   ____   _   _     ____
	| | | | |  _ | |  __| | | | |   | ___|
	| |_| | |  __| |  _|  | | | |_  | ___|
	|_____| |_|    |_|    |_| |___| |____| 1.0v
	""" + N

# Eligiendo UserAgent de forma aleatoria
def randomUA():
	UA = ['Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36',
		  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5',
		  'Mozilla/5.0 (X11; FreeBSD amd64; rv:40.0) Gecko/20100101 Firefox/40.0',
		  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.49 Safari/537.36 OPR/48.0.2685.7',
		  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
		  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
		  'Mozilla/5.0 (Linux; Android 7.0; PLUS Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36']
	return random.choice(UA)

# Obteniendo el hash del fichero sha256
def getsha256(filename):
	with open(filename, "rb") as f:
		bytes = f.read()
		string_hash = hashlib.sha256(bytes).hexdigest()
		return string_hash

# Funcion encargada de subir nuestro fichero al servidor elegido
def upload(api_url, filename):
	try:
		#Abrir archivo en modo lectura binaria
		file = {'file' : open(filename, 'rb')} 
		#User Agent
		headers = {'User-Agent':randomUA()}
		#Subir el archivo al hosting
		print G + "\n[i] Subiendo fichero, Solo espera..." 
		print "\n[+] Fichero: " + filename
		print "\n[+] Sha256: " + getsha256(filename) + N
		
		# ¡Listo!, es hora de enviar nuestro archivo
		r = requests.post(api_url, files=file, headers=headers)

		if r.status_code == 200:
			r = r.content
			j = json.loads(r)

			#datos de nuestro archivo subido al host
			link = j['data']['file']['url']['full']
			shortlink = j['data']['file']['url']['short']
			filename = j['data']['file']['metadata']['name']
			size = j['data']['file']['metadata']['size']['readable']

			clear # Limpiar terminal

			print G + "\n[i] Fichero subido exitosamente \n" + N
			print B + "Link completo: {}\nLink Corto: {}\nNombre de fichero: {}\nTamaño de fichero: {}"\
				.format(link, shortlink, filename, size) + N
		else:
			print "Error codigo de error: " + r.status_code

	except IOError:
		print B + "Error: Verifica tu conexion a internet o el nombre del fichero\nque deseas subir." + N
	
	except Exception as ex:
		print ex

def main():
	argp = ArgumentParser(version='Version 1.0', description='Sube tus archivos a diferentes Hosting con UpFile',
	 					  epilog='Creado por g0d, UpFile 1.0v - 2018')
	argp.add_argument('filename', help="Nombre del fichero a subir")
	argp.add_argument('-s', '--hosting', help="Selecciona el Hosting que deseas",
					  choices=['anonfile', 'uplovd'], dest='hosting')
	args = argp.parse_args()
	
	upload(hostings[args.hosting], args.filename)

if __name__ == "__main__":
	banner() # Un simple y bonito banner ;)
	main()
