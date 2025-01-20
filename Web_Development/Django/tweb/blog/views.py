from django.shortcuts import render
from django.http import HttpResponse
from .models import Article
from django.core.paginator import Paginator
def hello_world(request):
    return HttpResponse("""
    <h1>Hello World!</h1>
    <div style = 'display:flex;justify-content:center;'></div>
    <p>Welcome to my blog!</p>
    """)

def index(request):
    return HttpResponse("""
    <h2>APP blog.index</h2>
    
    """)

def get_index_page(request):
    page = request.GET.get('page')
    if page:
        page = int(page)
    else:
        page = 1
    print(page)
    all_article = Article.objects.all()
    paginator = Paginator(all_article, 2)
    page_num = paginator.num_pages
    print('page number:', page_num)
    page_article_list = paginator.page(page)
    if page_article_list.has_next():
        next_page = page + 1
    else:
        next_page = page
    if page_article_list.has_previous():
        previous_page = page - 1
    else:
        previous_page = page


    return render(request, 'blog/index.html',
                  {
                        'article_list': page_article_list,
                        'page_num':range(1,paginator.num_pages + 1),
                        'curr_page': page,
                        'next_page': next_page,
                        'previous_page': previous_page,
                        'top_2_article': Article.objects.order_by('-publish_date')[:2],
                  }
                )

def get_detail_page(request,article_id):
    all_article = Article.objects.all()
    cur_article = None
    pre_index = 0
    net_index = 0
    pre_article = None
    net_article = None
    for index,article in enumerate(all_article):
        if index == 0:
            pre_index = index
            net_index = index + 1
        elif index == len(all_article) - 1:
            pre_index = index - 1
            net_index = index
        else:
            pre_index = index - 1
            net_index = index + 1

        if article.article_id == article_id:
            cur_article = article
            pre_article = all_article[pre_index]
            net_article = all_article[net_index]
            break
    section = cur_article.content.split('\n')
    return render(request, 'blog/detail.html',
                  {
                        'curr_article': cur_article,
                        'section': section,
                        "previous_article": pre_article,
                        "next_article":net_article
                  }
                )