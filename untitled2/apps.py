"""Compatibility configuration for Summernote's existing AutoField migrations."""

from django_summernote.apps import DjangoSummernoteConfig


class SummernoteConfig(DjangoSummernoteConfig):
    default_auto_field = "django.db.models.AutoField"
