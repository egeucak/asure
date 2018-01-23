import time

from bs4 import BeautifulSoup
from selenium import webdriver

query = "python"

url = "https://www.khanacademy.org/search?page_search_query={}".format(query)
browser = webdriver.Chrome("C:\\Users\\Mert\\Desktop\\chromedriver.exe")
browser.get(url)
html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')
dumpListDict = {}
dumpListNames = []
dumpListSummary = []
dumpListPrice = []
dumpListUrl = []
dumpListImageUrl = []
count = 0
for i in soup.findAll(class_="gs-title"):
    str = i.get_text()
    str = str.replace(" | Khan Academy", "")
    if "(video)" in str: # it checks the
        dumpListNames.append(str)
        print(soup.findAll('div', attrs={'dir': 'ltr'})[count].get_text())
        dumpListSummary.append(soup.findAll('div', attrs={'dir': 'ltr'})[count].get_text())
        urls = soup.findAll(class_='gs-image')[count]  # image url and video url are here
        print(urls)
        dumpListPrice.append("Free") #there is no price for khan

        print(urls.findAll('a', attrs={'src': }))#image url

    count += 1

for i in range(len(dumpListNames)):
    # dumpListDict[dumpListNames[i]] = [dumpListNames[i], dumpListRatings[i], dumpListStars[i], dumpListImageUrl[i], dumpListSummary[i], dumpListPrice[i], dumpListUrl[i]]
    dumpListDict[dumpListNames[i]] = {"title": dumpListNames[i],

                                      "price": dumpListPrice[i],
                                      "url": dumpListUrl[i],
                                      "summary": dumpListSummary[i],
                                      "site": "Khan Academy"}
browser.close()
