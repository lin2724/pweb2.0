# coding=utf-8
from __future__ import print_function
import os
import imghdr
#this is log file name store in each folder
ListStoreFile = 'filelist.log'


def GetSpecificLine(start, end=-1, folder='./'):
    with open(os.path.join(folder,ListStoreFile), 'r') as fd:
        tmp = []
        if end == -1:
            for i, line in enumerate(fd):
                if i >= start:
                    tmp.append(line[:-1])
            return tmp
        for i, line in enumerate(fd):
            if i >= start and i <= end:
                tmp.append(line[:-1])
            if i >= end:
                return tmp
        return tmp


def syncImgFileList(dir):
    fd = 0
    if not os.path.exists(dir):
        print ('err dir not exist %s'%(dir))
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


class syncFileListBuilder(object):
    ffolder = ''

    def __init__(self,folder):
        if not os.path.exists(folder):
            print ('err folder not exist %s'%(folder))
            return None
        self.ffolder = folder

    def syncFolder(self):
        syncImgFileList(self.ffolder)

    def getSpecificFile(self, start,end = -1):
        return GetSpecificLine(start, end, self.ffolder)


def main():
    syncImgFileList(os.getcwd())
    print('end')
if __name__ == '__main__':
    main()