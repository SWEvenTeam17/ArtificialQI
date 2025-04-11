from django.urls import path
from API import views
from .views_def.sessions_view import SessionsView

urlpatterns = [
    path("session_list/", SessionsView.as_view()),
    path("session_list/<int:pk>/", SessionsView.as_view()),
    path("previous_tests/<int:pk>/", views.get_previous_tests),
    path("prompt_list/", views.prompt_list),
    path("prompt_list/<int:pk>/", views.prompt_detail),
    path("answer_list/", views.answer_list),
    path("answer_list/<int:pk>/", views.answer_detail),
    path("llm_list/", views.llm_list),
    path("llm_list/<int:pk>/", views.llm_detail),
    path("llm_list/load_ollama/", views.load_ollama_llms),
    path("llm_add/", views.add_llm_session),
    path("llm_remaining/<int:pk>", views.get_llm_session),
    path("llm_delete/<int:session_id>/<int:llm_id>", views.delete_llm_session),
    path("runtest", views.runtest),
]
