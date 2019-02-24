from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
from splinter.exceptions import ElementDoesNotExist
import time

def init_browser():

    from splinter import Browser
    # actual path to the chromedriver
    executable_path = {'executable_path': 'C:/chromedriver'}
    #browser = Browser("chrome", executable_path="chromedriver", headless=True)
    browser = Browser('chrome', **executable_path)
    return Browser

def scrape():
    browser = init_browser()
    # Visit visitcostarica.herokuapp.com

    executable_path = {'executable_path': 'C:/chromedriver'}
    browser = Browser('chrome', **executable_path)
    url = "https://mars.nasa.gov/news"    
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    newspage = browser.html

    #Initializing the marsData dictionary to store all the Mars Info
    marsData = {}

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(newspage, 'html.parser')

    # Retrieve the latest element that contains news title and news_paragraph
    newsTitle = soup.find('div', class_='content_title').find('a').text
    newsPara = soup.find('div', class_='article_teaser_body').text

    marsData["newsTitle"]= newsTitle
    marsData["newsPara"]= newsPara

    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(featured_image_url)
    htmlImg = browser.html
    #parse
    soup = bs(htmlImg, 'html.parser')

    #image url to the full size .jpg image.
    imgUrl  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    #soup.find_all('article', style_ ='background-image')
    # Website Url
    jplurl = 'https://www.jpl.nasa.gov'

    # Concatenate website url with scrapped route
    completeUrl = jplurl + imgUrl

    # add to Dict
    marsData ["featuredImage"] = completeUrl

    #  Mars Weather Twitter via Splinter
    marsWeatherUrl = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(marsWeatherUrl)
    marsWeatherUrlhtml = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(marsWeatherUrlhtml, 'html.parser')

    #Retrieve latest tweeets
    latestTweets = soup.find_all('div', class_ ='js-tweet-text-container')

    for tweet in latestTweets:
        mars_weather = tweet.find('p').text
        if 'sol' and 'pressure' in mars_weather:
            print(mars_weather)
            break
        else:
            pass
    # add to Dict
    marsData["weatherTweets"]=mars_weather

    # Mars facts url
    marsfactsurl = 'https://space-facts.com/mars/'

    # Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    factsofMars = pd.read_html(marsfactsurl)
    marsfactsdf = factsofMars[0]
    marsfactsdf.columns = ['Attributes','Value']
    #marsfactsdf.set_index('Attributes',inplace=True)
    marsfactsdf.to_html()
    marsfactDict = marsfactsdf.to_dict(orient='records')
    # add to Dict
    marsData["marsFacts"]= marsfactDict

    # Close the browser after scraping
    browser.quit()

    # Return results
    return marsData







