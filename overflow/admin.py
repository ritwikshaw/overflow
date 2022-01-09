from django.contrib import admin

from .models import UserAccount
from .models import Question
from .models import Answer


admin.site.register(UserAccount)
admin.site.register(Question)
admin.site.register(Answer)
