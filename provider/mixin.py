class AttrProviderMixin(object):
    """
    Provide dynamic attributes from a class information.

    References:
        https://stackoverflow.com/q/28861064/1245235
        https://stackoverflow.com/q/4295678/1245235
    """

    is_providing = False
    """
    Flag to avoid infinite loops while trying to provide data.

    Whenever `hasattr` is called, it is expected to raise a `AttributeError`
    in case the attribute doesn't exist but since this flow is interrupted by
    this class, it is necessary to intercept multiple checks of the same
    attribute using this flag and forcefully raise the exception when a loop
    is detected.
    """

    def can_provide_attr(self, attr):
        # Validate in the class' attributes that it's possible to retrieve the
        # expected dynamic attribute
        return False

    def provide_attr(self, attr):
        # Retrieve the value of the requested dynamic attribute
        return None

    def default_for_attr(self, attr):
        # Define a default value for the attribute
        # TODO: Enable having `None` as an option for default value because
        #  currently it is not supported (it indicates that no default value
        #  was provided)
        return None

    def __getattr__(self, item):
        """
        Intercept an invalid attribute check to provide the dynamic value.

        This function differs from `__getattribute__` which is called anytime
        a class attribute is accessed while `__getattr__` is sort of a
        fallback only when the accessed attribute doesn't exist. So this is
        the ideal function to implement this class` functionality.
        """
        try:
            return super().__getattr__(item)
        except AttributeError:
            # Try to detect an attribute validation loop and avoid it by
            # raising the error of an invalid attribute
            if self.is_providing:
                self.is_providing = False
                raise
            # Mark that it's trying to retrieve the attribute to avoid loops
            self.is_providing = True
            # Subclass can provide a default value
            default = self.default_for_attr(item)
            # If it's an unexpected attribute with no default value, the
            # dynamic attribute is not valid in this class
            if not self.can_provide_attr(item) and default is None:
                self.is_providing = False
                raise AttributeError("It was not possible to provide the attribute \"%s\" in %r. "
                                     "Check its availability in the current context." % (item, self))
            # Get the dynamic attribute value, uncheck that it's being
            # retrieved and return it
            attr_value = self.provide_attr(item)
            self.is_providing = False
            return attr_value or default


class KwargsOrGetProviderMixin(AttrProviderMixin):
    """
    Provides values from the view's `kwargs` or GET parameters.

    Instead of using `self.kwargs.get('arg')` or
    `self.request.GET.get('param')` use directly `self.arg` or `self.param`.
    """

    def can_provide_attr(self, attr):
        return \
            self.kwargs and attr in self.kwargs or \
            self.request.GET and attr in self.request.GET

    def provide_attr(self, attr):
        return \
            self.kwargs.get(attr, None) or \
            self.request.GET.get(attr, None)


class CleanedDataProviderMixin(AttrProviderMixin):
    """
    Provides values from `form.cleaned_data`.

    Instead of using `form.cleaned_data.get('field')` use directly
    `form.field`.
    """

    def can_provide_attr(self, attr):
        # Must be a form field
        return self.fields and attr in self.fields

    def provide_attr(self, attr):
        return self.cleaned_data.get(attr, None)
