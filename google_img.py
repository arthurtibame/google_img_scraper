from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

import sys
import json
import os
import argparse

import requests
import urllib
import urllib3
from urllib3.exceptions import InsecureRequestWarning

import datetime
import time

urllib3.disable_warnings(InsecureRequestWarning)

searchword1 = ''
#searchword2 = 'dog'
#searchword3 = 'cartoon'
#searchurl = 'https://www.google.com/search?q=' + searchword1 + '+' + searchword2 + '+' + searchword3 + '&source=lnms&tbm=isch'
searchurl = 'https://www.google.com/search?q=' + searchword1 + '+' + '&source=lnms&tbm=isch'
basde_dir = r'downloads'
 
dirs = f'./{basde_dir}/{searchword1}' 

maxcount = 10000

chromedriver = r'./chromedriver.exe'

if not os.path.exists(dirs):
    os.mkdir(dirs)

def download_google_staticimages(keyworkds_counter):

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    #options.add_argument('--headless')

    try:
        browser = webdriver.Chrome(options=options)
    except Exception as e:
        print(f'No found chromedriver in this environment.')
        print(f'Install on your machine. exception: {e}')
        sys.exit()

    browser.set_window_size(1280, 1024)
    browser.get(searchurl)
    time.sleep(1)

    print(f'Getting you a lot of images. This may take a few moments...')

    element = browser.find_element_by_tag_name('body')

    # Scroll down
    #for i in range(30):
    for i in range(50):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)

    try:
        browser.find_element_by_id('smb').click()
        for i in range(50):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)
    except:
        for i in range(10):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)

    print(f'Reached end of page.')
    time.sleep(0.5)
    print(f'Retry')
    time.sleep(0.5)

    # Below is in japanese "show more result" sentences. Change this word to your lanaguage if you require.
    browser.find_element_by_xpath('//input[@value="顯示更多結果"]').click()

    # Scroll down 2
    for i in range(50):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)

    try:
        browser.find_element_by_id('smb').click()
        for i in range(50):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)
    except:
        for i in range(10):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)

    #elements = browser.find_elements_by_xpath('//div[@id="islrg"]')
    #page_source = elements[0].get_attribute('innerHTML')
    page_source = browser.page_source 

    soup = BeautifulSoup(page_source, 'lxml')
    images = soup.find_all('img')

    urls = []
    for image in images:
        try:
            url = image['data-src']
            if not url.find('https://'):
                urls.append(url)
        except:
            try:
                url = image['src']
                if not url.find('https://'):
                    urls.append(image['src'])
            except Exception as e:
                print(f'No found image sources.')
                print(e)

    count = 0
    if urls:
        for url in urls:
            try:
                res = requests.get(url, verify=False, stream=True)
                rawdata = res.raw.read()
                with open(os.path.join(dirs, 'img_' + str(keyworkds_counter) +str(count) + '.jpg'), 'wb') as f:
                    f.write(rawdata)
                    count += 1
            except Exception as e:
                print('Failed to write rawdata.')
                print(e)

    browser.close()
    return count

# Main block
def main():
    global searchword1, searchurl, dirs, maxcount
    t0 = time.time()
    import pandas as pd
    # read your keywords
    df = pd.read_csv(r'./food_eng_final.csv', encoding='big5')
    keywords_list = df.iloc[:,0].tolist()
    keyworkds_counter = 0
    for searchword1 in keywords_list: 
    
        searchurl = 'https://www.google.com/search?q=' + str(searchword1) + '+' + '&source=lnms&tbm=isch'
        basde_dir = r'downloads'
        
        dirs = f'./{basde_dir}/{searchword1}' 

        maxcount = 10000
        if not os.path.exists(dirs):
            os.mkdir(dirs)


        count = download_google_staticimages(keyworkds_counter)
        t1 = time.time()

        total_time = t1 - t0
        print(f'\n')
        print(f'Download completed. [Successful count = {count}].')
        print(f'Total time is {str(total_time)} seconds.')
        keyworkds_counter+=1

if __name__ == '__main__':
    main()