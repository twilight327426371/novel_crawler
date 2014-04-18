#encoding=utf-8
import os,re,sys
from bs4 import BeautifulSoup 
import requests
#from threading import Thread, Lock
#import inspect
#from collections import deque
#from Queue import Queue,Empty

def parse_url(func):
    def _parse(*args):
        #url=inspect.getcallargs(func,*args)
        #print url
        res=requests.get(url,timeout=10)
        res.encoding='gb2312'
        page=re.sub('&nbsp;',' ',res.text)
        func(page)
    return _parse

def get_author_links(url):
    res=requests.get(url,timeout=10)
    res.encoding='gb2312'
    page=re.sub('&nbsp;',' ',res.text)
    soup=BeautifulSoup(page)
    link=[]
    for url in soup.find_all('table',cellpadding="3"):
        link.append(url.find('a').get('href'))
    link1=list(set([i for i in link if i.startswith('/files')]) )
    return link1

def get_book_links(url):
    res=requests.get(url,timeout=10)
    res.encoding='gb2312'
    page=re.sub('&nbsp;',' ',res.text)
    soup=BeautifulSoup(page)
    dir_name=soup.find('h2').text.encode('utf-8')
    #if len(dir_name)>100:
        #dir_name=re.sub('(\r|\n|<br \/>)',' ',dir_name)
        #dir_name=dir_name.decode('utf-8')[0:30]
    print dir_name
    books_link={}
    if not os.path.exists(dir_name):
        os.mkdir("./%s"%dir_name)
    else:
        return books_link,dir_name
    s=soup.find('table',cellspacing="1")
    for link in s.find_all('a'):
        books_link[link.text]=link.get('href')

    return books_link,dir_name

def get_chapts_links(url):
    res=requests.get(url,timeout=10)
    res.encoding='gb2312'
    page=re.sub('&nbsp;',' ',res.text)
    soup=BeautifulSoup(page)
    s=soup.find_all('table',cellspacing="1")
    if len(s)>1:
        sour=s[1]
    else:
        sour=s[0]
    links=[]
    for link in sour.find_all('a'):
        links.append(link.get('href'))

    fi=[re.sub('\.\/','',i) for i in links]
    return  fi

def get_text(url):
    res=requests.get(url,timeout=10)
    res.encoding='gb2312'
    page=re.sub('&nbsp;',' ',res.text)
    soup=BeautifulSoup(page)
    #with open('text.txt','a') as f:
        #f.write(soup.find('p').text.encode('gb2312'))
    return soup.find('p').text.encode('utf-8')


head='http://book.kanunu.org'
#unvisitedHrefs=deque()

def download(url):
    books_url,dir_name=get_book_links(url)
    for book in books_url.keys():
    #open文件夹时必须解码dir_name
        with open('%s/%s.txt'%(dir_name.decode('utf-8'),book),'a') as f:
            if not books_url[book].startswith('http'):
                book=head+books_url[book]
                print 'book:'+book+'\n'
                chapts=get_chapts_links(book)
                for chapt in chapts:
                    chapt=book+chapt
                    print chapt
                    text=get_text(chapt)
                    f.write(text)
def prints(url):
    print "nihao"+url
    

url="http://book.kanunu.org/files/writer/18-%d.html"
urls=[url%i for i in range(1,15)]

if __name__=='__main__':
    for url in urls:
        print url
        authors=get_author_links(url)
        for url in authors:
            url=head+url
            print 'url:'+url
            download(url)







    
