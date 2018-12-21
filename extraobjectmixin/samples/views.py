from django.core.exceptions import PermissionDenied
from django.views.generic import DetailView

from extraobjectmixin.extraobjectmixin import ExtraObjectMixin


# Include the mixin
class MyExtraObjectView(ExtraObjectMixin, DetailView):

    object = ModelA

    # Minimum required fields for the mixin
    model_extra = ExtraModel
    pk_url_kwarg_extra = 'extramodel_pk'

    def dispatch(self, request, *args, **kwargs):
        # Don't need to use relations or load instances
        if self.get_object_extra().validate_condition_x():
            raise PermissionDenied
        return super(MyExtraObjectView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super(MyExtraObjectView, self).get_context_data(**kwargs)
        # Extra object is loaded and no code repetition
        if not self.object_extra.validate_condition_y():
            context_data['value_x'] = 1
        else:
            context_data['value_x'] = 2
        # Add to context without repetition
        context_data['other_object'] = self.object_extra
        return context_data
