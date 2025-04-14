from django.urls import path
from API import views
from .views_def.sessions_view import SessionsView
from .views_def.prompt_view import PromptView
from .views_def.llm_view import LLMView, OllamaView
from .views_def.answer_view import AnswerView
from .views_def.session_llm_view import SessionLLMView

urlpatterns = [
    path("session_list/", SessionsView.as_view()),
    path("session_list/<int:pk>/", SessionsView.as_view()),
    path("previous_tests/<int:pk>/", views.get_previous_tests),
    path("prompt_list/", PromptView.as_view()),
    path("prompt_list/<int:pk>/", PromptView.as_view()),
    path("answer_list/", AnswerView.as_view()),
    path("answer_list/<int:pk>/", AnswerView.as_view()),
    path("llm_list/", LLMView.as_view()),
    path("llm_list/<int:pk>/", LLMView.as_view()),
    path("llm_list/load_ollama/", OllamaView.as_view()),
    path("llm_add/", SessionLLMView.as_view()),
    path("llm_remaining/<int:pk>", SessionLLMView.as_view()),
    path("llm_delete/<int:session_id>/<int:llm_id>", SessionLLMView.as_view()),
    path("runtest", views.runtest),
]
