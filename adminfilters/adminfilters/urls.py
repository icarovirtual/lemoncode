from django.contrib import admin
from django.urls import path

from website.views import ArticleView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ArticleView.as_view()),
]
