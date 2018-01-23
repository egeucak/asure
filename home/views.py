from django.shortcuts import render
from bs4 import BeautifulSoup
from selenium import webdriver
import random,string

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1200x600')
browser = webdriver.Chrome(chrome_options=options)

def coursera(link):
    browser.get(link)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    dumpListDict = {}

    dumpListNames = [x.get_text(separator='\t').split("\t")[0] for x in
                     soup.findAll('a', attrs={'name': 'offering_card'})]
    dumpListImageUrl = [x['src'] for x in soup.findAll('img', attrs={'class': 'offering-image'})]
    dumpListUrl = ["http://www.coursera.org" + x['href'] for x in
                   soup.findAll('a', attrs={'data-click-key': 'catalog.search.click.offering_card'})]

    for i in range(len(dumpListNames)):
        dumpListDict[dumpListNames[i]] = {"title": dumpListNames[i],
                                          "url": dumpListUrl[i],
                                          "thumbnail": dumpListImageUrl[i],
                                          "site_logo": "http://www.pvhc.net/img102/wimqmhowtqjoqdifgnlc.jpg",
                                          "site": "coursera"
                                          }


    return dumpListDict

def edx(query):
    def getDetails(url):
        browser.get(url)
        html = browser.page_source
        soup = BeautifulSoup(html, "html.parser")

        a = soup.find_all(attrs={"data-field": "price"})[0].find_all('span', attrs={"class": "uppercase"})[0].get_text()
        price = a

        summary = soup.find_all(attrs={"class": "course-description"})[0].get_text().strip()[:197] + "..."
        # stars
        rating = random.randrange(80, 95)
        # print(summary)
        # print(soup.find_all(attrs={"class":"course-description"})[0].get_text().strip())

        temp = {"price": price,
                "summary": summary,
                "rating": rating}
        return temp

    search_url = "https://www.edx.org/course?search_query={}".format(query)

    browser.get(search_url)
    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")
    # print(soup)
    # print(soup.find_all(class_="discovery-card course-card shadow verified")[0])

    elems = soup.find_all(class_="discovery-card course-card shadow verified")
    dumpListDict = {}
    for elem in elems:
        title = elem.find("h3").get_text()
        thumbnail = elem.find("img")["src"]
        url = elem.find_all("a")[0].get("href")
        source = "edx"
        temp = getDetails(url)

        price = temp["price"]
        summary = temp["summary"]
        rating = temp["rating"]
        tags = title.translate(string.punctuation).split(" ")
        dumpListDict[title] = {"title": title,
                               "url": url,
                               "price": price,
                               "rating": rating,
                               "summary": summary,
                               "thumbnail": thumbnail,
                               "tags": tags,
                               "source": source
                               }
    return dumpListDict

def index(request):
    z = {**coursera("https://www.coursera.org/courses?languages=en&query=python"), **edx("python")}
    return render(request, 'index.html', { 'dictionaries':  z  })


