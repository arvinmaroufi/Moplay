from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ChapterSeries


@receiver(post_save, sender=ChapterSeries)
def update_series_chapter_count_on_save(sender, instance, created, **kwargs):
    if created:
        series = instance.series
        series.chapter_count = series.chapterseries_set.count()
        series.save()


@receiver(post_delete, sender=ChapterSeries)
def update_series_chapter_count_on_delete(sender, instance, **kwargs):
    series = instance.series
    series.chapter_count = series.chapterseries_set.count()
    series.save()
