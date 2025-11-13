from django.urls import path
from .views import register_view, MyTokenObtainPairView, me_view, LogoutView, LogoutAllView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserUpdateView
urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', me_view, name='me'),
    path('update/', UserUpdateView.as_view(), name='user-update'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout_all/', LogoutAllView.as_view(), name='logout-all'),
]   