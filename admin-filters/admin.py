class ArticleAdmin(admin.ModelAdmin):
    list_filter = [StatusFilter]