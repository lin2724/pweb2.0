import web
import os
import sys
import re
import weibo_token
from common_lib import FileListSync
from syncFileList import syncFileListBuilder

token_store_file = 'token.db'


urls = ('/img','index',
         "/photolib/*", "photolib",
         '/photodetail/*','photolib_sub',
        '/list','ListFolder',
        '/auth','weibo_auth',
        '/gettoken','givetoken',
        '/delete.asp','PhotoDelete',
        '/*','HomePage',
        )#,('/xxx','index2'

def changeWorkPath():
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
    print 'now workpath is %s' % os.getcwd()


def tostr(ints):
    return str(ints)


def getImgFileName(start,end = -1, folder = None, sync='y'):
    folder = os.path.join('static', folder)
    return FileListSync().get_file_list(folder, start, end)
    ret = []
    if not folder:
        print 'ERR no folder given'
        return ret
    srcpath = os.path.join('static' , folder)
    if not os.path.exists(srcpath):
        print ('srcpath not exist %s' % srcpath)
        return ret
    syncHandler = syncFileListBuilder(srcpath)
    if sync=='y':
        syncHandler.syncFolder()
    tmp = syncHandler.getSpecificFile(start, end)
    return tmp

render = web.template.render( 'templates/', globals={'os': os, 'tostr': tostr, 'getImgFileName': getImgFileName})


class HomePage:
    def GET(self):
        user_data = web.input(id=[])
        return ('<a href="http://192.168.8.198:8080/photolib?ImgLib=adult_img&&pages=1&&sync=n">click here</a>')


class index:
    def GET(self):
        user_data = web.input(id=[])
        imgid = user_data.id
        for i in imgid:
            print "img is is " + i
        return render.index(imgid)


class task:
    def GET(self):
         user_data = web.input(id=[])
         return user_data
#for i in user_data:
            # yield "received id is %s"%i#user_data.id


class index2:
    def GET(self):
        greeting = "im index2"
        return render.index(greeting = greeting)


def ListDir(curdir):
    return os.listdir(curdir)


class photolib:
    def GET(self):
        user_data = web.input(pages=[0], SubHref='photodetail', ImgLib='img', sync='y')
        return render.PhotoLib(user_data)#,globals={'ldir':ListDir}


class photolib_sub:
    def GET(self):
        user_data = web.input(name='default',ImgLib='img')
        return render.PhotoLib_2(user_data)#,globals={'ldir':ListDir}

class ListFolder:
    def GET(self):
        print os.getcwd()
        folders = list()
        folders = FileListSync().get_folder_list('static', 0, 100)
        user_data = web.input(pages=[0], folder_list=folders)
        return render.folder_list(user_data)#,globals={'ldir':ListDir}

class PhotoDelete:
    def __init__(self):
        pass

    def GET(self):
        user_data = web.input()
        if user_data.has_key('file'):
            file_name = user_data.get('file')
            file_name = os.path.normpath(file_name)
            full_file_path = os.path.join(os.getcwd(), file_name)
            print 'delete %s ' % full_file_path
            try:
                os.remove(full_file_path)
            except:
                print 'delete fail %s' % full_file_path
            return '/'
        else:
            print 'no file specific'


class weibo_auth:
    def GET(self):
        token_file_tmp = 'token.tmp'

        user_data = web.input()
        print (type(user_data))
        if user_data.has_key('code'):
            if weibo_token.get_token(user_data.get('code'), token_file_tmp):
                weibo_token.store_token(token_file_tmp, token_store_file)
            print (user_data.get('code'))
            return ('<h1>we have received code ,thanks</h1><br><h3>by zzl 2016.6.12<h3>')
        else:
            return ('<h1>wrong code</h1>')


class givetoken:
    def GET(self):
        PassWord = '111222333'
        user_data = web.input()
        if user_data.has_key('password'):
            passwd = user_data.get('password')
            if passwd == PassWord:
                if os.path.exists(token_store_file):
                    with open(token_store_file, 'r') as fd:
                        return fd.read()
                else:
                    return ('<h1>Token Not Found</h1>')
            else:
                return ('<h1>Permission denied !</h1>')
        return ('<h1>Permission denied !</h1>')
app = web.application(urls, globals())
if __name__=="__main__":
    changeWorkPath()
    app.run()
