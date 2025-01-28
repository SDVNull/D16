from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from config import settings
from board_d16.views import register_view, verify_email
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_view, name='register'),
    path('verify-email/', verify_email, name='verify_email'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='advertisement_list'), name='logout'),
    path('', include('board_d16.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
