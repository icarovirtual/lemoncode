class StatusFilter(admin.SimpleListFilter):
    title = "Status"
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return Article.Status.choices

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(status=value)
