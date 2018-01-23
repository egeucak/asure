from bs4 import BeautifulSoup
from selenium import webdriver
from multiprocessing import Pipe, Process
import json
import string
import os, time
from multiprocessing.dummy import Pool as ThreadPool


pid = 0
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
browser = webdriver.Chrome(chrome_options=options)
dumpListDict = {}


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

def work(i, page):
    elems = page[i]
    elem = json.loads(elems['data-click-value'])
    print("in work ->>",i)
    ##
    type = elem['offeringType']
    if type =='specialization': return
    url = "https://www.coursera.org{}".format(elem['href'])
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
    print("in work ->",i)
    print("dumplist -> ",dumpListDict)

# def fork(size, page):
#     processes = {}
#     if __name__ == '__main__':
#         for i in range(size):
#             parent_conn, child_conn = Pipe()
#             p = Process(target=work, args=(child_conn, i, page,))
#             processes[i] = {"child_conn": child_conn, "parent_conn": parent_conn, "process": p}
#
#             p.start()
#             print("started process ->> ",i)
#
#         for i in range(size):
#             print("recieve data ->>",i)
#             print(processes[i]["parent_conn"].recv())  # prints "[42, None, 'hello']"
#             print(" arrived ! ->> ",i)
#             processes[i]["process"].join()

def scrape(section):
    try:
        print("a")
        global dumpListDict
        elems = section
        elem = json.loads(elems['data-click-value'])
        type = elem['offeringType']
        if type =='specialization': return
        url = "https://www.coursera.org{}".format(elem['href'])
        details = get_details(url)
        price = details["price"]
        rating = details["rating"]
        summary = details["summary"]
        thumbnail = elems.find_all("img")[0]["src"]
        title = elems.find("h2").get_text()
        tags = title.translate(string.punctuation).split(" ")
        dumpListDict[title] = {"title":title,
                           "url":url,
                           "price":price,
                           "rating":rating,
                           "summary":summary,
                           "thumbnail":thumbnail,
                           "tags":tags,
                           "source":"coursera"
                           }
    except:
        i = 0

query = "python"
url = "https://www.coursera.org/courses?languages=en&query={}".format(query)
browser.get(url)

html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')
#dumpListDict = {}

page = soup.findAll(attrs={"name":"offering_card"})
#print(page)
num = len(page)
start = time.time()
print("STARTED !!!! ")

pool = ThreadPool(num)
pool.map(scrape, page)
pool.close()
pool.join()
#fork(2, page)
print(dumpListDict)
print(time.time()-start)





#fork()
'''if(pid!=0):
    os.waitpid(0, 0)

else:
    #os.kill(os.getpid(), signal.SIGTERM)
    exit()'''

#
# try:
#     for elems in page[20]:
#         global dumpListDict
#         elem = json.loads(elems['data-click-value'])
#         type = elems['offeringType']
#         if type =='specialization': continue
#         url = "https://www.coursera.org{}".format(elems['href'])
#         details = get_details(url)
#         price = details["price"]
#         rating = details["rating"]
#         summary = details["summary"]
#         thumnail = elems.find_all("img")[0]["src"]
#         title = elems.find("h2").get_text()
#         tags = title.translate(string.punctuation).split(" ")
#         dumpListDict[title] = {"title":title,
#                                "url":url,
#                                "price":price,
#                                "rating":rating,
#                                "summary":summary,
#                                "thumbnail":thumnail,
#                                "tags":tags,
#                                "source":"coursera"
#         }
#         #print(dumpListDict)
#         # if (os.getpid() != parent_pid): os.kill(os.getpid(), signal.SIGKILL)
# except Exception as e:
#     os.kill(os.getpid(), signal.SIGKILL)
#     print(e)

#time.sleep(5)
#print(dumpListDict)


'''dumpListNames = [x.get_text(separator='\t').split("\t")[0] for x in soup.findAll('a', attrs={'name':'offering_card'})]
dumpListImageUrl = [x['src'] for x in soup.findAll('img', attrs={'class':'offering-image'})]
dumpListUrl = ["http://www.coursera.org" + x['href'] for x in soup.findAll('a', attrs={'data-click-key':'catalog.search.click.offering_card'})]


for i in range(len(dumpListNames)):
    dumpListDict[dumpListNames[i]] = [dumpListNames[i], dumpListImageUrl[i], dumpListUrl[i]]
print(dumpListDict)
'''
#browser.close()
