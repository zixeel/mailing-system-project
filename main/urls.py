from django.urls import path
from main.apps import MainConfig
from django.views.decorators.cache import never_cache
from main.views import (MailListView,MailCreateView, MessageCreateView,
                           ClientCreateView, MailDetailView, MailUpdateView,
                           MailDeleteView, MailEndingListView, ClientDeleteView,
                           ClientListView)


app_name = MainConfig.name


urlpatterns = [
    path('', MailListView.as_view(), name='mail_list'),
    path('completed/', MailEndingListView.as_view(), name='mail_complete'),

    path('create/', never_cache(MailCreateView.as_view()), name='mail_create'),
    path('edit/<int:pk>/', never_cache(MailUpdateView.as_view()), name='mail_update'),
    path('detail/<int:pk>/', MailDetailView.as_view(), name='mail_detail'),
    path('delete/<int:pk>/', MailDeleteView.as_view(), name='mail_delete'),

    path('message/create/', MessageCreateView.as_view(), name='message_create'),

    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
]