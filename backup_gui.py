# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid
import wx.richtext

###########################################################################
## Class MyFrame
###########################################################################

class MyFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 720,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.Size( 720,600 ), wx.Size( -1,600 ) )
		self.SetBackgroundColour( wx.Colour( 254, 250, 252 ) )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel2.SetMinSize( wx.Size( 700,110 ) )
		self.m_panel2.SetMaxSize( wx.Size( 700,80 ) )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText1 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Select source", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		self.m_staticText1.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 75, 90, 92, False, wx.EmptyString ) )
		
		fgSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )
		
		self.m_dirSource = wx.DirPickerCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		self.m_dirSource.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 75, 90, 90, False, wx.EmptyString ) )
		self.m_dirSource.SetMinSize( wx.Size( 300,-1 ) )
		
		fgSizer1.Add( self.m_dirSource, 0, wx.ALL, 0 )
		
		self.m_staticText2 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Back-up destination", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		self.m_staticText2.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 75, 90, 92, False, wx.EmptyString ) )
		
		fgSizer1.Add( self.m_staticText2, 0, wx.ALL, 5 )
		
		self.m_dirBackup = wx.DirPickerCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		self.m_dirBackup.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 75, 90, 90, False, wx.EmptyString ) )
		self.m_dirBackup.SetMinSize( wx.Size( 300,-1 ) )
		
		fgSizer1.Add( self.m_dirBackup, 0, wx.ALL, 0 )
		
		self.m_bitmap1 = wx.StaticBitmap( self.m_panel2, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 10,10 ), 0 )
		self.m_bitmap1.Enable( False )
		self.m_bitmap1.SetMinSize( wx.Size( 10,10 ) )
		self.m_bitmap1.SetMaxSize( wx.Size( 10,10 ) )
		
		fgSizer1.Add( self.m_bitmap1, 0, wx.ALL, 5 )
		
		self.m_btnAdd = wx.Button( self.m_panel2, wx.ID_ANY, u"Add Selection", wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		self.m_btnAdd.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 75, 90, 90, False, wx.EmptyString ) )
		
		fgSizer1.Add( self.m_btnAdd, 0, wx.ALL, 0 )
		
		
		bSizer2.Add( fgSizer1, 1, wx.EXPAND, 5 )
		
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer2.Add( bSizer9, 1, wx.EXPAND, 5 )
		
		
		self.m_panel2.SetSizer( bSizer2 )
		self.m_panel2.Layout()
		bSizer2.Fit( self.m_panel2 )
		bSizer1.Add( self.m_panel2, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticline3 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 0 )
		
		self.m_panel3 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		self.m_panel3.SetMinSize( wx.Size( -1,200 ) )
		self.m_panel3.SetMaxSize( wx.Size( -1,200 ) )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_grid1 = wx.grid.Grid( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		self.m_grid1.CreateGrid( 4, 4 )
		self.m_grid1.EnableEditing( True )
		self.m_grid1.EnableGridLines( True )
		self.m_grid1.EnableDragGridSize( False )
		self.m_grid1.SetMargins( 0, 0 )
		
		# Columns
		self.m_grid1.SetColSize( 0, 200 )
		self.m_grid1.SetColSize( 1, 200 )
		self.m_grid1.SetColSize( 2, 80 )
		self.m_grid1.SetColSize( 3, 120 )
		self.m_grid1.EnableDragColMove( False )
		self.m_grid1.EnableDragColSize( True )
		self.m_grid1.SetColLabelSize( 30 )
		self.m_grid1.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.m_grid1.EnableDragRowSize( True )
		self.m_grid1.SetRowLabelSize( 80 )
		self.m_grid1.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.m_grid1.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		self.m_grid1.SetMinSize( wx.Size( 700,200 ) )
		
		bSizer4.Add( self.m_grid1, 0, wx.ALL, 0 )
		
		
		self.m_panel3.SetSizer( bSizer4 )
		self.m_panel3.Layout()
		bSizer4.Fit( self.m_panel3 )
		bSizer1.Add( self.m_panel3, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 0 )
		
		self.m_panel4 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel4.SetMaxSize( wx.Size( 700,70 ) )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_btnBackup = wx.Button( self.m_panel4, wx.ID_ANY, u"Backup", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_btnBackup.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 75, 90, 90, False, wx.EmptyString ) )
		
		bSizer5.Add( self.m_btnBackup, 0, wx.ALL, 0 )
		
		self.m_textCtrl1 = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 500,-1 ), 0 )
		self.m_textCtrl1.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 75, 90, 90, False, wx.EmptyString ) )
		self.m_textCtrl1.Enable( False )
		self.m_textCtrl1.SetMinSize( wx.Size( 700,-1 ) )
		
		bSizer5.Add( self.m_textCtrl1, 0, wx.ALL, 0 )
		
		self.m_gauge1 = wx.Gauge( self.m_panel4, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gauge1.SetValue( 0 ) 
		self.m_gauge1.SetMinSize( wx.Size( 700,-1 ) )
		
		bSizer5.Add( self.m_gauge1, 0, wx.ALL, 0 )
		
		
		self.m_panel4.SetSizer( bSizer5 )
		self.m_panel4.Layout()
		bSizer5.Fit( self.m_panel4 )
		bSizer1.Add( self.m_panel4, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.m_richText1 = wx.richtext.RichTextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
		self.m_richText1.Enable( False )
		
		bSizer1.Add( self.m_richText1, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_dirSource.Bind( wx.EVT_DIRPICKER_CHANGED, self.m_dirSourceOnDirChanged )
		self.m_dirBackup.Bind( wx.EVT_DIRPICKER_CHANGED, self.m_dirBackupOnDirChanged )
		self.m_btnAdd.Bind( wx.EVT_BUTTON, self.m_btnAddOnButtonClick )
		self.m_grid1.Bind( wx.grid.EVT_GRID_CELL_CHANGED, self.m_grid1OnGridCellChanged )
		self.m_btnBackup.Bind( wx.EVT_BUTTON, self.m_btnBackupOnButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def m_dirSourceOnDirChanged( self, event ):
		event.Skip()
	
	def m_dirBackupOnDirChanged( self, event ):
		event.Skip()
	
	def m_btnAddOnButtonClick( self, event ):
		event.Skip()
	
	def m_grid1OnGridCellChanged( self, event ):
		event.Skip()
	
	def m_btnBackupOnButtonClick( self, event ):
		event.Skip()
	

