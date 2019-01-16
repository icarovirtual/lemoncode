# Function called in your AppConfig
def monkey_patch():
    # Import inside the function to avoid errors
    from myapp.views import MyFormView

    # Move all the monkey-patch code to be inside this function
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
