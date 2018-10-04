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
import base64
try:
    del app
except:
    pass


datestamp = time.strftime("%d-%m-%Y")
keys = ["in","out","overwrite","threshold","lastupdate"]
datadir = os.getenv("LOCALAPPDATA")
datadir = datadir + r"\Backup"
jsonpath = os.path.join(datadir, 'data.json')

fh = open(os.path.join(datadir,"icon.png"), "wb")
iconstring = b'iVBORw0KGgoAAAANSUhEUgAAACYAAAAmCAYAAACoPemuAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAQtJREFUeNrsWNsNhCAQJFRACZRACXZwdqAdXAt0YAmUYgmUQAnGCjxMICHkIs8FP5hkPoyBnczgAiI0MDAQBNEUmofmlch7zGbmqAqaKcinrC1uryDKcq/p1lWZLFQURwj7AqzXpcYkCsCxo1TUBCDKci6JcgFsP5+SwQegY9lxzoCiLNecKCFjzI6TNHDLkqQ4Njfcg5Nq7Q0dkz23oBBpTJQtY0yqqTo4FoyTdRD198SBO/SurL6pOjqmYrYgaZ4poEPU1JChA6RwlBMgMXdh7n2FxElKPDVVXthseeRpxXVn8+8DGL0D59PL10bJGi9+Frv4kTm49WoXa8wFRDbejqbxB2ZgwOAnwABX6sAdGZxwrwAAAABJRU5ErkJggg=='
iconstring = b'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'
fh.write(base64.b64decode(iconstring))
fh.close()

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

def removerow(self,row):
    self.diction2 = self.diction
    self.diction2['in'].pop(row)
    self.diction2['out'].pop(row)
    self.diction2['overwrite'].pop(row)
    self.diction2['threshold'].pop(row)
    self.diction2['lastupdate'].pop(row)
    self.diction = self.diction2    
    #print(self.diction)
    savedictionary(self)
        
    gridreset(self)
    gridrefresh(self)

class MainFrame(gui.MyFrame):
    def __init__(self,parent):
        # initialize parent class
        gui.MyFrame.__init__(self,parent)
        
        iconimage = wx.Icon(os.path.join(datadir,"icon.png"), type=wx.BITMAP_TYPE_ANY, desiredWidth=-1, desiredHeight=-1)
        self.SetIcon(iconimage)
        
        # make sure that when an entry is changed it doesn't automatically trigger the grid changed event
        self.lastupdated = datetime.datetime.now() 
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
        
        if (datetime.datetime.now()-self.lastupdated).seconds>1: # wait at least a second, because any changes of the grid like GridRefresh would otherwise trigger this event again, resulting in an infinite loop
            print((datetime.datetime.now()-self.lastupdated).seconds)
            print(type((datetime.datetime.now()-self.lastupdated).seconds))
            self.lastupdated = datetime.datetime.now() 
            
            
            print("changed")
            # when a value is changed by the user
            row = event.GetRow()
            col = event.GetCol()
            value = self.m_grid1.GetCellValue(row, col)
            if col == 0 or col == 1:
                # note: it does not check if the given path is valid
                if value == '':
                    removerow(self,row)
                else:
                    self.diction[keys[col]][row] = value
                    savedictionary(self)
            
            if col == 2: 
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
                    removerow(self,row)
            if col == 3:
                try:
                    value = int(value) 
                    if value >= 0:
                        self.diction[keys[col]][row] = value
                        savedictionary(self)
                except:
                    if value == '':
                        removerow(self,row)
                    else:
                        print("Invalid input in 4th column")
                        self.diction[keys[col]][row] = 0
                        savedictionary(self)
                
            gridreset(self)        
            gridrefresh(self)
            self.m_grid1.ForceRefresh
            
        else:
            pass
            
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
