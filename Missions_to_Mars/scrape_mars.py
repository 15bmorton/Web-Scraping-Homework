from bs4 import BeautifulSoup
import pandas as pd
import requests
import csv
import os
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
from flask import Flask, render_template
from pprint import pprint

def init_browser():
    executable_path = {'executable_path': "chromedriver.exe"}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    browser=init_browser()
    mars_dict= {}

    url = 'https://redplanetscience.com/#'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find_all('div', class_='content_title')[0].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text
    n_t = "HiRISE Views NASA's InSight and Curiosity on Mars"
    n_p = "New images taken from space offer the clearest orbital glimpse yet of InSight as well as a view of Curiosity rolling along."


    jpl_url2 = 'https://spaceimages-mars.com/'
    browser.visit(jpl_url2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image= soup.find_all('img')[2]
    image_url = (image.get("src"))
    featured_image_url = jpl_url2 + image_url



    facts_url = 'https://galaxyfacts-mars.com'
    tables = pd.read_html(facts_url)
    tables
    type(tables)
    tables[0]
    tables[1]
    tables_df = pd.merge(tables[0], tables[1], how= 'outer')
    edited_df = tables_df.drop(columns=2)
    mars_df = edited_df.drop([0,9,10,11,12,13], axis=0)
    mars_final_df = mars_df.rename(columns= {0: "Fact"})
    Mars_df = mars_final_df.rename(columns= {1: "Mars"})
    html_table = Mars_df.to_html()
    html_table.replace('\n', '')
    Mars_df.to_html('Mars_table.html')



    hemi_url = 'https://marshemispheres.com/'
    browser.visit(hemi_url)
    html= browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image_hems= soup.find_all('div', class_="item")
    image_hems
    hemisphere_image_urls = []

    for image in image_hems:
        try:
            hem= image.find('div', class_="description")
            title= hem.h3.text
            hem_url= hem.a['href']
            browser.visit(hemi_url + hem_url)
            html=browser.html
            soup= BeautifulSoup(html, 'html.parser')
            image_src= soup.find('li').a['href']
            if (title and image_src):
                print('-'*50)
                print(title)
                print(image_src)
            hem_dict= {
                'Title': title,
                'Image_url': image_src
            }
            hemisphere_image_urls.append(hem_dict)
        except Exception as e:
            print(e)
    

    mars_dict={
    "News_Title":news_title,
    "News_P":news_p,
    "Featured_Image_Url":featured_image_url,
    "HTML_Table":html_table,
    "Hemisphere_Images":hemisphere_image_urls
    }

    browser.quit()
    return mars_dict
    

