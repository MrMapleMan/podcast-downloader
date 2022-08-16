# Find mp3 URLs for smash boom best

import urllib.request, urllib.error, urllib.parse
import re
import threading
import time
from os.path import exists

fa = re.findall
fi = re.finditer

def thread_function(name):
    print("Thread %s: starting", name)
    time.sleep(2)
    print("Thread %s: finishing", name)

def downloadMP3(url,folder='C:/Users/henri/Downloads/',overwrite=False,):
    # Find last slash
    slashes = fi('[\\/]',url)
    lastSlash = [i.start() for i in slashes][-1]
    final = url[lastSlash+1:]
    path = folder + str(final)
    print(path)
    if overwrite==False:
        if exists(path):
            print(path + ' exists already. ''overwrite''==False. Skipping.')
            return
    urllib.request.urlretrieve(url, path)
    print('Completed '+path)

##url='https://rss.art19.com/who-smarted'
url='https://feeds.publicradio.org/public_feeds/smash-boom-best/rss/rss'

response = urllib.request.urlopen(url)
webContent = response.read().decode('UTF-8')
print(len(webContent))
# Discard prefix section
x = [m.span() for m in re.finditer('item', webContent)][0]
webContent = webContent[x[0]:]
print(len(webContent))
titles = fa('<title>(.*?)</title>',webContent)
mp3_URLs = fa('http.*?mp3',webContent)

for i in mp3_URLs[:10]:
    print(i)

##for i in range(len(mp3_URLs)):
##    print('{:}\n\t{:}'.format(titles[i],mp3_URLs[i]))

print('Found {:} episodes.'.format(len(mp3_URLs)))

ans = input('Download file? "y" or "n"\n')

if ans.lower() == 'y':
    idx = 1
    x=[]
    downloadPath = 'C:/Users/henri/Downloads/'
    ans = input('Use default download path - ''y'' or ''n''? ('+downloadPath+')\n')
    if ans.lower() == 'n':
        downloadPath = input('Enter new download path.\n')
        if downloadPath[-1] != '/':
            downloadPath += '/'
    items = mp3_URLs[:]
    doThreading=False
    tStart = time.time()
    if(doThreading):
        for url in items:
            x.append(threading.Thread(target=downloadMP3, args=(url,downloadPath,False)))
            x[-1].start()
            time.sleep(0.010)
        for i in x:
            i.join()
    else:
        for i,url in enumerate(items):
            print("Processing episode %d of %d (%.0f%%, %.1f seconds elapsed)..." %(i+1,len(items),100.0*(i+1)/len(items),time.time()-tStart))
            print(titles[i])
            downloadMP3(url,downloadPath,False)
    
