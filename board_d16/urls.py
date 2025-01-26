from django.urls import path
from .views import AdvertisementListView, AdvertisementDetailView, AdvertisementCreateView

urlpatterns = [
    path('', AdvertisementListView.as_view(), name='advertisement_list'),
    path('<int:pk>/', AdvertisementDetailView.as_view(), name='advertisement_detail'),
    path('create/', AdvertisementCreateView.as_view(), name='advertisement_create'),
]
