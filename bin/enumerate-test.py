from __future__ import print_function
import os
import imghdr
#this is log file name store in each folder
ListStoreFile = 'filelist.log'


def GetSpecificLine(start,end,file):
    with open(file) as fd:
        tmp = []
        for i, line in enumerate(fd):
            if i >= start and i <= end:
                tmp.append(line)
            if i >= end:
                return tmp
        return None

def syncImgFileList(dir):
    fd = 0
    if not os.path.exists(dir):
        print ('err dir not exist')
        return False
    # check if folder has a newer change-time than log file
    if not os.path.exists(os.path.join(dir,ListStoreFile)):
        fd = open(os.path.join(dir, ListStoreFile), 'w+')
    if(os.stat(dir).st_mtime < os.stat(os.path.join(dir,ListStoreFile)).st_mtime):
        print ('list already new')
    else:
        if not fd:
            fd = open(os.path.join(dir, ListStoreFile), 'w+')  #open with 'w' write through
        print ('list need sync')
        for fil in os.listdir(dir):
            if imghdr.what(os.path.join(dir, fil)):   #check if it is a img file
                fd.write(fil)
                fd.write('\n')
        #print (os.stat(dir).st_mtime)
        #print (os.stat(os.path.join(dir,ListStoreFile)).st_mtime)
        fd.close()
def GetImgFileName(start,end):
    return GetSpecificLine(start,end,ListStoreFile)

def main():
    #tmp = GetSpecificLine(2,5,os.path.join(os.getcwd(),'CSV.py'))
    #print (tmp)
    #print (os.stat(os.getcwd()).st_mtime)
    syncImgFileList(os.path.join(os.getcwd(), 'full'))
    print('end')

main()