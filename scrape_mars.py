from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd     
import time

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_news():

    browser = init_browser()
        
    url="https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)
    html=browser.html
    soup=BeautifulSoup(html, "html.parser")

    content = soup.find("ul", class_="item_list")
    articles = content.find_all("li")

    title_list=[]
    text_list=[]
    for article in articles:
        news_title=article.find("div", class_="content_title").text
        title_list.append(news_title)
        news_p=article.find("div", class_="article_teaser_body").text
        text_list.append(news_p)

    latest_title=title_list[0]
    latest_news=text_list[0]

    browser.quit()

    return latest_title, latest_news


def scrape_image():
    browser = init_browser()
    url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(1)
    html=browser.html
    soup=BeautifulSoup(html, "html.parser")

    pictures=soup.find('ul', class_="articles").find_all("li")
    complete_url=[]
    for picture in pictures:
        url=picture.find('div', class_='img').find('img')['src']
        complete_url.append("https://www.jpl.nasa.gov"+url)

    featured_image_url=complete_url[0]

    browser.quit()

    return featured_image_url

def scrape_weather():

    browser = init_browser()

    url="https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    time.sleep(1)
    html=browser.html
    soup=BeautifulSoup(html, "html.parser")

    tweets = soup.find('div', class_="stream").find_all("li", class_="js-stream-item stream-item stream-item")
    record=[]
    for tweet in tweets:
        content = tweet.find('div', class_="js-tweet-text-container").find('p').text
        if content[0:7]=='InSight':
            record.append(content)

    Latest_weather=record[0]

    browser.quit()

    return Latest_weather

def scrape_fact():
    
    #####
    url="https://space-facts.com/mars/"
    table = pd.read_html(url)[0]
    fact_html=table.to_html(header=False, index=False)   

    return fact_html
    
def scrape_hemisphere():

    browser = init_browser()

    url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(1)
    html=browser.html
    soup=BeautifulSoup(html, "html.parser")

    items=soup.find_all('div', class_="item")

    hemisphere_image_urls=[]

    for item in items:
        link=item.find("a", class_="itemLink product-item").find('img')['src']
        img_url= "https://astrogeology.usgs.gov/" + link
        img_title=item.find("div", class_="description").find("a", class_="itemLink product-item").find("h3").text
        hemisphere_image_urls.append({
            "title" : img_title,
            "img_url": img_url
        })
    
    browser.quit()

    return hemisphere_image_urls

def scrape_info():

    data={}
    
    data["news_title"], data["news_p"]=scrape_news()
    data["featured_image_url"]=scrape_image()
    data["current_weather"]=scrape_weather()
    data["mars_facts"]= scrape_fact()
    data["mars_hemisphere" ]=scrape_hemisphere()   

    return data
       
   







        
  


