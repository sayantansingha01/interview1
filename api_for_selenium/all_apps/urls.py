from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/', views.SignUpView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('token_resfresh/', TokenRefreshView.as_view()),
    path('get_profile/', views.Proile.as_view()),
    path('selenium/', views.SeleniumView.as_view()),
    path('pdf/', views.FileShowView.as_view())

]