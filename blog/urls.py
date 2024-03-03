from django.urls import path

from blog.apps import BlogConfig
from django.views.decorators.cache import cache_page, never_cache

from blog.views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView, MainListView

app_name = BlogConfig.name

urlpatterns = [
    path('', never_cache(MainListView.as_view()), name='main'),

    path('blog/', cache_page(60)(BlogListView.as_view()), name='blog_list'),
    path('blog/create/', never_cache(BlogCreateView.as_view()), name='blog_create'),
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/edit/<slug:slug>/', never_cache(BlogUpdateView.as_view()), name='blog_update'),
    path('blog/delete/<slug:slug>/', BlogDeleteView.as_view(), name='blog_delete'),
]