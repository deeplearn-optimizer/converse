from urllib.parse import urlparse
from django.urls import URLPattern, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views
urlpatterns = [path("", views.getRoutes),
path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("get_answer/",views.get_answer ),]