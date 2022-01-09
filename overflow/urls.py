from django.urls import path

from .views import (
    RegisterApi,
    MyTokenObtainPairView,
    QuestionListView,
    QuestionCreateView,
    AnswerCreateView,
    AnswerCommentView,
    QuestionVoteView,
    QuestionRejectView,
    AnswerVoteView,
    AnswerRejectView,
)

urlpatterns = [
    path("register/", RegisterApi.as_view()),
    path("login/", MyTokenObtainPairView.as_view()),
    path("questionlist/", QuestionListView.as_view(), name="QuestionList"),
    path("question-create/", QuestionCreateView.as_view(), name="QuestionCreate"),
    path("answer-create/", AnswerCreateView.as_view(), name="AnswerCreate"),
    path("answer-comment/", AnswerCommentView.as_view(), name="AnswerComment"),
    path("question-Vote/", QuestionVoteView.as_view(), name="QuestionVote"),
    path("question-reject/", QuestionRejectView.as_view(), name="QuestionReject"),
    path("answer-Vote/", AnswerVoteView.as_view(), name="AnswerVote"),
    path("answer-reject/", AnswerRejectView.as_view(), name="AnswerReject"),
]
