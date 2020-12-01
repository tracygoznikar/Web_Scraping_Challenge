from bs4 import BeautifulSoup
import requests
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import time

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    ##NASA Mars News website
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    time.sleep(1)


#soupify page
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # title text
    new_soup=soup.select_one('ul.item_list li.slide')
    title = new_soup.find('div', class_='content_title')
    title = title.text
    title

    # paragraph 
    description = new_soup.find('div', class_='article_teaser_body')
    description = description.text
    description

    #image
    url_pic = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_pic)

    browser.links.find_by_partial_text('FULL IMAGE').click()
    browser.links.find_by_partial_text('more info').click()

    html = browser.html
    soup1 = BeautifulSoup(html, 'html.parser')

    image = soup1.select_one('figure.lede a img').get('src')
    image
    featured_image_url = f'https://www.jpl.nasa.gov/{image}'
    featured_image_url



    url_facts = 'https://space-facts.com/mars/'
    tables = pd.read_html(url_facts)
    
    df = tables[0]
    facts_df = df.rename(columns={0: "Description", 1: "Mars"})
    facts_df.set_index("Description", inplace = True)
    
    html_table = facts_df.to_html()
    html_table


    browser = init_browser()
    url_hemi ='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemi)
    html = browser.html

    soup2 = BeautifulSoup(html,'html.parser')
    quotes = soup2.find_all('div',class_='item')
    
    hemisphere_image_urls=[]
    
    for quote in quotes:
        t = quote.find('h3').text
        a = quote.a['href']
        a=a.replace('search/map','download')
        dic={}
        dic['title']=t
        dic['img_url']= "https://astropedia.astrogeology.usgs.gov"+a+'.tif/full.jpg'
        hemisphere_image_urls.append(dic)
        hemisphere_image_urls
        
        #cerberus_img = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'
        #schiaparelli_img = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'
        #syrtis_img = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'
        #valles_img = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'

    mars_data = { 
    "title":title, "description":description,
    "featured_image_url":featured_image_url,
    "html_table":html_table,
    "hemisphere_image_urls":hemisphere_image_urls
    #"cerberus_img":cerberus_img
    #"schiaparelli_img":schiaparelli_img
    }


    browser.quit()

    return mars_data    