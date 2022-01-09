from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from overflow.models import (
    Answer,
    UserAccount,
    Question,
    Comment,
    Qvote,
    Qdown,
    Avote,
    Adown,
)
from overflow.serializer import (
    RegisterSerializer,
    MyTokenObtainPairSerializer,
    UserSerializer,
    questionSerializer,
    answerSerializer,
)

# Create your views here.


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "message": "User Created Successfully.  Now perform Login to get your token",
            }
        )


class QuestionListView(ListAPIView):
    serializer_class = questionSerializer
    queryset = Question.objects.all()


class QuestionCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = questionSerializer

    def post(self, request, *args, **kwargs):
        title = request.data.get("title")
        des = request.data.get("des")
        question = Question.objects.create(user=self.request.user, title=title, des=des)
        question.save()
        return Response(status=HTTP_200_OK)


class AnswerCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = answerSerializer

    def post(self, request, *args, **kwargs):
        title = request.data.get("title")
        des = request.data.get("des")
        qid = request.data.get("questionid")
        question = Question.objects.get(id=qid)
        if question is None:
            return Response({"message": "Invalid request"}, status=HTTP_400_BAD_REQUEST)
        ans = Answer.objects.create(
            user=self.request.user, title=title, des=des, questionid=id
        )
        ans.save()
        question.answer.add(ans)
        return Response(status=HTTP_200_OK)


class AnswerCommentView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = answerSerializer

    def post(self, request, *args, **kwargs):
        answer = request.data.get("answer")
        id = request.data.get("answerid")
        ans = Answer.objects.get(id=id)
        if ans is None:
            return Response({"message": "Invalid request"}, status=HTTP_400_BAD_REQUEST)
        comment = Comment.objects.create(
            user=self.request.user, body=answer, answer=ans
        )
        comment.save()
        ans.acomment.add(comment)
        return Response(status=HTTP_200_OK)


class QuestionVoteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        qid = request.data.get("questionid")
        question = Question.objects.get(id=qid)
        vote = Qvote.objects.create(user=self.request.user, question=question)
        vote.save()
        question.positivevote.add(vote)
        return Response(status=HTTP_200_OK)


class QuestionRejectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        qid = request.data.get("questionid")
        question = Question.objects.get(id=qid)
        vote = Qdown.objects.create(user=self.request.user, question=question)
        vote.save()
        question.negativevote.add(vote)
        return Response(status=HTTP_200_OK)


class AnswerVoteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        aid = request.data.get("questionid")
        ans = Answer.objects.get(id=aid)
        vote = Avote.objects.create(user=self.request.user, answer=ans)
        vote.save()
        ans.positivevote.add(vote)
        return Response(status=HTTP_200_OK)


class AnswerRejectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        aid = request.data.get("questionid")
        ans = Answer.objects.get(id=aid)
        vote = Adown.objects.create(user=self.request.user, answer=ans)
        vote.save()
        ans.negativevote.add(vote)
        return Response(status=HTTP_200_OK)
