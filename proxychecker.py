from threading import Thread 
import subprocess
import socket
import socks
import time
from httpproxy import *
socket.setdefaulttimeout(30)
def checksocks5proxy(x,y):
	s=socks.socksocket()
	s.setproxy(socks.PROXY_TYPE_SOCKS5,x,y)
	try:
		s.connect(('www.google.com',80))
		s.close()
		return True
	except:
		try:
			s.close()
		except:
			pass
		return False
def checksocks4proy(x,y):
	s=socks.socksocket()
	s.setproxy(socks.PROXY_TYPE_SOCKS4,x,y)
	try:
		s.connect(('www.google.com',80))
		s.close()
		return True
	except:
		try:
			s.close()
		except:
			pass
		return False
def checkhttpproxy(x,y):
	s=socks.socksocket()
	s.setproxy(socks.PROXY_TYPE_HTTP,x,y)
	try:
		s.connect(('www.google.com',80))
		s.close()
		return True
	except:
		try:
			s.close()
		except:
			pass
		return False
def checkproxy(x,callback):
	if x.count(':')!=1:
		callback("FATALERROR101"+x)
		return
	try:
		y=x.strip().split(':')
		port = int(y[1])
		ip=y[0]
	except:
		callback("FATALERROR101"+x)
		return
	try:
		if checkhttpproxy(ip,port):
			callback("SUCCESS124"+x+"PROXYTYPE HTTP")
		elif checksocks5proxy(ip,port):
			callback("SUCCESS124"+x+"PROXYTYPE SOCKS5")
		elif checksocks4proy(ip,port):
			callback("SUCCESS124"+x+"PROXYTYPE SOCKS4")
		else:
			raise
		return True
	except:
		callback("FAILED259"+x)
		return False