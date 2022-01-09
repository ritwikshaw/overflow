from rest_framework import fields, serializers

# Register serializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from overflow.models import (
    UserAccount,
    Question,
    Answer,
    Qvote,
    Qdown,
    Avote,
    Adown,
    Comment,
)


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ("id", "email", "password", "first_name", "address")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = UserAccount.objects.create_user(
            validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            address=validated_data["address"],
        )
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        # Add extra responses here
        data["id"] = self.user.id
        data["email"] = self.user.email
        data["name"] = self.user.first_name
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = "__all__"


class qvoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qvote
        fields = ("id", "user", "question")


class qdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qdown
        fields = ("id", "user", "question")


class avoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avote
        fields = ("id", "user", "answer")


class adownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adown
        fields = ("id", "user", "answer")


class commentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "user", "body", "answer")


class answerSerializer(serializers.ModelSerializer):
    positivevote = serializers.SerializerMethodField()
    negativevote = serializers.SerializerMethodField()
    acomment = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = (
            "id",
            "user",
            "title",
            "des",
            "questionid",
            "negativevote",
            "positivevote",
            "acomment",
            "created",
        )

    def get_positivevote(self, obj):
        return avoteSerializer(obj.positivevote.all(), many=True).data

    def get_negativevote(self, obj):
        return adownSerializer(obj.negativevote.all(), many=True).data

    def get_acomment(self, obj):
        return commentSerializer(obj.acomment.all(), many=True).data


class questionSerializer(serializers.ModelSerializer):
    positivevote = serializers.SerializerMethodField()
    negativevote = serializers.SerializerMethodField()
    answer = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = (
            "id",
            "user",
            "title",
            "des",
            "positivevote",
            "negativevote",
            "answer",
            "created",
        )

    def get_positivevote(self, obj):
        return qvoteSerializer(obj.positivevote.all(), many=True).data

    def get_negativevote(self, obj):
        return qdownSerializer(obj.negativevote.all(), many=True).data

    def get_answer(self, obj):
        return answerSerializer(obj.answer.all(), many=True).data
