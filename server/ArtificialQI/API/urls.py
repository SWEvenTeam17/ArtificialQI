from django.urls import path
from API import views

urlpatterns=[
    path('prompt_list/', views.prompt_list),
    path('prompt_list/<int:pk>/', views.prompt_detail),
    path('answer_list/', views.answer_list),
    path('answer_list/<int:pk>/', views.answer_detail),
    path('llm_list/', views.llm_list),
    path('llm_list/<int:pk>/', views.llm_detail),
    path('test',views.test)
]