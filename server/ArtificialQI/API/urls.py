from django.urls import path
from API import views

urlpatterns=[
    path('questions/', views.question_list),
    path('questions/<int:pk>/',views.question_detail),
]