from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from videoflix.db.models import PublishStateOptions
from videoflix.db.receivers import published_state_pre_save, slugify_pre_save
from videoapp.models import VideoContent
from categories.models import Category


class PlaylistManagerQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            state=PublishStateOptions.PUBLISH,
            publish_timestamp__lte=now)


class PlaylistManager(models.Manager):
    def get_queryset(self):
        return PlaylistManagerQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()


class Playlist(models.Model):
    class PlayListTypeChoices(models.TextChoices):
        MOVIE = "MOV", "Movie"
        SHOW = "SVS", "Tv Show"
        SEASON = "SEA", "Season"
        PLAYLIST = "PLY", "Playlist"

    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, related_name="playlist", blank=True, null=True, on_delete=models.SET_NULL)
    order = models.IntegerField(default=1)
    title = models.CharField(max_length=220)
    type = models.CharField(max_length=3, choices=PlayListTypeChoices.choices, default=PlayListTypeChoices.PLAYLIST)
    description = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=2, choices=PublishStateOptions.choices, default=PublishStateOptions.DRAFT)
    slug = models.SlugField(blank=True, null=True)
    video = models.ForeignKey(VideoContent, related_name='playlist_featured',
                              blank=True, null=True, on_delete=models.SET_NULL)
    videos = models.ManyToManyField(VideoContent, related_name='playlist_itrms', blank=True, through='PlaylistItem')
    active = models.BooleanField(default=True)
    publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    objects = PlaylistManager()

    def __str__(self):
        return self.title

    @property
    def is_published(self):
        return self.active


# Movie Proxy
class MovieProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(type=Playlist.PlayListTypeChoices.MOVIE)


class MovieProxy(Playlist):
    objects = MovieProxyManager()

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"
        proxy = True

    def save(self, *args, **kwargs):
        self.type = Playlist.PlayListTypeChoices.MOVIE
        super().save(*args, **kwargs)


# Tv Show Proxy
class TvShowProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(parent__isnull=True, type=Playlist.PlayListTypeChoices.SHOW)


class TvShowProxy(Playlist):
    objects = TvShowProxyManager()

    class Meta:
        verbose_name = "TV Shov"
        verbose_name_plural = "TV Shows"
        proxy = True

    def save(self, *args, **kwargs):
        self.type = Playlist.PlayListTypeChoices.SHOW
        super().save(*args, **kwargs)


# Tv Show Season Proxy
class TvShowSeasonProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(parent__isnull=False, type=Playlist.PlayListTypeChoices.SEASON)


class TvShowSeasonProxy(Playlist):
    objects = TvShowSeasonProxyManager()

    class Meta:
        verbose_name = "Season"
        verbose_name_plural = "Seasons"
        proxy = True

    def save(self, *args, **kwargs):
        self.type = Playlist.PlayListTypeChoices.SEASON
        super().save(*args, **kwargs)


# Play list Item for through
class PlaylistItem(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    video = models.ForeignKey(VideoContent, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-timestamp']


pre_save.connect(published_state_pre_save, sender=Playlist)
pre_save.connect(slugify_pre_save, sender=Playlist)
