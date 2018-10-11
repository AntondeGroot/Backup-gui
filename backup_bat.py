# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 17:04:57 2018
@author: Anton
"""

import datetime
import json
import os
import shutil
import time
import threading




datestamp = time.strftime("%d-%m-%Y")
keys = ["in","out","overwrite","threshold","lastupdate"]
datadir = os.getenv("LOCALAPPDATA")
datadir = datadir + r"\Backup"
jsonpath = os.path.join(datadir, 'data.json')

def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        if int(last) != int(last+avg):
            out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


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

# load
inputf = ''
outputf = ''        
# open data
with open(jsonpath, 'r') as file:
    diction = json.load(file)    
    lendict = len(diction[keys[0]])



#%% cronjobs
def job_loaddictionary():
    with open(jsonpath, 'r') as file:
        diction = json.load(file)    
    return diction

def job_dayspassed(diction,i):
    timestamp_then = datetime.datetime.strptime(diction['lastupdate'][i], "%d-%m-%Y")
    timestamp_now = datetime.datetime.now()
    delta = abs((timestamp_now - timestamp_then).days)    
    return delta

def job_walkthrough(diction): 
    # to walk through all directories and items and list them
    dirlist       = []
    inp           = []
    outp          = []
    overwritelist = []
    # check all backup entries
    lendict = len(diction[keys[0]])
    for i in range(lendict):
        input_dir      = diction['in'][i]
        output_dir     = diction['out'][i]
        threshold_days = diction['threshold'][i]  
        overwrite      = diction['overwrite'][i]
        delta          = job_dayspassed(diction,i)        
        # is it time to update
        if delta >= threshold_days: 
            try:
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                    # Now, if a user appends an entry, then the user does not need to create the map himself
            except:
                print("Drive {} is not connected".format(os.path.splitdrive(output_dir)[0]))
            if os.path.exists(output_dir):
                for root, dirs, files in os.walk(input_dir):
                    for file in files:
                        inp.append(os.path.join(root,file))
                        # split makes sure you also include the map name you're copying from
                        outp.append(os.path.join(output_dir,os.path.split(input_dir)[1],os.path.relpath(root, input_dir),file)) 
                        dirlist.append(os.path.join(output_dir,os.path.split(input_dir)[1],os.path.relpath(root, input_dir)))
                        overwritelist.append(overwrite)
                        # now you have 3 lists of equal length such that element i of list 1 corresponds to element i of list 3
                        # so that no further bookkeapings needs to be done.
    return inp, outp, dirlist, overwritelist

def job_transfer_files(inplist,outplist,writelist):    
    if len(inplist) > 0:
        for i in range(len(inplist)): # over all inputs                    
            # save unsaved files
            if not os.path.isdir(inplist[i]): 
                if writelist[i]: # if overwrite == True
                    shutil.copy2(inplist[i],outplist[i])                            
                else:
                    if not os.path.isfile(outplist[i]): # only if a file doesn't yet exist                                
                        shutil.copy2(inplist[i],outplist[i])                                
def job_backupprocedure(dictionlist):
    diction = dictionlist
    inp, outp, dirlist, overwritelist = job_walkthrough(diction)
    nr_threads = 4
    inputlist  = chunkIt(inp, nr_threads)
    outputlist = chunkIt(outp, nr_threads)
    writelist  = chunkIt(overwritelist, nr_threads)
    nrthreads = len(inputlist)
    
    job_make_all_dirs(dirlist)
    #print("all dirs made")
    for i in range(nrthreads):
        threading.Thread(target = job_transfer_files, name = 'thread{}'.format(i), args = (inputlist[i],outputlist[i],writelist[i])).start()
    return 4  

def job_make_all_dirs(dirlist):
    #print("dirlist {}".format(dirlist))
    for dir_i in dirlist:
        if not os.path.exists(dir_i):
            os.makedirs(dir_i)     

def execute_job():
    diction = job_loaddictionary()
    #print([diction])
    thr2 = threading.Thread(target = job_backupprocedure, name = 'thread2', args = ([diction]))
    thr2.run()

execute_job()
