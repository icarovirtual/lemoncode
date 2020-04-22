from django.contrib import admin

from .models import Article


class StatusFilter(admin.SimpleListFilter):
    title = "Status"
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return self._lookups()

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(status=value)
        return queryset

    @classmethod
    def _lookups(cls):
        # Static choices used in the forms
        return Article.Status.choices


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_filter = [StatusFilter]
