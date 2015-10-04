from django.db import models

from ..models import SubjectiveMixin


class Reviewed_Item(SubjectiveMixin, models.Model):
    pass
