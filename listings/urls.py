from django.urls import path

from . import views

urlpatterns = [
    path('', views.index , name='listings'),
    path('<int:listing_id>', views.listing , name='listing'),
    path('search', views.search , name='search'),
    path('ascending', views.ascending , name='ascending'),
    path('descending', views.descending , name='descending'),
    path('comment', views.comment , name='comment'),

]
