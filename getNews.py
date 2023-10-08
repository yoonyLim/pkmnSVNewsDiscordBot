import os
from datetime import date

from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium import webdriver

load_dotenv(verbose = True)

# use selenium chrome webdriver without opening the browser
op = webdriver.ChromeOptions()
op.add_argument('headless')

# get raid events
driver = webdriver.Chrome(options = op)
driver.get(os.getenv("ADDRESS") + "/list")
html_txt = driver.page_source
soup = BeautifulSoup(html_txt, 'lxml')

# find news that came out today
anchors = soup.find_all('a')

def getTodayNews():
    today = date.today().strftime("%Y. %m. %d.")

    isTdoayNews = False
    index = 0

    for anchor in anchors:
        tgt  = anchor.find("div", {"class": "date-text"})

        if tgt.text == today:
            isTdoayNews = True
            index = anchors.index(anchor)

    if isTdoayNews:
        # store news title, img, and link to send out
        newsTitle = anchors[index].find("div", {"class": "title-content"}).text
        newsImgUrl = os.getenv("ADDRESS") + '/' + anchors[index].find("img")["src"]
        newsLink = os.getenv("ADDRESS") + '/' + anchors[index]["href"]

        isTdoayNews = False

        return [newsTitle, newsImgUrl, newsLink]
    else: 
        return 0

def getPrevNews():
    allNews = []

    for anchor in anchors:
        newsTitle = anchor.find("div", {"class": "title-content"}).text
        newsImgUrl = os.getenv("ADDRESS") + '/' + anchor.find("img")["src"]
        newsLink = os.getenv("ADDRESS") + '/' + anchor["href"]
        newsDate = anchor.find("div", {"class": "date-text"}).text

        allNews.append([newsTitle, newsImgUrl, newsLink, newsDate])

    return allNews