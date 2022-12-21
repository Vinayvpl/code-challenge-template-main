
from django.urls import path
from .views import  WeatherListApi, YieldListApi, WeatherAnalysisListApi

urlpatterns = [
    path('weather',WeatherListApi.as_view()),
    path("yield",YieldListApi.as_view()),
    path('weather/stats', WeatherAnalysisListApi.as_view()),


]