# -*- coding: utf-8 -*-


from django.contrib import admin
from django.contrib.admin.options import IncorrectLookupParameters
from django.contrib.admin.views.main import ChangeList
from django.core.paginator import InvalidPage, Paginator
from django.utils.functional import cached_property


def copy_queryset_without_annotations(original_qs):
    """ Create a new queryset copying the filters but without annotations. """
    # Create a new queryset based on the same model
    optimized_qs = original_qs.model.objects.all()
    # Copy the filters
    optimized_qs.query.where = original_qs.query.where
    optimized_qs.query.where_class = original_qs.query.where_class
    return optimized_qs


class PaginatorWithOptimizedCount(Paginator):
    """
    Optimizes the counting of items.

    This value is calculated for the footer which shows the total of itens in
    all pages of displayed results (objects with filters).
    """

    @cached_property
    def count(self):
        """ Returns the total of itens optimizing the queryset. """
        try:
            return copy_queryset_without_annotations(self.object_list).count()
        except (AttributeError, TypeError):
            # AttributeError if object_list has no count() method.
            # TypeError if object_list.count() requires arguments
            # (i.e. is of type list).
            return len(self.object_list)


class ChangeListWithOptimizedCount(ChangeList):
    """
    Admin listing which optimizes the counting of items.

    Covers the counting of items per page as the total of items of the model
    (objects without filters).
    """

    def get_results(self, request):
        paginator = self.model_admin.get_paginator(request, self.queryset, self.list_per_page)
        # Get the number of objects, with admin filters applied.
        result_count = paginator.count

        # Get the total number of objects, with no admin filters applied.
        if self.model_admin.show_full_result_count:
            full_result_count = copy_queryset_without_annotations(self.root_queryset).count()
        else:
            full_result_count = None
        can_show_all = result_count <= self.list_max_show_all
        multi_page = result_count > self.list_per_page

        # Get the list of objects to display on this page.
        if (self.show_all and can_show_all) or not multi_page:
            result_list = self.queryset._clone()
        else:
            try:
                result_list = paginator.page(self.page_num + 1).object_list
            except InvalidPage:
                raise IncorrectLookupParameters

        self.result_count = result_count
        self.show_full_result_count = self.model_admin.show_full_result_count
        # Admin actions are shown if there is at least one entry
        # or if entries are not counted because show_full_result_count is disabled
        self.show_admin_actions = not self.show_full_result_count or bool(full_result_count)
        self.full_result_count = full_result_count
        self.result_list = result_list
        self.can_show_all = can_show_all
        self.multi_page = multi_page
        self.paginator = paginator


class ModelAdminOptimizedMixin(object):
    """
    Provides optimization of admin classes.

    Applies optimization in model listing and pagination.
    """

    ignore_defer = False
    """ Do not alert about queryset optimization. """

    def get_changelist(self, request, **kwargs):
        return ChangeListWithOptimizedCount

    def get_paginator(self, request, queryset, per_page, orphans=0, allow_empty_first_page=True):
        # Alert about potential optimization
        if not self.ignore_defer and not queryset.query.deferred_loading[0]:
            print("Admin for `%s` does not use `.defer` in its queryset. "
                  "Use this option to further optimize the database requests."
                  % queryset.model._meta.object_name)
        return PaginatorWithOptimizedCount(queryset, per_page, orphans, allow_empty_first_page)


# To use it, simply inherit the mixin in your `ModelAdmin`
@admin.register(YourModel)
class YourModelAdmin(ModelAdminOptimizedMixin, admin.ModelAdmin):
    pass
