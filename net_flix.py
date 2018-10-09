import os
import re
import requests
from bs4 import BeautifulSoup
import json
from configparser import ConfigParser
from selenium import webdriver
import time
import codecs
import math
import Netflix_XmlToSrt
from selenium.webdriver.common.keys import Keys
import urllib.request

def getResources(driver,lk,idd):
    driver.get(lk)
    time.sleep(10)
    resourceList = []
    sub_url=""
    #print("Searching for subtitle")
    resourceList = driver.execute_script("return window.performance.getEntries();")
    for i in resourceList:
        if 'name' in i.keys():
          #print(i['name'])
          if "nflxvideo.net/?o" in i['name']:
            #print("Here")
            sub_url=i['name']
    
    if sub_url=="":
      print("No Subtitle Found")
      return False
    else:
      #print("Downloading XML")
      subRequestObject = requests.get(sub_url)
      subsFileHandler = open(str(idd) + ".xml","w",encoding='utf-8')
      subsFileHandler.write(subRequestObject.text)
      subsFileHandler.close()
      #print("Converting XML to SRT")
      #converting xml to srt
      filename = str(idd) + ".xml"
      outputFile = str(idd) + ".srt"
      with codecs.open(filename, 'rb', "utf-8") as f:
          text = f.read()
      with codecs.open(outputFile,'wb',"utf-8") as f:
          f.write(Netflix_XmlToSrt.to_srt(text))
      os.remove(str(idd) + ".xml")
      os.rename(str(idd) + ".srt","netflix-data/"+str(idd) + ".srt")
      print("Subtitle Found")
      return True

def extract(driver,lk,idd):
    lk=lk.replace('watch','title')
    driver.get(lk)
    html=driver.page_source
    soup=BeautifulSoup(html,"lxml")
    year=soup.find('span',{'class':'year'}).text
    try:
      title=soup.find('div',{'class':'text image-fallback-text'}).text
    except:
      title=soup.find('img',{'class':'logo'}).attrs['alt']
    duration=soup.find('span',{'class':'duration'}).text
    j={'data':[]}
    j['data'].append({'title':title})
    j['data'].append({'id':idd})
    j['data'].append({'year':year})
    j['data'].append({'duration':duration})
    gen=soup.find('p',{'class':'genres inline-list'})
    gens=[]
    try:
      gen_a=gen.findAll('a')
      for i in gen_a:
        gens.append(i.text)
    except:
      pass
    j['data'].append({'genres':gens})
    with open(str(idd)+'.json', 'w') as outfile:
      json.dump(j, outfile)
    os.rename(str(idd)+'.json', "netflix-data/"+str(idd)+'.json')
    print("--Done--")

def extract1(title,titles,durations,year,idd):
    j={'data':[]}
    j['data'].append({'title':titles})
    j['data'].append({'series':title})
    j['data'].append({'id':idd})
    j['data'].append({'year':year})
    j['data'].append({'duration':durations})
    j['data'].append({'genres':'tvshow'})
    with open(str(idd)+'.json', 'w') as outfile:
      json.dump(j, outfile)
    os.rename(str(idd)+'.json', "netflix-data/"+str(idd)+'.json')
    print("--Done--")
    
def netflix(netflixDriver,lk,idd,img,title,titles,durations,year):
  chk=getResources(netflixDriver,lk,idd)
  if chk:
    if title==None:
      extract(netflixDriver,lk,idd)
    else:
      extract1(title,titles,durations,year,idd)
    #print(img)
    urllib.request.urlretrieve(img, str(idd)+".webp")
    os.rename(str(idd)+".webp", "netflix-data/"+str(idd)+".webp")
  else:
    fh = open(str(idd)+".nosub","w")
    fh.close()
    os.rename(str(idd) + ".nosub", "netflix-data/"+str(idd) + ".nosub")
  #netflixDriver.close()
  #netflixDriver.quit()