class MyComplexView(DetailView):

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Relations can get very long (which type even is `related_object_b`?)
        if not self.object.related_object_a.related_object_b.validate_condition_x():
            raise PermissionDenied
        # Load other object (that is needed in multiple places) manually
        other_object = get_object_or_404(MyOtherModel, condition_n=True, condition_m=False)
        if other_object.validate_condition_w():
            raise PermissionDenied
        return super(MyComplexView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super(MyComplexView, self).get_context_data(**kwargs)
        # Repeating long sentence only to use a different function
        if not self.object.related_object_a.related_object_b.validate_condition_y():
            context_data['value_x'] = 1
        else:
            context_data['value_x'] = 2
        # Code duplication from `dispatch` to load other object
        context_data['other_object'] = get_object_or_404(MyOtherModel, condition_n=True, condition_m=False)
        return context_data
