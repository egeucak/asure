from bs4 import BeautifulSoup
from selenium import webdriver
import json
import string
import os, time
import signal


dumpListDict = {}
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
browser = webdriver.Chrome(chrome_options=options)

def get_details(url):
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


query = "python"
url = "https://www.coursera.org/courses?languages=en&query={}".format(query)
browser.get(url)

html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')
dumpListDict = {}

page = soup.findAll(attrs={"name":"offering_card"})

num = len(page)
parent_pid=os.getpid()
for i in range(len(page)):
    pid = os.fork()
    num = num - 1
    if (pid==0):
        break
    if (num-1==i): os.kill(os.getpid(), signal.SIGKILL)
if (os.getpid == 0): os.kill(os.getpid(), signal.SIGKILL)

print(num)
#time.sleep(20)

try:
    for elems in page[20]:
        global dumpListDict
        elem = json.loads(elems['data-click-value'])
        type = elems['offeringType']
        if type =='specialization': continue
        url = "https://www.coursera.org{}".format(elems['href'])
        details = get_details(url)
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
        #print(dumpListDict)
        if (os.getpid() != parent_pid): os.kill(os.getpid(), signal.SIGKILL)
except Exception as e:
    os.kill(os.getpid(), signal.SIGKILL)
    print(e)

time.sleep(5)
print(dumpListDict)


'''dumpListNames = [x.get_text(separator='\t').split("\t")[0] for x in soup.findAll('a', attrs={'name':'offering_card'})]
dumpListImageUrl = [x['src'] for x in soup.findAll('img', attrs={'class':'offering-image'})]
dumpListUrl = ["http://www.coursera.org" + x['href'] for x in soup.findAll('a', attrs={'data-click-key':'catalog.search.click.offering_card'})]


for i in range(len(dumpListNames)):
    dumpListDict[dumpListNames[i]] = [dumpListNames[i], dumpListImageUrl[i], dumpListUrl[i]]
print(dumpListDict)
'''
#browser.close()
