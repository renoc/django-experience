from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property


METRICS = getattr(settings, 'RATING_METRICS', ['overall'])


class Experience(models.Model):
    subject_type = models.ForeignKey(ContentType)
    subject_id = models.PositiveIntegerField(null=False, blank=False)
    subject = GenericForeignKey('subject_type', 'subject_id')
    experiencer = models.CharField(
        max_length=64, null=False, blank=False, default='Anonymous')
    timestamp = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, null=True, blank=True)

    def __unicode__(self):
        return '%s by %s' % (self.subject, self.experiencer)

    class Meta:
        ordering = ['-timestamp']

    def average_score(self):
        return self.rating_set.aggregate(models.Avg('score'))['score__avg']

    def get_approved_review(self):
        # Your schema may require using the all_approved_reviews method
        try:
            return self.review_set.get(approved=True)
        except ObjectDoesNotExist:
            return None

    def all_approved_reviews(self):
        return self.review_set.filter(approved=True)


class Rating(models.Model):
    experience = models.ForeignKey(Experience, null=False, blank=False)
    score = models.DecimalField(
        null=False, blank=False, max_digits=5, decimal_places=2)
    metric = models.CharField(
        max_length=64, null=False, blank=False, default=METRICS[0])

    def __unicode__(self):
        return '%s: %s - %s' % (
            self.experience.subject_type, self.score,
            self.experience.experiencer)


class Review(models.Model):
    experience = models.ForeignKey(Experience, null=False, blank=False)
    approved = models.BooleanField(default=False)
    text = models.TextField(null=False, blank=False)

    def __unicode__(self):
        return '%s - %s' % (self.experience.experiencer, self.text[:32])


class SubjectiveMixin(object):
    METRICS = METRICS

    @cached_property
    def self_content_type(self):
        return ContentType.objects.get_for_model(type(self))

    def get_average_score(self, metric=''):
        ratings = Rating.objects.filter(
            experience__subject_id=self.pk,
            experience__subject_type=self.self_content_type)
        if metric:
            ratings = ratings.filter(metric=metric)
        return ratings.aggregate(models.Avg('score'))['score__avg']
