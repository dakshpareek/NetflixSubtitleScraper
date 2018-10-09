#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import time, sys,re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from net_flix import netflix
from urllib.request import Request, urlopen
import json
from pathlib import Path

class RealComp:
    firsttime = 'true'

    def __init__(self):
        
        #mine end
        path = 'C://chromedriver.exe'
        self.driver = webdriver.Chrome(path)
        #self.driver.maximize_window ()
        '''
        options = Options ()
        options.add_argument ('--no-sandbox')
        options.add_argument ('--disable-dev-shm-usage')
        path = 'C://chromedriver.exe'
        self.driver = webdriver.Chrome (chrome_options=options)
        '''

    def login(self):

        self.driver.implicitly_wait (10)
        self.driver.get ("https://www.netflix.com/login")
        print ("Logging In.")
        self.driver.find_element_by_id ('email').send_keys ("nicoleypoli@gmail.com")
        self.driver.find_element_by_id ('password').send_keys ("testnetflix")
        self.driver.find_element_by_id ("password").send_keys (u'\ue007')
        self.driver.find_element_by_xpath ('//*[@id="appMountPoint"]/div/div/div/div[2]/div/div/ul/li[2]/div/a/div/div').click()
        print ("Logged In.")
        

    def get_data(self,Soup,chk=False,title=None,year=None):
        soup1=Soup.findAll('a',href=re.compile("/watch"))
        #print(len(soup1))
        if chk==False:
          cls='boxart-image boxart-image-in-padded-container'
          images1=Soup.findAll('img',{'class':cls})
          images=[]
          titles=[]
          durations=[]
          for k in images1:
            images.append(k.attrs['src'])
            titles.append(None)
            durations.append(None)
        else:
          cls='episodeArt video-artwork'
          images1=Soup.findAll('div',{'class':cls})
          images=[]
          for k in images1:
            img=k.attrs['style']
            a1=img.find('("')
            a2=img.find('")')
            images.append(img[a1+2:a2])
          titles1=Soup.findAll('p',{'class':'ellipsized'})
          titles=[]
          for k in titles1:
            titles.append(k.text)
          durations1=Soup.findAll('span',{'class':'duration'})
          durations=[]
          for k in durations1:
            durations.append(k.text)
        for i,j in enumerate(soup1):
          img=images[i]
          lk=j.attrs['href']
          lk="https://www.netflix.com"+lk
          #print(lk)
          a1=lk.find('h/')
          a2=lk.find('?')
          idd=lk[a1+2:a2]
          if Path("netflix-data/"+str(idd) + ".nosub").is_file():
            print("Skipping (No Subtitle)")
          else:
            if Path("netflix-data/"+str(idd) + ".srt").is_file():
              print("Skipping (Already Exist)")
            else:
              print("Getting:"+str(idd))
              #print(lk,idd,img,title,titles[i],durations[i],year)
              netflix(self.driver,lk,idd,img,title,titles[i],durations[i],year)

    def first_scrap(self):
        self.login ()
        time.sleep(2)
        self.driver.get("https://www.netflix.com/browse/genre/34399?so=az")
        SCROLL_PAUSE_TIME = 1.5
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            html=self.driver.page_source
            Soup = BeautifulSoup(html,"lxml")
            self.get_data(Soup)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            print("..Scrolling..")
            if new_height == last_height:
                break
            last_height = new_height
        #netflix(self.driver)
        
    def shows(self,year):
        #print("Here")
        st='//*[@id="pane-Episodes"]/div/div/div/div[2]/div/div/span/b'
        while True:
          try:
            self.driver.find_element_by_xpath(st).click()
            #print("Scrolling")
          except:
            break
        
        html=self.driver.page_source
        Soup = BeautifulSoup(html,"lxml")
        soup1=Soup.find('div',{'class':'sliderMask'})
        try:
          title=Soup.find('div',{'class':'text image-fallback-text'}).text
        except:
          title=Soup.find('img',{'class':"logo"}).attrs['alt']
        self.get_data(soup1,True,title,year)

    def serial(self,url):
        #self.login()
        #time.sleep(5)
        #self.driver.get('https://www.netflix.com/browse/genre/83?so=az')
        self.driver.get(url)
        time.sleep(3)
        html=self.driver.page_source
        Soup = BeautifulSoup(html,"lxml")
        year=Soup.find('span',{'class':'year'}).text
        try:
          self.driver.find_element_by_xpath('//*[@id="tab-Episodes"]/a').click()
          #self.shows()
          i=1
          while True:
            try:
              self.driver.find_element_by_xpath('//*[@id="pane-Episodes"]/div/div/div/div[1]/div').click()
              st='//*[@id="pane-Episodes"]/div/div/div/div[1]/div[2]/ul/li[{}]'.format(i)
            except:
              time.sleep(2)
              self.shows(year)
              #time.sleep(2)
              #break
            try:
              self.driver.find_element_by_xpath(st).click()
              time.sleep(2)
              self.shows(year)
            except:
              break
            i+=1
        except:
          pass

          
    def tv(self):
        self.login ()
        time.sleep(5)
        self.driver.get("https://www.netflix.com/browse/genre/83?so=az")
        SCROLL_PAUSE_TIME = 1.5
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            html=self.driver.page_source
            Soup = BeautifulSoup(html,"lxml")
            soup1=Soup.findAll('a',href=re.compile("/watch"))
            for k in soup1:
              try:
                self.serial("https://www.netflix.com"+k.attrs['href'].replace('watch','title'))
              except:
                pass
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            print("..Scrolling..")
            if new_height == last_height:
                break
            last_height = new_height
        #netflix(self.driver)
    
mv = RealComp ()
if sys.argv[1]=='movie':
  mv.first_scrap()
else:
  mv.tv()