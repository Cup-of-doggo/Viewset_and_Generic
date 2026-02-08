import re
from rest_framework.serializers import ValidationError


class LessonValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        if not "youtube" in tmp_val:
            raise ValidationError(
                "В названии присутствуют запрещенные слова или ссылки"
            )
