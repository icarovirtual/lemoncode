from django.views.generic import FormView

from .admin import StatusFilter
from .forms import BaseFilterForm
from .models import Article


class BaseFilterView:
    # List of admin filters
    filters = [StatusFilter]

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        # Pass the filters to the form
        form_kwargs['filters'] = self.filters
        return form_kwargs

    def apply_filters(self, queryset):
        # Map filters submitted in the request to their values
        filter_params = dict(self.request.GET.items())
        for filter_cls in self.filters:
            # Apply the filter if any parameter match the filter
            # `parameter_name`
            filter_obj = filter_cls(self.request, filter_params, None, None)
            queryset = filter_obj.queryset(self.request, queryset)
        return queryset


class ArticleView(BaseFilterView, FormView):
    template_name = 'articles.html'
    # Use the form
    form_class = BaseFilterForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        articles = Article.objects.all()
        # Call the filter function wherever you want to use it
        context_data['articles'] = self.apply_filters(articles)
        return context_data
