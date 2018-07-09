from django.shortcuts import render,redirect
from django.http import HttpResponse
import datetime
def index (request):
    title = '首頁.....'
    time = datetime.datetime.now()
    # return HttpResponse("<h2>home about</h2><h2>home contact</h2>")
    # return render (request,'home/index.html',{'title':'首頁...','name':'kuanlin'})
    return render (request,'home/index.html',locals())
def about (request):
    # return HttpResponse("<h2>home about</h2>")
    return render (request,'home/about.html')
    # return redirect('/contact')
def contact (request):
    # return HttpResponse("<h2>home contact</h2>")
    name = request.GET.get("name","man")
    age = request.GET.get("age","0")
    return render (request,'home/contact.html',locals())
def contact1 (request,name,age):
    # return HttpResponse("<h2>home contact</h2>")
    # name = request.GET["name"]
    # age = request.GET["age"]
    return render (request,'home/contact.html',locals())
# Create your views here.
