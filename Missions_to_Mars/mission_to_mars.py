#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
import os
from bs4 import BeautifulSoup as bs
from splinter import Browser
from urllib.request import urlopen as uReq
import requests
import time

def scrape():
        # In[2]:


        executable_path={'executable_path':'/usr/local/bin/chromedriver'}


        # In[3]:


        browser=Browser('chrome', **executable_path, headless=False)


        # # NASA Mars News

        # In[4]:


        news_url='https://mars.nasa.gov/news'
        browser.visit(news_url)
        #'https://mars.nasa.gov/'


        # In[5]:


        html_response = browser.html
        news_soup = bs(html_response, 'html.parser') 
        #print(soup.prettify()) 


        # In[6]:


        news = news_soup.select('.content_title')


        # In[7]:


        news_title = news_soup.find('div', class_='content_title').get_text()
        news_title


        # In[8]:


        news_detail = news_soup.find('div', class_ = 'article_teaser_body').get_text()
        news_detail


        # # JPL Mars Space Images - Featured Image

        # In[9]:


        main_url='https://www.jpl.nasa.gov'
        url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)


        # In[10]:


        #first click takes you to the next page where link to full image is
        button = browser.find_by_id("full_image").first.click()
        time.sleep(3)


        # In[11]:


        #click more_info to get to the full image page
        more_info = browser.click_link_by_partial_text('more info')


        # In[12]:


        html=browser.html

        full_size_img_soup=bs(html, "html.parser")

        images=full_size_img_soup.find_all('img', {"class":"main_image"})


        # In[13]:


        featured_image =images[0]['src']


        # In[14]:


        #print(main_url + featured_image)


        # In[15]:


        featured_image_url = main_url + featured_image


        # # Mars Weather

        # In[16]:


        tweet_url = "https://twitter.com/marswxreport?lang=en"
        browser.visit(tweet_url)


        # In[17]:


        page_html = browser.html
        page_soup = bs(page_html, "html.parser")


        # In[18]:


        tweets = page_soup.find("p",{"class":"TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"})


        # In[19]:


        mars_weather=tweets.text


        # In[20]:


        #mars_weather


        # In[21]:


        time_stamp = page_soup.find_all("a",{"class":"tweet-timestamp"})
        time_stamp[0].text


        # # Mars Facts

        # In[22]:


        import pandas as pd


        # In[23]:


        facts_url='https://space-facts.com/mars/'
        browser.visit(facts_url)


        # In[24]:


        temp_html = browser.html


        # In[25]:


        facts_soup = bs(temp_html, "html.parser")


        # In[26]:


        facts = facts_soup.find('table', attrs={'class':'tablepress tablepress-id-p-mars'})


        # In[27]:


        #facts


        # In[28]:


        table_data=[]
        rows = facts.find_all('tr')
        for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                table_data.append([ele for ele in cols if ele]) # Get ri


        # In[29]:


        table_data


        # In[30]:


        mars_df = pd.DataFrame(table_data)


        # In[31]:


        mars_facts_table = mars_df.to_html()

        #strip unwanted newlines to clean up the table
        mars_facts = mars_facts_table.replace('\n', '')
        #mars_facts
        # In[32]:

        #save the table directly to a file
        mars_df.to_html('MarsFacts.html')
        # # Mars Hemispheres

        # In[33]:
        main_url = 'https://astrogeology.usgs.gov/'
        hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemisphere_url)
        time.sleep(5)

        # In[34]:
        temp_html = browser.html

        # In[35]:

        hemis_soup = bs(temp_html, "html.parser")
        hemis_link = hemis_soup.findAll('div', class_='item')
        hemis_link[0]
        # In[36]:
        #name of the hemisphere
        hemis_link[0].h3.text
        # In[37]:

        #link to image for the hemisphere
        hemis_link[0].a.get('href')

        # In[38]:
        dlist = []
        for data in hemis_link:
                d={}
                d['title']=data.h3.text
                temp_url=main_url+data.a.get('href')
                response = requests.get(temp_url)
                soup = bs(response.content)
                full_img_url = soup.find('img', class_ = 'wide-image')
                
                d['img_url'] = main_url+full_img_url.get('src')
                
                dlist.append(d)

        #dlist

        scrape_data = {"NewsTitle": news_title,
        "NewsParagraph": news_detail,
        "FeaturedImageURL": featured_image_url,
        "MarsWeather": mars_weather,
        "MarsFacts": mars_facts, 
        "MarsHemispheres": dlist    
        }

        return scrape_data
        browser.quit()
#print(scrape())