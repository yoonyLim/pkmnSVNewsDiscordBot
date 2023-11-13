import os
from datetime import date

from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium import webdriver

load_dotenv(verbose = True)

# use selenium chrome webdriver without opening the browser
op = webdriver.ChromeOptions()
op.add_argument('headless') # to reduce received data size
driver = webdriver.Chrome(options = op)
driver.get(os.getenv("ADDRESS") + "/list") # fetch from the web page

def fetchPage():
    driver.refresh() # refresh to get the latest news
    html_txt = driver.page_source
    soup = BeautifulSoup(html_txt, 'lxml')

    # find news that came out today
    anchors = soup.find_all('a')

    return anchors

def getTodayNews():
    anchors = fetchPage()
    today = date.today().strftime("%Y.%m.%d.")

    isTdoayNews = False
    indexes = []
    newsArray = []

    for anchor in anchors:
        tgt  = anchor.find("div", {"class": "date-text"})

        if tgt.text.replace(" ", "") == today:
            isTdoayNews = True
            indexes.append(anchors.index(anchor))

    if isTdoayNews:
        # store news title, img, and link to send out
        for index in indexes:
            newsTitle = anchors[index].find("div", {"class": "title-content"}).text
            newsImgUrl = os.getenv("ADDRESS") + '/' + anchors[index].find("img")["src"]
            newsLink = os.getenv("ADDRESS") + '/' + anchors[index]["href"]

            newsArray.append([newsTitle, newsImgUrl, newsLink])

        isTdoayNews = False

        return newsArray
    else: 
        return 0

def getPrevNews():
    anchors = fetchPage()
    newsArray = []

    for anchor in anchors:
        newsTitle = anchor.find("div", {"class": "title-content"}).text
        newsImgUrl = os.getenv("ADDRESS") + '/' + anchor.find("img")["src"]
        newsLink = os.getenv("ADDRESS") + '/' + anchor["href"]
        newsDate = anchor.find("div", {"class": "date-text"}).text

        newsArray.append([newsTitle, newsImgUrl, newsLink, newsDate])

    return newsArray