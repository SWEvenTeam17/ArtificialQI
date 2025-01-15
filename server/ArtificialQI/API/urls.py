from django.urls import path
from API import views

urlpatterns=[
    path('session_list/', views.session_list),
    path('session_list/<int:pk>/', views.session_detail),
    path('prompt_list/', views.prompt_list),
    path('prompt_list/<int:pk>/', views.prompt_detail),
    path('answer_list/', views.answer_list),
    path('answer_list/<int:pk>/', views.answer_detail),
    path('llm_list/', views.llm_list),
    path('llm_list/<int:pk>/', views.llm_detail),
    path('llm_add/', views.add_llm_session),
    path('llm_remaining/<int:pk>', views.get_llm_session),
    path('llm_delete/<int:session_id>/<int:llm_id>', views.delete_llm_session),
    path('runtest', views.runtest)
]