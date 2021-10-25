from django.test import TestCase
from .models import VideoContent


class VideoContentModelTestCase(TestCase):

    def setUp(self):
        VideoContent.objects.create(
            title="bu title fieldi"
        )

    def test_valid_title(self):
        title = "bu title fieldi"
        qs=VideoContent.objects.filter(title=title)
        self.assertTrue(qs.exists())

    def test_created_count(self):
        qs=VideoContent.objects.all()
        self.assertEqual(qs.count(), 1)