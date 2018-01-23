from django.shortcuts import render, get_object_or_404
from bs4 import BeautifulSoup
from selenium import webdriver
import random,string

from .scrapper.coursera_seq import Coursera
from .scrapper.edx import Edx
from .scrapper.udemy import Udemy

udemy = Udemy()
edx = Edx()
coursera = Coursera()

def index(request):
    if request.method == "POST":
        print(request.POST)
    elif request.method == "GET":
        print(request.GET)
    #z = {**coursera.search("python"), **edx.search("python")}
    print("-#"*20)
    return render(request, 'index.html', {  })


