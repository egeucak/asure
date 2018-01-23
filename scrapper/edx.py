from bs4 import BeautifulSoup
from selenium import webdriver
import json

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
browser = webdriver.Chrome(chrome_options=options)

def getDetails(url):
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")

    print(soup.find_all(attrs={"data-field":"price"})[0].find("uppercase"))
    return 0

query = "python"
search_url = "https://www.edx.org/course?search_query={}".format(query)

browser.get(search_url)
html = browser.page_source
#print(html)
soup = BeautifulSoup(html, "html.parser")
#print(soup.find_all(class_="discovery-card course-card shadow verified")[0])

elem = soup.find_all(class_="discovery-card course-card shadow verified")[0]

title = elem.find("h3").get_text()
thumbnail = elem.find("img")["src"]
url = elem.find_all("a")[0].get("href")
source = "edx"
getDetails(url)

#print(elem.find_all("a")[0].get("href"))


#rating price summary stars