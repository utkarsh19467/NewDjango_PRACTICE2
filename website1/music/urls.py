from django.conf.urls import url
from . import views


app_name='music'
urlpatterns=[
    #/music/
    url(r'^$',views.IndexView.as_view(),name='index'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    #/music/album_id/
    url(r'^(?P<pk>[0-9]+)/$',views.DetailsView.as_view(),name='detail'),
    url(r'album/add/$',views.AlbumCreate.as_view(),name='album-add'),
    url(r'album/(?P<pk>[0-9]+)/$',views.AlbumUpdate.as_view(),name='album-update'),
    url(r'album/(?P<pk>[0-9]+)/delete/$',views.AlbumDelete.as_view(),name='album-delete'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),

]