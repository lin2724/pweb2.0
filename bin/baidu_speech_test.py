# coding=utf-8
import urllib
import urllib2
import sys
import time
import os
import hashlib
try:
    import pydub
    gUsingPyDub = True
except ImportError:
    gUsingPyDub = False
    pass


def _get_param_by_text(text):
    urlpro = urllib.quote(text)
    if _get_text_len(urlpro) >= 200:
        print ('ERROR: text is out of range!')
        return None
    #print ('text len %d' % _get_text_len(urlpro))
    i = 0
    while True:
        if i >= len(urlpro):
            break
        if urlpro[i] == '%':
            urlpro = urlpro[:i+1] + '25' + urlpro[i+1:]
        i += 1
        if i >= 300:
            break
    return urlpro


def _get_girl_url(arg):
    url = tmpurl = 'http://tts.baidu.com/text2audio?idx=1&tex=%s&cuid=baidu_speech_demo&cod=2&lan=zh&ctp=1&pdt=1&spd=5&per=0&vol=5&pit=5' % arg
    return url


def get_man_url(arg):
    url =  'http://tts.baidu.com/text2audio?idx=1&tex=%s&cuid=baidu_speech_demo&cod=2&lan=zh&ctp=1&pdt=1&spd=5&per=3&vol=5&pit=5' % arg
    return url


def _get_mp3_form_url(url, storepath):
    filename = 'tmp.mp3'
    newnamepath = None
    if not os.path.exists(storepath):
        os.mkdir(storepath)
    try:
        newname = md5(url) + '.mp3'
        newnamepath = os.path.join(storepath, newname)
        if os.path.exists(newnamepath):
            print 'Already have this mp3 skip'
            return newnamepath
        content = urllib2.urlopen(url, timeout=500).read()
        with open(os.path.join(storepath, filename), 'wb+') as fd:
            fd.write(content)

        if os.path.exists(newname):
            os.remove(newname)
        try:
            os.rename(os.path.join(storepath, filename), newnamepath)
        except:
            pass
        print ('done')
    except urllib2.HTTPError:
        print (sys.exc_info()[0])
    return newnamepath


def _get_text_len(urlpro):
    i = 0
    ass = 0
    utf = 0
    while True:
        if urlpro[i] == '%':
            i += 3
            utf += 1
        else:
            ass += 1
            i += 1
        if i >= len(urlpro):
            break
    return (ass+1)/2 + (utf+2)/3


def get_mp3_by_text(text, store_path=None):
    mp3url = _get_girl_url(_get_param_by_text(text))
    if not store_path:
        store_path = 'audio'
    mp3file =  _get_mp3_form_url(mp3url, store_path)
    return mp3file


def get_wav_by_file(file):
    mpfile = list()
    with open(file, 'r') as fd:
        while True:
            line = fd.read(380)
            if not line:
                print ('done')
                break
            if len(line) == 380:
                fd.seek(-2, os.SEEK_CUR)
            print line
            tmp = get_mp3_by_text(line)
            if tmp:
                mpfile.append(tmp)
            #print line
        mpfile = _convert_to_wav(mpfile)

    return mpfile


def md5(fname):
    hash_md5 = hashlib.md5()
    hash_md5.update(fname)
    return hash_md5.hexdigest()
    """
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
    """


def _convert_to_wav(files):
    print ('convert')
    converttype = 'wav'
    newfiles = []
    if not gUsingPyDub:
        print 'Failed to get pydub'
        return ''
    print (files)
    for fil in files:
        song = pydub.AudioSegment.from_mp3(fil)
        print ('song long %d' % song.duration_seconds)
        newfilepath =  fil.split('.')[0] + '.' + converttype
        print (newfilepath)
        if os.path.exists(newfilepath):
            os.remove(newfilepath)
        song.export(newfilepath, format=converttype)
        os.remove(fil)
        newfiles.append(newfilepath)
        print ('done')
    if not newfiles:
        return newfiles
    song = pydub.AudioSegment.from_wav(newfiles[0])
    for fil in newfiles[1:]:
        song += (pydub.AudioSegment.from_wav(fil))
    tmpfilpath = os.path.join(os.path.dirname(newfilepath), 'pydub_convert_tmp')
    if os.path.exists(tmpfilpath):
        os.remove(tmpfilpath)
    song.export(tmpfilpath, format=converttype)
    #for fil in newfiles:
     #   os.remove(fil)
    newfilepath = os.path.join(os.path.dirname(tmpfilpath), md5(tmpfilpath) + '.' + converttype)
    if os.path.exists(newfilepath):
        os.remove(newfilepath)
    os.rename(tmpfilpath, newfilepath)
    print ('convert done')
    return newfilepath

if __name__ == '__main__':
    get_mp3_by_text("大家晚上好", None)

    #file =[]
    #file.append(os.path.join('audio', 'huoyuanjia.mp3'))
    #print (_convert_to_wav(file))




