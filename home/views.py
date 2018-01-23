from django.shortcuts import render
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
    z = {**coursera.search("python"), **edx.search("python")}
    return render(request, 'index.html', { 'dictionaries':  z  })


