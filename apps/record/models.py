# python
import os
from os import path
from datetime import datetime

# django imports
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class Record(models.Model):
    """
    Record Model:
    """
    title = models.CharField(('title'), max_length=255)
    author = models.CharField(('author'), max_length=255)
    description = models.TextField(('description'), blank=True)
    adder = models.ForeignKey(User, related_name="added_records", verbose_name=('adder'))
    added = models.DateTimeField(('added'), default=datetime.now)
