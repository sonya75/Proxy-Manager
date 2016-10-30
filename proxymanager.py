import wx
import subprocess
import Queue
from PROXYGUI import *
from proxychecker import *
class ProxyManager(MyFrame1):
	def __init__(self):
		MyFrame1.__init__(self,None)
		self.proxylist={}
		self.totalchecks=0
		self.MAX_CHECKS=30
		self.MAX_PROCESS=30
		self.totalprocess=0
		self.checkqueue=Queue.Queue()
		self.workingproxies=Queue.Queue()
		self.selectedproxy=None
		self.Bind(wx.EVT_CLOSE,self.onclose)
		self.Bind(wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED,self.showlog)
	def onclose(self,event):
		self.Hide()
	def addproxy(self,proxy):
		if proxy in self.proxylist:
			return
		self.m_dataViewListCtrl4.AppendItem([proxy,"To be checked","",""])
		self.proxylist[proxy]={}
		self.addtocheckqueue(proxy)
	def deleteproxy(self,proxy):
		f=self.m_dataViewListCtrl4.GetItemCount()
		for i in range(0,f):
			if self.m_dataViewListCtrl4.GetTextValue(i,0)==proxy:
				self.m_dataViewListCtrl4.DeleteItem(i)
				self.proxylist.pop(proxy,None)
				return
#The following function can't be run in same thread.
	def startbroker(self):
		startupinfo = subprocess.STARTUPINFO()
		startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		self.ProxyBroker=subprocess.Popen(["proxy\\toto.exe"],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,startupinfo=startupinfo)
		for p in self.ProxyBroker.stdout:
			if self.killsignal:
				break
			p=p.strip()
			wx.CallAfter(self.addproxy,p)
	def killbroker(self):
		startupinfo = subprocess.STARTUPINFO()
		startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		try:
			subprocess.Popen(["TASKKILL","/F","/T","/pid",(self.ProxyBroker.pid)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,startupinfo=startupinfo)
		except:
			pass
	def updateitem(self,proxy,values):
		f=self.m_dataViewListCtrl4.GetItemCount()
		for i in range(0,f):
			if self.m_dataViewListCtrl4.GetTextValue(i,0)==proxy:
				for j in range(0,len(values)):
					self.m_dataViewListCtrl4.SetValue(values[j],i,(j+1))
				return
	def addtocheckqueue(self,proxy):
		self.checkqueue.put(proxy)
		self.updateitem(proxy,["Added to checking queue","",""])
	def processproxy(self,value):
		self.totalchecks-=1
		if "FATALERROR101" in value:
			val=value.strip().split("FATALERROR101")[-1]
			self.deleteproxy(val)
			return
		if "FAILED259" in value:
			val=value.strip().split("FAILED259")[-1]
			if "retries" in (self.proxylist[val]):
				if self.proxylist[val]["retries"]>=5:
					self.deleteproxy(val)
					return
			else:
				self.proxylist[val]["retries"]=0
			self.proxylist[val]["retries"]+=1
			if "lastretry" not in (self.proxylist[val]):
				self.proxylist[val]["lastretry"]=5
			else:
				self.proxylist[val]["lastretry"]=(self.proxylist[val]['lastretry'])*2
			wx.CallLater((1000*60*(self.proxylist[val]['lastretry'])),self.addtocheckqueue,val)
			self.updateitem(val,["Failed","","Retrying in "+str(self.proxylist[val]["lastretry"])+" mins"])
			return
		if "SUCCESS124" in value:
			val=value.strip().split("SUCCESS124")[-1]
			val1=val.split('PROXYTYPE')[-1].strip()
			val=val.split('PROXYTYPE')[0].strip()
			if "retries" in (self.proxylist[val]):
				self.proxylist[val].pop("retries",None)
			if "lastretry" in (self.proxylist[val]):
				self.proxylist[val].pop("lastretry",None)
			self.proxylist[val]["type"]=val1
			self.workingproxies.put(val)
			self.updateitem(val,["Working","",""])
	def startchecker(self):
		if self.killsignal:
			return
		if self.totalchecks>=self.MAX_CHECKS:
			wx.CallLater(1000,self.startchecker)
			return
		try:
			g=self.checkqueue.get_nowait()
			t=Thread(target=checkproxy,args=(g,self._procprox))
			t.daemon=True
			t.start()
			self.updateitem(g,["Checking","",""])
			self.totalchecks+=1
		except:
			wx.CallLater(1000,self.startchecker)
	def createcallback(self,proxy,callbk):
		def f(value):
			if len(value)>=3:
				if value[:3]=='8||':
					callbk(value[3:])
					return
			if len(value)>=6:
				if value[:6]=='|KILL|':
					wx.CallAfter(self.processproxy,("FAILED259"+proxy))
					wx.CallAfter(self.updatelog,proxy,"",setvalue=True)
					return
			if "log" not in self.proxylist[proxy]:
				wx.CallAfter(self.updatelog,proxy,"",setvalue=True)
			wx.CallAfter(self.updatelog,proxy,value)
			return
		return f
	def updatelog(self,proxy=None,value="",setvalue=False):
		if proxy==None:
			h=self.selectedproxy
			if h not in self.proxylist:
				return
			if "log" not in self.proxylist[h]:
				self.proxylist[h]['log']=""
			self.m_textCtrl23.SetValue(self.proxylist[h]["log"])
			return
		if setvalue:
			self.proxylist[proxy]["log"]=value
			self.updatelog()
			return
		self.proxylist[proxy]["log"]+=(value+"\n")
		if proxy==self.selectedproxy:
			self.m_textCtrl23.write(value+"\n")
	def showlog(self,event):
		h=self.m_dataViewListCtrl4.GetSelectedRow()
		if h==wx.NOT_FOUND:
			return
		else:
			self.selectedproxy=self.m_dataViewListCtrl4.GetTextValue(h,0)
			self.updatelog()
			return
	def runprocess(self,func,*args,**kwargs):
		if self.totalprocess>=self.MAX_PROCESS:
			wx.CallLater(1000,self.runprocess,func,*args,**kwargs)
			return
		try:
			g=self.workingproxies.get_nowait()
		except:
			wx.CallLater(1000,self.runprocess,func,*args,**kwargs)
			return
		self.totalprocess+=1
		self.updateitem(g,["Working","In Use","Building account. See log for details."])
		callbk=kwargs.pop("callback",None)
		cb=self.createcallback(g,callbk)
		t=Thread(target=func,args=(*args,**kwargs,proxy=g,callback=cb))
		t.daemon=True
		t.start()