from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify

from videoflix.db.models import PublishStateOptions
from videoapp.models import VideoContent
from .models import Playlist


class PlaylisttModelTestCase(TestCase):

    # create show with seasons obj for test
    def create_show_with_seasons(self):
        the_office = Playlist.objects.create(title="The office series")
        season_1 = Playlist.objects.create(title="The office series season 1", parent=the_office, order=1)
        season_2 = Playlist.objects.create(title="The office series season 2", parent=the_office, order=2)
        season_3 = Playlist.objects.create(title="The office series season 3", parent=the_office, order=3)
        self.show = the_office

    # video obectlarini test uchun yaratishga tayyor turish
    def create_videos(self):
        obj_video = VideoContent.objects.create(title='video', video_id="id")
        obj_video2 = VideoContent.objects.create(title='video', video_id="id2")
        obj_video3 = VideoContent.objects.create(title='video', video_id="id3")
        self.obj_video = obj_video
        self.obj_video2 = obj_video2
        self.obj_video3 = obj_video3
        self.video_qs = VideoContent.objects.all()

    # vaqtinchalik test uchun test object yaratish
    def setUp(self):
        self.create_videos()
        self.create_show_with_seasons()
        self.obj_a = Playlist.objects.create(title="bu title fieldi", video=self.obj_video)
        obj_b = Playlist.objects.create(title="bu title fiel", state=PublishStateOptions.PUBLISH, video=self.obj_video)
        # obj_b.videos.set([self.obj_video, self.obj_video2, self.obj_video3])
        obj_b.videos.set(self.video_qs)
        obj_b.save()
        self.obj_b = obj_b

    # show objni parent ligini tekshirish season obj lariga nisbatan
    def test_show_has_seasons(self):
        seasons = self.show.playlist_set.all()
        self.assertTrue(seasons.exists())
        self.assertEqual(seasons.count(), 3)

    # playlist yaratilganini test qilish test qilish
    def test_playlist_video(self):
        self.assertEqual(self.obj_a.video, self.obj_video)

    # videos(ManToMany) ni test qilish
    def test_video_playlist_items(self):
        count = self.obj_b.videos.all().count()
        self.assertEqual(count, 3)

    # PlaylistItem va playlist videos(through model)ni test qilish
    def test_playlist_video_through_model(self):
        v_qs = sorted(list(self.video_qs.values_list('id')))
        video_qs = sorted(list(self.obj_b.videos.all().values_list('id')))
        playlist_item_qs = sorted(list(self.obj_b.playlistitem_set.all().values_list('video')))
        self.assertEqual(v_qs, video_qs, playlist_item_qs)

    # video(ForeginKey) ni test qilish
    def test_video_playlist_ids_propery(self):
        ids = self.obj_a.video.get_playlist_ids()
        actualy_ids = list(Playlist.objects.filter(video=self.obj_video).values_list('id', flat=True))
        self.assertEqual(ids, actualy_ids)

    # video(ForeginKey) ni test qilish
    def test_video_playlist(self):
        qs = self.obj_video.playlist_featured.all()
        self.assertEqual(qs.count(), 2)

    # slugni test qilish
    def test_slug_field(self):
        text = self.obj_a.title
        text_slug = slugify(text)
        self.assertEqual(text_slug, self.obj_a.slug)

    # titile kiritilganini test qilish
    def test_valid_title(self):
        title = "bu title fieldi"
        qs = Playlist.objects.filter(title=title)
        self.assertTrue(qs.exists())

    # Playlist yaratilganini test qilish
    def test_created_count(self):
        qs = Playlist.objects.all()
        self.assertEqual(qs.count(), 6)

    # draftni test qilish playlist
    def test_draft_case(self):
        qs = Playlist.objects.filter(state=PublishStateOptions.DRAFT)
        self.assertEqual(qs.count(), 5)

    # publish va publish_timestampni test qilish playlist
    def test_publish_case(self):
        now = timezone.now()
        qs = Playlist.objects.filter(state=PublishStateOptions.PUBLISH, publish_timestamp__lte=now)
        self.assertTrue(qs.exists())

    # publishni test qilish playlist
    def test_publish_manager(self):
        qs = Playlist.objects.all().published()
        qs2 = Playlist.objects.published()
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(), qs2.count())
