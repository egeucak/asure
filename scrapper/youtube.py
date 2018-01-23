from bs4 import BeautifulSoup
from selenium import webdriver
import time, re

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1200x600')
url = "https://www.youtube.com/results?search_query=python"
browser = webdriver.Chrome(chrome_options=options)
browser.get(url)
html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')
dumpListDict = {}

dumpListNames = [x.get_text().strip() for x in soup.findAll('span', attrs={'class':'style-scope ytd-playlist-renderer'})]


dumpListUrl = ["https://www.youtube.com" + x['href'] for x in soup.findAll('a', attrs={'class':'yt-simple-endpoint style-scope ytd-playlist-renderer'})]

dumpListLike = []
dumpListDislike = []
dumpListPercentage = []
dumpListDescriptionList = []
dumpListThumbnailList = [x for x in soup.findAll('yt-img-shadow', attrs={'class':'style-scope ytd-playlist-video-thumbnail-renderer no-transition'})]
print(dumpListThumbnailList[0]['yt-img-shadow']['img'])

for i in dumpListUrl:
    browser.get(i)
    time.sleep(2)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    temp = ""
    dumpListLikeDislike = [x.get_text().replace(u'\xa0', u'') for x in
                           soup.findAll('yt-formatted-string', attrs={'id': 'text'})]
    dumpListDescriptionDummy = [x.get_text().strip().split("\n") for x in
                           soup.findAll('div', attrs={'class': 'style-scope ytd-expander'})][0]
    for j in dumpListDescriptionDummy:
        temp = temp + j + " "
    dumpListDescriptionList.append(temp)

    if(len(dumpListLikeDislike)==5):
        dumpListLike.append(re.findall('\d+', dumpListLikeDislike[1])[0])
        if("B" in dumpListLikeDislike[1]):
            dumpListLike[-1] = str(int(dumpListLike[-1]) * 1000)
        dumpListDislike.append(re.findall('\d+', dumpListLikeDislike[2])[0])
        if ("B" in dumpListLikeDislike[2]):
            dumpListDislike[-1] = str(int(dumpListDislike[-1]) * 1000)
    else:
        dumpListLike.append(re.findall('\d+', dumpListLikeDislike[2])[0])
        if ("B" in dumpListLikeDislike[2]):
            dumpListLike[-1] = str(int(dumpListLike[-1]) * 1000)
        dumpListDislike.append(re.findall('\d+', dumpListLikeDislike[3])[0])
        if ("B" in dumpListLikeDislike[3]):
            dumpListDislike[-1] = str(int(dumpListDislike[-1]) * 1000)

for i in range(len(dumpListLike)):
    dumpListPercentage.append(str(100*(int(dumpListLike[i]) / (int(dumpListLike[i]) + int(dumpListDislike[i])))))



for i in range(len(dumpListNames)):
    dumpListDict[dumpListNames[i]] = {"name":dumpListNames[i],
                                      "percentage":dumpListPercentage[i],
                                      "likes":dumpListLike[i],
                                      "dislikes":dumpListDislike[i],
                                      "link":dumpListUrl[i],
                                      "description":dumpListDescriptionList[i][:200],
                                      "site":"youtube"
                                      }
print(dumpListDict)
browser.close()
