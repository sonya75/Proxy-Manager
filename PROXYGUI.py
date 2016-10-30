# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 640,446 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_dataViewListCtrl4 = wx.dataview.DataViewListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_dataViewListColumn10 = self.m_dataViewListCtrl4.AppendTextColumn( u"Proxy Server" ,align= wx.ALIGN_CENTER,flags=wx.dataview.DATAVIEW_COL_SORTABLE)
		self.m_dataViewListColumn11 = self.m_dataViewListCtrl4.AppendTextColumn( u"Status" ,align=wx.ALIGN_CENTER,flags=wx.dataview.DATAVIEW_COL_SORTABLE)
		self.m_dataViewListColumn12 = self.m_dataViewListCtrl4.AppendTextColumn( u"Usage" ,align=wx.ALIGN_CENTER,flags=wx.dataview.DATAVIEW_COL_SORTABLE)
		self.m_dataViewListColumn13 = self.m_dataViewListCtrl4.AppendTextColumn( u"Action",align=wx.ALIGN_CENTER ,flags=wx.dataview.DATAVIEW_COL_SORTABLE)
		bSizer1.Add( self.m_dataViewListCtrl4, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.m_textCtrl23 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY )
		bSizer1.Add( self.m_textCtrl23, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
