from django.test import TestCase
from .models import Category
from playlist.models import Playlist


class CategoryTestCase(TestCase):

    def setUp(self):
        self.cat_a = Category.objects.create(title="Action")
        self.cat_b = Category.objects.create(title="Comedy", active=False)
        self.playlist_a = Playlist.objects.create(title="this is title", category=self.cat_a)

    def test_is_active(self):
        self.assertTrue(self.cat_a.active)

    def test_is_not_active(self):
        self.assertFalse(self.cat_b.active)

    def test_related_playlist(self):
        qs = self.cat_a.playlist.all()
        self.assertEqual(qs.count(), 1)
