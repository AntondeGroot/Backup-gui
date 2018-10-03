# -*- coding: utf-8 -*-
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

#%% relating to datastorage
def loaddictionary(self):
    with open(jsonpath, 'r') as file:
        self.diction = json.load(file)    
        self.lendict = len(self.diction[keys[0]])

def savedictionary(self):
    with open(jsonpath, 'w') as file:
        file.write(json.dumps(self.diction)) 
    self.lendict = len(self.diction[keys[0]])
#%%
def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        if int(last) != int(last+avg):
            out.append(seq[int(last):int(last + avg)])
        last += avg

    return out

def walkthrough(self): 
    # to walk through all directories and items and list them
    self.dirlist       = []
    self.inp           = []
    self.outp          = []
    self.overwritelist = []
    # check all backup entries
    for i in range(self.lendict):
        input_dir      = self.diction['in'][i]
        output_dir     = self.diction['out'][i]
        threshold_days = self.diction['threshold'][i]  
        overwrite      = self.diction['overwrite'][i]
        dayspassed(self,i)        
        # is it time to update
        if self.delta >= threshold_days: 
            try:
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                    # Now, if a user appends an entry, then the user does not need to create the map himself
            except:
                print("Drive {} is not connected".format(os.path.splitdrive(output_dir)[0]))
            if os.path.exists(output_dir):
                for root, dirs, files in os.walk(input_dir):
                    for file in files:
                        self.inp.append(os.path.join(root,file))
                        # split makes sure you also include the map name you're copying from
                        self.outp.append(os.path.join(output_dir,os.path.split(input_dir)[1],os.path.relpath(root, input_dir),file)) 
                        self.dirlist.append(os.path.join(output_dir,os.path.split(input_dir)[1],os.path.relpath(root, input_dir)))
                        self.overwritelist.append(overwrite)
                        # now you have 3 lists of equal length such that element i of list 1 corresponds to element i of list 3
                        # so that no further bookkeapings needs to be done.
    self.m_gauge1.SetRange(len(self.inp))
    
    
def transfer_files(self,infolist):
    
    inplist   = infolist[0]
    outplist  = infolist[1]
    writelist = infolist[2]
    
    if len(inplist) > 0:
        for i in range(len(inplist)): # over all inputs
            self.k += 1
            self.m_gauge1.SetValue(self.k)                    
            # save unsaved files
            if not os.path.isdir(inplist[i]): 
                if writelist[i]: # if overwrite == True
                    shutil.copy2(inplist[i],outplist[i])                            
                    self.m_textCtrl1.SetValue("Backing up")
                else:
                    if not os.path.isfile(outplist[i]): # only if a file doesn't yet exist                                
                        shutil.copy2(inplist[i],outplist[i])                                
                        self.m_textCtrl1.SetValue("Backing up")    
    self.m_textCtrl1.SetValue('Back up finished')
    
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

def make_all_dirs(self):
    print("dirlist {}".format(self.dirlist))
    for dir_i in self.dirlist:
        if not os.path.exists(dir_i):
            os.makedirs(dir_i)
def backupprocedure(self):
    self.k = 0 
    print(threading.current_thread())
    walkthrough(self)
    nr_threads = 4
    inputlist  = chunkIt(self.inp, nr_threads)
    outputlist = chunkIt(self.outp, nr_threads)
    writelist  = chunkIt(self.overwritelist, nr_threads)
    nrthreads = len(inputlist)
    
    make_all_dirs(self)
    print("all dirs made")
    for i in range(nrthreads):
        listing = [inputlist[i],outputlist[i],writelist[i]]
        threading.Thread(target = transfer_files, name = 'thread{}'.format(i), args = (self,listing)).start()
    self.m_textCtrl1.SetValue('Back up finished')
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
                           "You can manually change the entries and confirm them by pressing enter.\n"
                           "0 days means you always check if you need to back it up")
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
thr_main = threading.Thread(target = runapp, name = 'mainthread',args = ())
thr_main.run()
