from django.contrib import admin
from tags.admin import TaggedItemInline
from .models import MovieProxy, TvShowProxy, TvShowSeasonProxy, Playlist, PlaylistItem


# MovieProxy
class MovieProxyItemInline(admin.TabularInline):
    model = MovieProxy
    extra = 0
    fields = ['order', 'title', 'state', 'slug']


@admin.register(MovieProxy)
class MovieProxyAdmin(admin.ModelAdmin):
    inlines = [MovieProxyItemInline]
    # fields = ['title', 'description', 'state', 'video', 'slug']

    def get_queryset(self, request):
        return MovieProxy.objects.all()


# TvShowProxy
class TvShowProxyItemInline(admin.TabularInline):
    model = TvShowProxy
    extra = 0
    fields = ['order', 'title', 'state', 'slug']


@admin.register(TvShowProxy)
class TvShowProxyAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline, TvShowProxyItemInline]
    # fields = ['title', 'description', 'state', 'video', 'slug']

    def get_queryset(self, request):
        return TvShowProxy.objects.all()


# TvShowSeasonProxy
class TvShowSeasonProxyItemInline(admin.TabularInline):
    model = TvShowSeasonProxy
    extra = 0
    fields = ['order', 'title', 'state', 'slug']


@admin.register(TvShowSeasonProxy)
class TvShowSeasonProxyAdmin(admin.ModelAdmin):
    inlines = [TvShowSeasonProxyItemInline]

    def get_queryset(self, request):
        return TvShowSeasonProxy.objects.all()


# Playlist
class PlaylistItemInline(admin.TabularInline):
    model = PlaylistItem
    extra = 0


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    inlines = [PlaylistItemInline]

    def get_queryset(self, request):
        return Playlist.objects.filter(type=Playlist.PlayListTypeChoices.PLAYLIST)
