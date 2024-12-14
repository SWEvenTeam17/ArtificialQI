from django.urls import path
from API import views

urlpatterns=[
    path('prompt_texts/', views.prompt_text_list),
    path('prompt_texts/<int:pk>/',views.prompt_text_detail),
]