import time

from bs4 import BeautifulSoup
from selenium import webdriver

class Udemy:
    def search(self, query):
        url = "http://www.udemy.com/courses/search/?q={}&src=ukw".format(query)
        options = webdriver.ChromeOptions()
        options.add_argument('window-size=5x5')


        browser = webdriver.Chrome(chrome_options=options)
        browser.get(url)
        time.sleep(2)
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
        for star in range(len(dumpListStars)):
            dumpListStars[star] = "{}/100".format(float(dumpListStars[star])*20)
        print(dumpListStars)
        for i in range(len(dumpListNames)):
            #dumpListDict[dumpListNames[i]] = [dumpListNames[i], dumpListRatings[i], dumpListStars[i], dumpListImageUrl[i], dumpListSummary[i], dumpListPrice[i], dumpListUrl[i]]
            dumpListDict[dumpListNames[i]] = {"title":dumpListNames[i],
                                              #"rating":dumpListRatings[i],
                                              "thumbnail":dumpListImageUrl[i],
                                              "price":dumpListPrice[i],
                                              "url":dumpListUrl[i],
                                              "summary":dumpListSummary[i],
                                              "rating":dumpListStars[i],
                                              "site":"udemy",
                                              "site_logo":"https://about.udemy.com/wp-content/uploads/2017/10/NewUlogo-large-1.png"
                                              }
        return dumpListDict