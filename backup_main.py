"""
Created on Thu Aug 16 17:04:57 2018

@author: Anton
"""

import backup_gui as gui
import datetime
import json
import os
import shutil
import time
import threading
# wxpython
import wx
import wx._adv
import wx._html

try:
    del app
except:
    pass


itemlist = []
datestamp = time.strftime("%d-%m-%Y")
keys = ["in","out","overwrite","threshold","lastupdate"]
datadir = os.getenv("LOCALAPPDATA")
datadir = datadir + r"\Backup"
jsonpath = os.path.join(datadir, 'data.json')

#%% initializing localappdata folder with data file
if not os.path.exists(datadir):
    os.makedirs(datadir)

# checks if a json data file containing a dictionary exists: if not, create it
if not os.path.exists(jsonpath): 
    diction = {}
    with open(jsonpath, 'w') as file:
        for key in keys:
            diction.update({key : []})
        file.write(json.dumps(diction)) 
#%%        
def loaddictionary(self):
    with open(jsonpath, 'r') as file:
        self.diction = json.load(file)    
        self.lendict = len(self.diction[keys[0]])

def savedictionary(self):
    with open(jsonpath, 'w') as file:
        file.write(json.dumps(self.diction)) 
    self.lendict = len(self.diction[keys[0]])

def walkthrough(self): # os.walk: to walk through all directories and list them
    self.k          = 0
    self.dirlist_nr = 0
    self.itemnr     = 0 
    self.dirlist    = []
    self.inp        = []
    self.outp       = []
    self.indexlist  = []   
    # check if you even need to consider it
    for i in range(self.lendict):
        input_dir      = self.diction['in'][i]
        output_dir     = self.diction['out'][i]
        threshold_days = self.diction['threshold'][i]        
        dayspassed(self,i)        
        if self.delta >= threshold_days:
            if os.path.exists(output_dir):
                self.k += 1
                self.indexlist.append(i)
                self.inp.append(input_dir)
                self.outp.append(output_dir)
                subdir_list = [x[0] for x in os.walk(input_dir)]
                self.dirlist.append(subdir_list)
                self.dirlist_nr += len(subdir_list)   
    self.m_textCtrl1.SetValue(str(self.outp))    
    print(str(self.dirlist_nr))
    self.m_gauge1.SetRange(self.k)
    #print("k = {}".format(self.dirlist_nr))

def transfer_files(self):
    walkthrough(self)
    self.k = 0 
    if len(self.indexlist) > 0:
        for i in range(len(self.indexlist)): # approved indexes 
            self.inp[i]
            self.outp[i]
            self.dirlist[i]
            self.index = self.indexlist[i]
            subdir_list = self.dirlist[i]
            start_dir = os.path.basename(self.inp[i])            
            # make all directories first
            for dirs in subdir_list:
                
                rel_dir = os.path.relpath(dirs, self.inp[i])
                abs_path = os.path.join(*[self.outp[i],start_dir,rel_dir])                
                
                if not os.path.exists(abs_path):
                    os.makedirs(abs_path)
                    
            # then save every file in every directory
            for subdir in subdir_list:
                
                rel_dir = os.path.relpath(subdir, self.inp[i])
                abs_path = os.path.join(*[self.outp[i],start_dir,rel_dir]) 

                for item in os.listdir(subdir):
                    
                    if item not in itemlist:
                        itemlist.append(item)
                    
                    itempath = os.path.join(subdir,item)
                    outputpath = os.path.join(abs_path,item)
                    
                    # save unsaved files
                    if not os.path.isdir(itempath): 
                        self.k += 1
                        self.m_gauge1.SetValue(self.k)

                        if self.diction['overwrite'][self.index]: # if overwrite == True
                            shutil.copy2(itempath,abs_path)                            
                            if len(itemlist)>0:
                                self.m_textCtrl1.SetValue("writing to: {} , file: {}".format(self.outp[i],itemlist[-1]))
                        else:
                            if not os.path.isfile(outputpath):                                
                                shutil.copy2(itempath,abs_path)                                
                                if len(itemlist)>0:
                                    self.m_textCtrl1.SetValue("writing to: {} , file: {}".format(self.outp[i],itemlist[-1]))
    self.m_textCtrl1.SetValue('Back up finished')
    print("Backup finished")
    


def dayspassed(self,i):
    timestamp_then = datetime.datetime.strptime(self.diction['lastupdate'][i], "%d-%m-%Y")
    timestamp_now = datetime.datetime.now()
    self.delta = abs((timestamp_now - timestamp_then).days)


def gridreset(self):
    self.lendict = len(self.diction['in'])
    
    for i in range(self.lendict):
        self.m_grid1.DeleteRows(1)
    for i in range(self.lendict):
        self.m_grid1.AppendRows(1)
    if self.lendict == 0 :
        for col in range(4):
            self.m_grid1.SetCellValue(0, col, '')        
def gridrefresh(self):
    if self.lendict > 0:
        for row in range(self.lendict):
            for col in range(4):
                self.m_grid1.SetCellValue(row, col, str(self.diction[keys[col]][row]))



