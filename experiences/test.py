from django.core.exceptions import MultipleObjectsReturned
from django.test import TestCase
from model_mommy import mommy
import mox

from .models import Experience, Rating, Review, SubjectiveMixin
from .exptests.models import Reviewed_Item
#Add to settings file
#TESTING = 'test' in sys.argv
#if TESTING:
#    INSTALLED_APPS += ['experiences.exptests',]


class Test_Experience_Model(TestCase):

    def setUp(self):
        self.subject = Reviewed_Item.objects.create()
        self.exp = Experience.objects.create(
            subject_type=self.subject.self_content_type,
            subject_id=self.subject.pk)

    def test_unicode(self):
        self.assertEqual('%s' % self.exp, 'Reviewed_Item object by Anonymous')


class Test_Rating_Model(TestCase):

    def setUp(self):
        self.subject = Reviewed_Item.objects.create()
        self.exp = Experience.objects.create(
            subject_type=self.subject.self_content_type,
            subject_id=self.subject.pk)
        self.rating1 = Rating.objects.create(
            experience=self.exp, score=1, metric='one')
        self.rating2 = Rating.objects.create(
            experience=self.exp, score=2, metric='two')

    def test_unicode(self):
        self.assertEqual('%s' % self.rating1, 'reviewed_ item: 1 - Anonymous')

    def test_experience_average_score(self):
        self.assertEqual(self.exp.average_score(), 1.5)

    def test_subject_average_score(self):
        self.assertEqual(self.subject.get_average_score(), 1.5)

    def test_subject_average_score_filtered(self):
        self.assertEqual(self.subject.get_average_score(metric='one'), 1)


class Test_Review_Model(TestCase):

    def setUp(self):
        self.subject = Reviewed_Item.objects.create()
        self.exp = Experience.objects.create(
            subject_type=self.subject.self_content_type,
            subject_id=self.subject.pk)
        self.review = Review.objects.create(
            experience=self.exp, approved=True,
            text='z' * 28 + 'truncated text')

    def test_unicode(self):
        self.assertEqual('%s' % self.review, 'Anonymous - %strun' % ('z' * 28))

    def test_get_approved_none(self):
        self.review.approved = False
        self.review.save()
        self.assertEqual(self.exp.get_approved_review(), None)

    def test_get_approved_one(self):
        self.assertEqual(self.exp.get_approved_review(), self.review)

    def test_get_approved_multi(self):
        self.review.id = None
        self.review.save()
        self.assertRaises(MultipleObjectsReturned, self.exp.get_approved_review)

    def test_all_approved(self):
        self.assertEqual(self.exp.all_approved_reviews().get(), self.review)


class Test_Subjective_Mixin(TestCase):

    def test_self_content_type(self):
        subject = Reviewed_Item.objects.create()
        self.assertEqual(subject.self_content_type.model, 'reviewed_item')
