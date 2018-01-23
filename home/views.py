from django.shortcuts import render
from bs4 import BeautifulSoup
from selenium import webdriver

def coursera(link):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1200x600')
    url = "https://www.coursera.org/courses?languages=en&query=python"
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url)
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
                                          "site": "https://www.surfacedstudio.com/wordpress/wp-content/uploads/2018/01/Udemy-Icon.png"
                                          }
    browser.close()
    return dumpListDict

def index(request):


    return render(request, 'index.html', { 'dictionaries': coursera("https://www.coursera.org/courses?languages=en&query=python") })

