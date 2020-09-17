# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    martian_dict ={}

    # Mars News URL of page to be scraped
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    # Retrieve the latest news title and paragraph
    news_title = news_soup.find_all('div', class_='content_title')[0].text
    news = news_soup.find_all('div', class_='article_teaser_body')[0].text

    # Mars Image to be scraped
    jpl_url = 'https://www.jpl.nasa.gov'
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')
    # Retrieve featured image link
    relative_image_path = image_soup.find_all('img')[3]["src"]
    featured_image = jpl_url + relative_image_path

    # Mars facts to be scraped, converted into html table
    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    mars_facts = tables[2]
    mars_facts.columns = ["Description", "Value"]
    mars_html_tbl = mars_facts.to_html()
    mars_html_tbl.replace('\n', '')
    
    # Mars hemisphere name and image to be scraped
    usgs_url = 'https://astrogeology.usgs.gov'
    hemis_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemis_url)
    hemis_html = browser.html
    hemis_soup = BeautifulSoup(hemis_html, 'html.parser')
    # Mars hemispheres products data
    all_martian_hemis = hemis_soup.find('div', class_='collapsible results')
    martian_hemis = all_martian_hemis.find_all('div', class_='item')
    hemis_image_urls = []
    # Iterate through each hemisphere data
    for i in mars_hemis:
        # Collect Title
        hemis = i.find('div', class_="description")
        title = hemis.h3.text        
        # Collect image link by browsing to hemisphere page
        hemis_link = hemis.a["href"]    
        browser.visit(usgs_url + hemis_link)        
        image_html = browser.html
        image_soup = BeautifulSoup(image_html, 'html.parser')        
        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']
        # Create Dictionary to store title and url info
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = image_url        
        hemis_image_urls.append(image_dict)

    # Mars 
    martian_dict = {
        "news_title": news_title,
        "news": news,
        "featured_image_url": featured_image,
        "fact_table": str(mars_html_tbl),
        "hemisphere_images": hemis_image_urls
    }

    return martian_dict
