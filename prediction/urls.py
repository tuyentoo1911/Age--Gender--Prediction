from django.urls import path
from .views import (
    HomeView, PredictView, CameraPredictView, 
    AboutView, HistoryView, StatsView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('predict/', PredictView.as_view(), name='predict'),
    path('camera-predict/', CameraPredictView.as_view(), name='camera_predict'),
    path('about/', AboutView.as_view(), name='about'),
    path('history/', HistoryView.as_view(), name='history'),
    path('stats/', StatsView.as_view(), name='stats'),
] 