def backupprocedure(self):
    for i in range(self.lendict):
        self.input_dir  = self.diction['in'][i]
        self.output_dir = self.diction['out'][i]
        self.overwrite  = self.diction['overwrite'][i]
        self.threshold  = self.diction['threshold'][i]
        
        dayspassed(self,i)
        transfer_files(self)
    return 4
class MainFrame(gui.MyFrame):
    def __init__(self,parent):
        # initialize parent class
        gui.MyFrame.__init__(self,parent)
        
        # set initial directory
        self.m_dirSource.SetInitialDirectory('.')
        self.m_dirBackup.SetInitialDirectory('.')
        self.m_grid1.SetColLabelValue(0, "source")
        self.m_grid1.SetColLabelValue(1, "output")
        self.m_grid1.SetColLabelValue(2, "overwrite")
        self.m_grid1.SetColLabelValue(3, "backup per \nN days")
        self.input = ''
        self.output = ''        
        # set rich text
        self.txt = self.m_richText1
        self.txt.BeginBold()
        self.txt.BeginFontSize(12)
        self.txt.WriteText("Help\n")
        self.txt.EndFontSize()
        self.txt.EndBold()
        self.txt.WriteText("Select a folder you would like to backup, it will trace all subfolders and files within that folder.\n" \
                           "Then select a destination folder and confirm your selection. These selections are saved in \"%appdata%/local/Backup\" .\n"
                           "To remove a row of entries: simply delete one entry and press enter, the rest of the row will then be deleted.\n"
                           "You can manually change the entries and confirm them by pressing enter.")
        # start multithread
        self.thr2 = threading.Thread(target = backupprocedure, name = 'thread2', args = (self, ))
        loaddictionary(self)
        if self.lendict > 4:
            self.m_grid1.AppendRows(self.lendict-4)
        
        gridreset(self)
        gridrefresh(self)
        
        
    ## LOAD ALL DATA ==========================================================
    def m_grid1OnGridCellChanged( self, event ): #in gui file it's called ...CellChange, error comes from wxbuilder, add the missing d in the gui file
        # when a value is changed by the user
        row = event.GetRow()
        col = event.GetCol()
        value = self.m_grid1.GetCellValue(row, col)
        # see what was changed
        if 'False' in value:
            value = False
            self.diction[keys[col]][row] = value
            savedictionary(self)
        elif 'True' in value:
            value = True
            self.diction[keys[col]][row] = value
            savedictionary(self)
        elif value == '':
            # then remove this row
            
            self.diction2 = self.diction
            self.diction2['in'].pop(row)
            self.diction2['out'].pop(row)
            self.diction2['overwrite'].pop(row)
            self.diction2['threshold'].pop(row)
            self.diction2['lastupdate'].pop(row)
            self.diction = self.diction2    
            print(self.diction)
            savedictionary(self)
                
            gridreset(self)
            gridrefresh(self)
        else:
            try:
                value = int(value) 
                if value >= 0:
                    self.diction[keys[col]][row] = value
                    savedictionary(self)
            except:
                pass
            
        gridreset(self)        
        gridrefresh(self)
        self.m_grid1.ForceRefresh
        
    def m_dirSourceOnDirChanged( self, event ):                
        self.input = event.GetPath()
        
    def m_dirBackupOnDirChanged( self, event ):
        self.output = event.GetPath()
        
    def m_btnBackupOnButtonClick( self, event ):  
        # start backup process in another thread
        try:
            #self.thr2 = threading.Thread(target = backupprocedure, name = 'thread2', args = (self, ))
            self.thr2.start()
                        
        except:
            self.thr2 = threading.Thread(target = backupprocedure, name = 'thread2', args = (self, ))
            self.thr2.run()

    def m_btnAddOnButtonClick( self, event ):
        col, row = 0 , 0 
        
        self.m_dirSource.SetInitialDirectory('.')
        self.m_dirBackup.SetInitialDirectory('.')
        self.m_dirSource.SetPath('')
        self.m_dirBackup.SetPath('')
        # load dictionary
        loaddictionary(self)
        
        if self.input != '' and self.output != '':
            if self.lendict == 0:
                self.diction.update({'in' : [self.input]})
                self.diction.update({'out' : [self.output]})
                self.diction.update({'overwrite' : [False]})
                self.diction.update({'threshold': [1]})
                self.diction.update({'lastupdate': [datestamp]})
            else:
                self.diction['in'].append(self.input)
                self.diction['out'].append(self.output)
                self.diction['overwrite'].append(False)
                self.diction['threshold'].append(1)
                self.diction['lastupdate'].append(datestamp)
                for key in keys:
                    self.diction.update({key : self.diction[key]})
                
            savedictionary(self)
            
            if self.lendict > 4: # set minimum of 4 rows visible for user
                self.m_grid1.AppendRows(1)
            if self.lendict > 0:
                for row in range(self.lendict):
                    for col in range(4):           
                        self.m_grid1.SetCellValue(row, col, str(self.diction[keys[col]][row]))
        else:
            self.input  = ''
            self.output = ''
        gridreset(self)    
        gridrefresh(self)        
        
def runapp():
    app = wx.App(False) 
    frame = MainFrame(None)
    frame.Show(True)
    app.MainLoop()
    
    
# initialize a thread, named 't'
thr1 = threading.Thread(target = runapp, name = 'thread1',args = ())
thr1.run()
