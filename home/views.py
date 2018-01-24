from django.shortcuts import render, get_object_or_404
from bs4 import BeautifulSoup
from selenium import webdriver
import random,string
from collections import OrderedDict

from .scrapper.coursera_seq import Coursera
from .scrapper.edx import Edx
from .scrapper.udemy import Udemy
from .scrapper.youtube import Youtube

udemy = Udemy()
edx = Edx()
coursera = Coursera()
youtube = Youtube()

def order(z):
    newDict = OrderedDict(sorted(z.items(), key=lambda t: t[1]["rating"].split("/")[0]), reversed=True)
    return newDict

def index(request):
    sources = []
    if request.method == "POST":
        print(request.POST)
        query = request.POST.get("search-text")
        if (query==""): return render(request, 'index.html', {  })
        keys = request.POST.keys()
        print(keys)
        if "udemy" in keys:
            sources.append(udemy)
        if "edx" in keys:
            sources.append(edx)
        if "coursera" in keys:
            sources.append(coursera)
        if "youtube" in keys:
            sources.append(youtube)
        if sources==[]: return render(request, 'index.html', { 'dictionaries' : {"code":"No resources are selected"} })

        z = {}
        for source in sources:
            z.update(source.search(query))

        #z = {source.search(query) for source in sources}
        print(z)

        z = order(z)

        return render(request, 'index.html', { 'dictionaries' : z})

    elif request.method == "GET":
        print(request.GET)
    #z = {**coursera.search("python"), **edx.search("python")}
    print("-#"*20)
    return render(request, 'index.html', {  })


#'udemy': ['udemy'], 'free': ['free'], 'youtube': ['youtube'], 'edx': ['edx'], 'search-text': [''], 'csrfmiddlewaretoken': ['zo8EueopuFNfSRmBMI5qfKjc7iHFVZMg3pAkDDZIYrRToO4oZL26qnapNV5xF9xq'], 'search': ['Submit']}>
