from django.contrib import admin
from .models import VideoContent, VideoAllProxy, VideoPublishedProxy


@admin.register(VideoContent)
class VideoContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_id', 'active']
    search_fields = ['video_id']

    class Meta:
        model=VideoContent


@admin.register(VideoAllProxy)
class VideoAllProxyAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_id','state', 'is_published']
    search_fields = ['video_id']
    list_filter = ['state','active']
    readonly_fields = ['id', 'is_published','publish_timestamp']

    class Meta:
        model=VideoAllProxy


@admin.register(VideoPublishedProxy)
class VideoPublishedProxyAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_id', 'active']
    search_fields = ['video_id']

    class Meta:
        model=VideoPublishedProxy

    def get_queryset(self, request):
        return VideoPublishedProxy.objects.filter(active=True)