from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from videoflix.db.models import PublishStateOptions
from videoflix.db.receivers import published_state_pre_save, slugify_pre_save
from videoapp.models import VideoContent



class PlaylistManagerQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            state=PublishStateOptions.PUBLISH,
            publish_timestamp__lte=now
        )


class PlaylistManager(models.Manager):
    def get_queryset(self):
        return PlaylistManagerQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()


class Playlist(models.Model):
    title             = models.CharField(max_length=220)
    description       = models.TextField(blank=True, null=True)
    state             = models.CharField(max_length=2, choices=PublishStateOptions.choices, default=PublishStateOptions.DRAFT )
    slug              = models.SlugField(blank=True, null=True)
    video             = models.ForeignKey(VideoContent, related_name='playlist_featured', blank=True, null=True, on_delete=models.SET_NULL)
    videos            = models.ManyToManyField(VideoContent, related_name='playlist_itrms', blank=True )
    active            = models.BooleanField(default=True)
    publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    objects = PlaylistManager()

    def __str__(self):
        return self.title

    @property
    def is_published(self):
        return self.active



pre_save.connect(published_state_pre_save, sender=Playlist)
pre_save.connect(slugify_pre_save, sender=Playlist)