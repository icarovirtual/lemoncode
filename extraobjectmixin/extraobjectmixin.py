from django.shortcuts import get_object_or_404


class ExtraObjectMixin(object):
    """ Provides a second object via URL parameter. """

    model_extra = None
    """ Type of the model. """

    pk_url_kwarg_extra = None
    """ Argument name for the object's PK. """

    slug_url_kwarg_extra = None
    """ Argument name for the object's slug. """
    slug_field_extra = None
    """
    Object's field name that maps the slug argument.
    If undefined, will use `slug_url_kwarg_adicional`.
    """

    object_extra = None
    """ Extra object's instance. """

    def dispatch(self, request, *args, **kwargs):
        """ Prepare the extra object. """
        self.get_object_extra()
        return super(ExtraObjectMixin, self).dispatch(request, *args, **kwargs)

    def get_object_extra(self):
        """ Try to prepare the extra object . """
        # Re-use the object if it's been loaded
        if self.object_extra is not None:
            return self.object_extra
        # Required fields
        if not self.model_extra or not (self.pk_url_kwarg_extra or self.slug_url_kwarg_extra):
            raise AttributeError("Define the `model_extra` field and `pk_url_kwarg_extra` or `slug_url_kwarg_extra`.")
        # Use the PK to load the instance
        if self.pk_url_kwarg_extra:
            self.object_extra = get_object_or_404(self.model_extra, pk=self.kwargs[self.pk_url_kwarg_extra])
        # Use the slug to load the instance
        elif self.slug_url_kwarg_extra:
            # Check if should use the slug argument or it's own field name
            slug_field = self.slug_field_extra or self.slug_url_kwarg_extra
            self.object_extra = get_object_or_404(self.model_extra, **{slug_field: self.kwargs[self.slug_url_kwarg_extra]})
        return self.object_extra
