from django.urls import path
from .views_def.sessions_view import SessionsView
from .views_def.prompt_view import PromptView
from .views_def.llm_view import LLMView, OllamaView
from .views_def.session_llm_view import SessionLLMView
from .views_def.test_view import TestView
from .views_def.prev_test_view import PrevTestView
from .views_def.block_view import BlockView, BlockTestView
from .views_def.run_view import RunPromptView

urlpatterns = [
    path("session_list/", SessionsView.as_view()),
    path("session_list/<int:instance_id>/", SessionsView.as_view()),
    path("previous_tests/<int:instance_id>/", PrevTestView.as_view()),
    path("prompt_list/", PromptView.as_view()),
    path("prompt_list/<int:instance_id>/", PromptView.as_view()),
    path("question_blocks/",BlockView.as_view()),
    path("question_blocks/<int:instance_id>/",BlockView.as_view()),
    path("question_blocks/compare/", BlockTestView.as_view()),
    path("llm_list/", LLMView.as_view()),
    path("llm_list/<int:instance_id>/", LLMView.as_view()),
    path("llm_list_by_session/<int:instance_id>/", SessionLLMView.as_view()),
    path("llm_list/load_ollama/", OllamaView.as_view()),
    path("llm_add/", SessionLLMView.as_view()),
    path("llm_remaining/<int:instance_id>", SessionLLMView.as_view()),
    path("llm_delete/<int:session_id>/<int:llm_id>", SessionLLMView.as_view()),
    path("runtest", TestView.as_view()),
    path("prompt_runs", RunPromptView.as_view()),
]
