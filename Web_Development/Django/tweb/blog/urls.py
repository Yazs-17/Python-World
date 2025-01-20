from django.urls import path, include

import blog.views

urlpatterns = [
    path('hello_world', blog.views.hello_world),
    path('', blog.views.index),
    path('index',blog.views.get_index_page),
    # path('admin/', blog.views.admin),
    # path('detail', blog.views.get_detail_page),
    path('detail/<int:article_id>', blog.views.get_detail_page),
]