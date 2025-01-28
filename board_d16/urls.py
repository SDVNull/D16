from django.urls import path
from .views import AdvertisementListView, AdvertisementDetailView, AdvertisementCreateView
from . import views

urlpatterns = [
    path('', AdvertisementListView.as_view(), name='advertisement_list'),
    path('<int:pk>/', AdvertisementDetailView.as_view(), name='advertisement_detail'),
    path('create/', AdvertisementCreateView.as_view(), name='advertisement_create'),
    path('advertisement/<int:ad_id>/response/', views.create_response, name='create_response'),
    path('my-responses/', views.my_responses, name='my_responses'),
    path('accept-response/<int:response_id>/', views.accept_response, name='accept_response'),
    path('delete-response/<int:response_id>/', views.delete_response, name='delete_response'),
]
