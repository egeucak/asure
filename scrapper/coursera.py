from bs4 import BeautifulSoup
from selenium import webdriver


options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1200x600')
url = "https://www.coursera.org/courses?languages=en&query=python"
browser = webdriver.Chrome("/Users/oguz298/Downloads/chromedriver",chrome_options=options)
browser.get(url)
html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')
dumpListDict = {}

dumpListNames = [x.get_text(separator='\t').split("\t")[0] for x in soup.findAll('a', attrs={'name':'offering_card'})]
dumpListImageUrl = [x['src'] for x in soup.findAll('img', attrs={'class':'offering-image'})]
dumpListUrl = ["http://www.coursera.org" + x['href'] for x in soup.findAll('a', attrs={'data-click-key':'catalog.search.click.offering_card'})]


for i in range(len(dumpListNames)):
    dumpListDict[dumpListNames[i]] = [dumpListNames[i], dumpListImageUrl[i], dumpListUrl[i]]
print(dumpListDict)
browser.close()
