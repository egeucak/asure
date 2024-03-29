from bs4 import BeautifulSoup
from selenium import webdriver
import json
import random, string

class Edx:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        self.browser = webdriver.Chrome(chrome_options=options)

    def _getDetails(self, url):
        browser = self.browser
        browser.get(url)
        html = browser.page_source
        soup = BeautifulSoup(html, "html.parser")

        a = soup.find_all(attrs={"data-field": "price"})[0].find_all('span', attrs={"class":"uppercase"})[0].get_text()
        price = a

        summary = soup.find_all(attrs={"class":"course-description"})[0].get_text().strip()[:197] + "..."
        #stars
        rating = random.randrange(80,95)
        #print(summary)
        #print(soup.find_all(attrs={"class":"course-description"})[0].get_text().strip())

        temp = {"price":price,
                "summary":summary,
                "rating":rating}
        return temp

    def search(self, query):
        browser = self.browser
        query = "python"
        search_url = "https://www.edx.org/course?search_query={}".format(query)

        browser.get(search_url)
        html = browser.page_source
        soup = BeautifulSoup(html, "html.parser")
        #print(soup)
        #print(soup.find_all(class_="discovery-card course-card shadow verified")[0])

        elems = soup.find_all(class_="discovery-card course-card shadow verified")
        dumpListDict = {}
        for elem in elems:
            try:
                title = elem.find("h3").get_text()
                thumbnail = elem.find("img")["src"]
                url = elem.find_all("a")[0].get("href")
                source = "edx"
                temp = self._getDetails(url)

                price = temp["price"]
                summary = temp["summary"]
                rating = "{}/100".format(temp["rating"])
                tags = title.translate(string.punctuation).split(" ")
                dumpListDict[title] = {"title": title,
                                       "url": url,
                                       "price": price,
                                       "rating": rating,
                                       "summary": summary,
                                       "thumbnail": thumbnail,
                                       "tags": tags,
                                       "source": source,
                                       "site_logo":"https://www.edx.org/sites/default/files/mediakit/image/thumb/edx_logo_200x200.png"
                                       }
            except Exception as e:
                print(e)
        return dumpListDict