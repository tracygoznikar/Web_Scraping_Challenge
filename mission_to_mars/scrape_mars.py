from bs4 import BeautifulSoup
import requests
import Pandas as pd
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
    url_two = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_two)

    browser.links.find_by_partial_text('FULL IMAGE').click()

    browser.links.find_by_partial_text('more info').click()

    html = browser.html
    soup1 = BeautifulSoup(html, 'html.parser')

    #Get the link to featured image [image=new soup]
    image = soup1.select_one('figure.lede a img').get('src')
    image
    featured_image_url = f'https://www.jpl.nasa.gov/{image}'
    featured_image_url

    url_three = 'https://space-facts.com/mars/'

    #Get tables using pandas
    tables = pd.read_html(url_three)
    #tables

    df = tables[0]
    #df.head(10)

    facts_df = df.rename(columns={0: "Description", 1: "Mars"})
    #facts_df

    facts_df.set_index("Description", inplace = True)
    
    html_table = facts_df.to_html()


    #hemispheres

    final_data = { 
    "title":title, "description":description,
    "featured_image_url":featured_image_url,
    "html_table":html_table}


    browser.quit()

    return final_data    