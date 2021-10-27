from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from videoflix.db.models import PublishStateOptions
from videoflix.db.receivers import published_state_pre_save, slugify_pre_save



class VideoContentManagerQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            state=PublishStateOptions.PUBLISH,
            publish_timestamp__lte=now
        )


class VideoContentManager(models.Manager):
    def get_queryset(self):
        return VideoContentManagerQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()


class VideoContent(models.Model):
    title             = models.CharField(max_length=220)
    description       = models.TextField(blank=True, null=True)
    state             = models.CharField(max_length=2, choices=PublishStateOptions.choices,
                                         default=PublishStateOptions.DRAFT )
    slug              = models.SlugField(blank=True, null=True)
    video_id          = models.CharField(max_length=220, unique=True)
    active            = models.BooleanField(default=True)
    publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    objects=VideoContentManager()

    def __str__(self):
        return self.title

    @property
    def is_published(self):
        return self.active

    def get_playlist_ids(self):
        # self.<foregned_obj>_set.all() == Foregned_obj.objects.filter(video=video_a)
        return list( self.playlist_featured.all().values_list('id', flat=True) )


class VideoAllProxy(VideoContent):
    class Meta:
        proxy=True
        verbose_name="All Video"
        verbose_name_plural = "All Videos"


class VideoPublishedProxy(VideoContent):
    class Meta:
        proxy=True
        verbose_name="Published Video"
        verbose_name_plural = "Published Videos"


pre_save.connect(published_state_pre_save, sender=VideoContent)
pre_save.connect(slugify_pre_save, sender=VideoContent)