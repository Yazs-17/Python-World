import time

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("""
    <div>
        <h1>
            欢迎来到我的Project
        </h1>
        <h5>%s</h5>   
        <p>这是我的第四个Project网站</p>
        
    </div>
    """%(time.asctime()))