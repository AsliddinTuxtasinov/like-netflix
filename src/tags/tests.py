from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.test import TestCase
from django.db.utils import IntegrityError
from playlist.models import Playlist
from .models import TaggedItem


class TaggedItemTestCase(TestCase):

    def setUp(self):
        playlist_title = "new playlist title"
        self.playlist_obj = Playlist.objects.create(title=playlist_title)
        self.playlist_obj2 = Playlist.objects.create(title=playlist_title)
        self.playlist_title = playlist_title
        self.playlist_obj.tags.add(TaggedItem(tag="new-tag"), bulk=False)
        self.playlist_obj2.tags.add(TaggedItem(tag="new-tag"), bulk=False)
        # self.tag_a = TaggedItem.objects.create(tag="my-new-tag")

    # content_type null emasligini tekshirish
    def test_content_type_is_not_null(self):
        # self.assertIsNotNone(self.tag_a.pk)
        with self.assertRaises(IntegrityError):
            TaggedItem.objects.create(tag="my-new-tag")

    # content_type orqali yaratish
    def test_create_via_type(self):
        c_type = ContentType.objects.get(app_label='playlist', model='playlist')
        # c_type.model_class() => Playlist
        tag_a = TaggedItem.objects.create(tag="my-new-tag", content_type=c_type, object_id=1)
        self.assertIsNotNone(tag_a.pk)

    # model, content_type orqali yaratish
    def test_create_via_model_content_type(self):
        c_type = ContentType.objects.get_for_model(Playlist)
        tag_a = TaggedItem.objects.create(tag="my-new-tag", content_type=c_type, object_id=1)
        self.assertIsNotNone(tag_a.pk)

    # app, content_type orqali yaratish
    def test_create_via_app_loader_content_type(self):
        playListClass = apps.get_model(app_label='playlist', model_name='Playlist')
        c_type = ContentType.objects.get_for_model(playListClass)
        tag_a = TaggedItem.objects.create(tag="my-new-tag", content_type=c_type, object_id=1)
        self.assertIsNotNone(tag_a.pk)

    # releted_field ni test qilish
    def test_releted_field(self):
        self.assertEqual(self.playlist_obj.tags.count(), 1)

    # releted_field orqali tag obj yaratish
    def test_releted_field_create(self):
        self.playlist_obj.tags.create(tag="another-new-tag")
        self.assertEqual(self.playlist_obj.tags.count(), 2)

    # releted_field orqali filter qilish
    def test_releted_field_query_name(self):
        qs = TaggedItem.objects.filter(playlist__title__iexact=self.playlist_title) # playlist is releted_query_name that tags field in Playlist model
        self.assertEqual(qs.count(), 2)

    # releted_field da content_type orqali filter qilish
    def test_releted_field_via_content_type(self):
        c_type = ContentType.objects.get_for_model(Playlist)
        tag_qs = TaggedItem.objects.filter(content_type=c_type, object_id=self.playlist_obj.id)
        self.assertEqual(tag_qs.count(), 1)

    # togridan togri obj yaratish
    def test_direct_obj_creation(self):
        obj = self.playlist_obj
        tag = TaggedItem.objects.create(content_object=obj, tag='another1')
        self.assertIsNotNone(tag.pk)
