from bs4 import BeautifulSoup
from selenium import webdriver
import string, json

class Coursera:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        self.browser = webdriver.Chrome(chrome_options=options)

    def _get_details(self, url):
        browser = self.browser
        browser.get(url)
        html = browser.page_source
        soup = BeautifulSoup(html, "html.parser")
        rating = soup.find_all(class_="ratings-text bt3-visible-xs")[0].get_text()
        rating = float(rating.split(" ")[0])*20
        rating = "{}/100".format(rating)
        summary = ":".join(soup.find_all(class_="body-1-text course-description")[0].get_text().split(":")[1:])[:197] + "..."
        price = "Free"
        temp = {"price":price, "rating":rating, "summary":summary}
        return temp

    def search(self, query):
        browser = self.browser

        url = "https://www.coursera.org/courses?languages=en&query={}".format(query)
        browser.get(url)

        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        dumpListDict = {}

        page = soup.findAll(attrs={"name":"offering_card"})

        for i in range(len(page)):
            elems = page[i]
            elem = json.loads(elems['data-click-value'])

            ##
            type = elem['offeringType']
            if type =='specialization': continue
            url = "https://www.coursera.org{}".format(elem['href'])
            details = self._get_details(url)
            price = details["price"]
            rating = details["rating"]
            summary = details["summary"]
            thumnail = elems.find_all("img")[0]["src"]
            title = elems.find("h2").get_text()
            tags = title.translate(string.punctuation).split(" ")
            dumpListDict[title] = {"title":title,
                                   "url":url,
                                   "price":price,
                                   "rating":rating,
                                   "summary":summary,
                                   "thumbnail":thumnail,
                                   "tags":tags,
                                   "source":"coursera"
                                   }
        browser.close()
        return dumpListDict