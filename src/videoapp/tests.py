from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify


from .models import VideoContent


class VideoContentModelTestCase(TestCase):

    def setUp(self):
        self.obj_a = VideoContent.objects.create( title="bu title fieldi", video_id="abs")
        self.obj_b = VideoContent.objects.create( title="bu title fieldi",video_id="absdd",
                                                state=VideoContent.VideoStateOptions.PUBLISH )

    def test_slug_field(self):
        text = self.obj_a.title
        text_slug = slugify(text)
        self.assertEqual(text_slug, self.obj_a.slug)

    def test_valid_title(self):
        title = "bu title fieldi"
        qs=VideoContent.objects.filter(title=title)
        self.assertTrue(qs.exists())

    def test_created_count(self):
        qs=VideoContent.objects.all()
        self.assertEqual(qs.count(), 2)

    def test_draft_case(self):
        qs = VideoContent.objects.filter(state=VideoContent.VideoStateOptions.DRAFT)
        self.assertEqual(qs.count(), 1)

    def test_publish_case(self):
        now = timezone.now()
        qs = VideoContent.objects.filter(
            state=VideoContent.VideoStateOptions.PUBLISH,
            publish_timestamp__lte=now
        )
        self.assertTrue(qs.exists())