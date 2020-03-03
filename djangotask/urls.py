from django.conf.urls import url
from .views import ItemCreateView,ItemDeleteView,\
    ItemDetailView,ItemUpdateView,ItemListView
app_name='djangotask'
urlpatterns = [
  url(r'^item/create/$',ItemCreateView.as_view(),name='item-create'),
  url(r'^item/list/$', ItemListView.as_view(), name='item-list'),
  url(r'^item/(?P<pk>\w+)/$', ItemDetailView.as_view(), name='item-detail'),
  url(r'^item/(?P<pk>\w+)/delete/$', ItemDeleteView.as_view(), name='item-delete'),
  url(r'^item/(?P<pk>\w+)/update/$', ItemUpdateView.as_view(), name='item-update'),

]