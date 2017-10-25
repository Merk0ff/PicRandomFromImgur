import urllib.request
import random
import time
import select
import sys
import os
from bs4 import BeautifulSoup

chars = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4","5","6","7","8","9"]

def GenerateUrl_postfix():
    return random.choice(chars) + random.choice(chars) + random.choice(chars) + random.choice(chars) \
           + random.choice(chars)

def GenerateUrl():

    url = 'https://imgur.com/' + GenerateUrl_postfix()

    try:
        urllib.request.urlopen(url, timeout=1)
    except urllib.error.URLError as e:
        print(url + " : " + str(e))
        return -1

    return url


def GetImg( url ):

    try:
        html = urllib.request.urlopen(url, timeout=1)
    except urllib.error.URLError as e:
        print(url + ' : ' + str(e))
        return

    soup = BeautifulSoup(html, "html.parser")

    img_src = soup.img['src']

    if len(img_src) > 0:
        ex = img_src[14:]
        try:
            urllib.request.urlretrieve("https:" + img_src, "img/file_" + ex)
        except urllib.error.URLError as e:
            print("Some hell is going on: " + str(e))

def LoadProxy():
    list = []

    with open("./src/proxy.list", "r") as file:
        for line in file:
            list.append(line[0:-2])

    return list

def ConnectToProxy( proxy ):
    proxy = urllib.request.ProxyHandler({'http': proxy})
    opener = urllib.request.build_opener(proxy)
    urllib.request.install_opener(opener)
    print("Proxy changed")

def main():
    i = 0
    elem = 1

    Plist = LoadProxy()
    ConnectToProxy(Plist[0])

    while not select.select([sys.stdin,],[],[],0.0)[0]:

        if i >= 3:
            ConnectToProxy(Plist[elem])
            elem += 1

            if elem >= len(Plist):
                elem = 0

            i = 0

        url = GenerateUrl()

        if url != -1:
            GetImg(url)
            with open("log.txt", "a") as file:
                file.write(url + "\n")

        i += 1
        time.sleep(0.5)


if not os.path.exists("img"):
    os.makedirs("img")

main()