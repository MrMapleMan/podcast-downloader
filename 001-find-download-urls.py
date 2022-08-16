# Find mp3 URLs for smash boom best

import urllib.request, urllib.error, urllib.parse
import re
fa = re.findall

url='https://rss.art19.com/who-smarted'
#url = 'http://www.oldbaileyonline.org/browse.jsp?id=t17800628-33&div=t17800628-33'

response = urllib.request.urlopen(url)
webContent = response.read().decode('UTF-8')

# Discard prefix section
x = [m.span() for m in re.finditer('item', webContent)][0]
webContent = webContent[x[0]:]

titles = fa('<title>(.*?)</title>',webContent)
mp3_URLs = fa('http.*?mp3',webContent)

for i in range(len(mp3_URLs)):
    print('{:}\n\t{:}'.format(titles[i],mp3_URLs[i]))

print('Found {:} episodes.'.format(len(mp3_URLs)))

ans = input('Download file? "y" or "n"')

if ans.lower() == 'y':
    idx = 1
    for url in mp3_URLs[20:50]:
        # print(url)
        final = fa('episodes\/(.*?mp3)',url)[0]
        # print(final) # TODO: remove after testing
        path = 'C:/Users/henri/Downloads/' + str(final)
        print(idx,path)
        urllib.request.urlretrieve(url, path)
        idx += 1

# for i in mp3_URLs[:10]:
#     print(i)
