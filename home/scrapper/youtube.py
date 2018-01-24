from bs4 import BeautifulSoup
from selenium import webdriver
import time, re

class Youtube:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        self.browser = webdriver.Chrome(chrome_options=options)

    def search(self, query):
        browser = self.browser
        site_logo = "https://www.youtube.com/yt/about/media/images/brand-resources/icons/YouTube-icon-our_icon.png"
        url = "https://www.youtube.com/results?search_query={}".format(query)
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
        dumpListThumbnailList = [x.find('img')['src'] for x in soup.findAll('yt-img-shadow', attrs={'class':'style-scope ytd-playlist-video-thumbnail-renderer no-transition'})]

        for i in dumpListNames:
            try:
                a = dumpListThumbnailList[i]
            except:
                dumpListThumbnailList.append(site_logo)


        for i in dumpListUrl:
            browser.get(i)
            time.sleep(4)
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
            dumpListPercentage.append(str(int(100*(int(dumpListLike[i]) / (int(dumpListLike[i]) + int(dumpListDislike[i]))))) + "/100")



        for i in range(len(dumpListNames)):
            dumpListDict[dumpListNames[i]] = {"title":dumpListNames[i],
                                              "rating":dumpListPercentage[i],
                                              "likes":dumpListLike[i],
                                              "dislikes":dumpListDislike[i],
                                              "url":dumpListUrl[i],
                                              "summary":dumpListDescriptionList[i][:197]+"...",
                                              "thumbnail":dumpListThumbnailList[i],
                                              "source":"youtube",
                                              "price":"Free",
                                              "site_logo":"https://www.youtube.com/yt/about/media/images/brand-resources/icons/YouTube-icon-our_icon.png"
                                              }
        return dumpListDict
