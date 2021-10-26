from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify

from videoflix.db.models import PublishStateOptions
from videoapp.models import VideoContent
from .models import Playlist


class VideoContentModelTestCase(TestCase):

    def setUp(self):
        obj_video = VideoContent.objects.create( title='video', video_id="id")
        self.obj_video = obj_video
        self.obj_a = Playlist.objects.create( title="bu title fieldi", video=obj_video )
        self.obj_b = Playlist.objects.create( title="bu title fieldi", state=PublishStateOptions.PUBLISH , video=obj_video )

    def test_playlist_video(self):
        self.assertEqual(self.obj_a.video, self.obj_video)

    def test_video_playlist(self):
        qs = self.obj_video.playlist_set.all()
        self.assertEqual(qs.count(), 2)

    def test_slug_field(self):
        text = self.obj_a.title
        text_slug = slugify(text)
        self.assertEqual(text_slug, self.obj_a.slug)

    def test_valid_title(self):
        title = "bu title fieldi"
        qs=Playlist.objects.filter(title=title)
        self.assertTrue(qs.exists())

    def test_created_count(self):
        qs=Playlist.objects.all()
        self.assertEqual(qs.count(), 2)

    def test_draft_case(self):
        qs = Playlist.objects.filter(state=PublishStateOptions.DRAFT)
        self.assertEqual(qs.count(), 1)

    def test_publish_case(self):
        now = timezone.now()
        qs = Playlist.objects.filter(
            state=PublishStateOptions.PUBLISH,
            publish_timestamp__lte=now )
        self.assertTrue(qs.exists())

    def test_publish_manager(self):
        qs = Playlist.objects.all().published()
        qs2 = Playlist.objects.published()
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(), qs2.count())