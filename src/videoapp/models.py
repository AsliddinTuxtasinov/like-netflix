from django.db import models
from django.utils import timezone


class VideoContent(models.Model):
    class VideoStateOptions(models.TextChoices):
        PUBLISH ='PU', 'Publish'
        DRAFT   ='DR', 'Draft'

    title             = models.CharField(max_length=220)
    description       = models.TextField(blank=True, null=True)
    state             = models.CharField(max_length=2, choices=VideoStateOptions.choices, default=VideoStateOptions.DRAFT)
    slug              = models.SlugField(blank=True, null=True)
    video_id          = models.CharField(max_length=220)
    active            = models.BooleanField(default=True)
    publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def is_published(self):
        return self.active

    def save(self, *args, **kwargs):
        if (self.state == self.VideoStateOptions.PUBLISH) and (self.publish_timestamp is None):
            self.publish_timestamp=timezone.now()
        elif self.state == self.VideoStateOptions.DRAFT:
            self.publish_timestamp=None
        super().save(*args, **kwargs)


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