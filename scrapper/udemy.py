import time

from bs4 import BeautifulSoup
from selenium import webdriver

url = "http://www.udemy.com/courses/search/?q=python&src=ukw"
browser = webdriver.Chrome("/Users/oguz298/Downloads/chromedriver")
browser.get(url)
time.sleep(5)
html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')
dumpListDict = {}

dumpListNames = [x.get_text() for x in soup.findAll('h1', attrs={'':''})]
dumpListRatings = [str(x).split(">")[4].split("<")[0] for x in soup.findAll('div', attrs={'data-purpose':'search-course-card-review-count'})]
dumpListStars = [x.get_text() for x in soup.findAll('span', attrs={'data-purpose':'search-course-card-review-point'})]
dumpListSummary = [x.get_text() for x in soup.findAll('p', attrs={'data-purpose':'search-course-card-headline'})]
dumpListImageUrl = [x['src'] for x in soup.findAll('img', attrs={'alt':'course image'})]
dumpListPrice = [x.get_text() for x in soup.findAll('span', attrs={'data-purpose':'search-course-card-discount-price'})]
dumpListUrl = ["http://www.udemy.com" + x['href'] for x in soup.findAll('a', attrs={'data-purpose':'search-course-card-title'})]

for i in range(len(dumpListNames)):
    dumpListDict[dumpListNames[i]] = [dumpListNames[i], dumpListRatings[i], dumpListStars[i], dumpListImageUrl[i], dumpListSummary[i], dumpListPrice[i], dumpListUrl[i]]
browser.close()
