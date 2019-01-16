# Define your flags as constants which you can toggle easily
MY_FORM_VIEW_PATCH = True
OTHER_VIEW_PATCH = True


def monkey_patch():
    # Create if statements for constant
    if MY_FORM_VIEW_PATCH:
        from myapp.views import MyFormView

        def get_initial_my_form_view(self):
            initial = super(MyFormView, self).get_initial()
            initial['my_field'] = 1 if self.request.GET.get('param') == 'value' else 2
            initial['field_a'] = 'a_value'
            initial['field_b'] = 'b_value'
            initial['field_c'] = 'c_value'
            initial['field_d'] = 'd_value'
            initial['field_e'] = 'e_value'
            return initial

        MyFormView.get_initial = get_initial_my_form_view
    # Each will contain it's monkey-patch
    elif OTHER_VIEW_PATCH:
        from myapp.views import OtherView

        def get_initial_other_view(self):
            initial = super(OtherView, self).get_initial()
            initial['other_field'] = 'other_value'
            return initial

        OtherView.get_initial = get_initial_other_view
