class MyFormView(FormView):

    def get_initial(self):
        initial = super(MyFormView, self).get_initial()
        # Actual logic stays untouched
        initial['my_field'] = 1 if self.request.GET.get('param') == 'value' else 2
        return initial


# Create a function with the same signature
def get_initial_my_form_view(self):
    # The superclass call references the view
    initial = super(MyFormView, self).get_initial()
    # It's important to keep the original logic too
    initial['my_field'] = 1 if self.request.GET.get('param') == 'value' else 2
    # Insert your help code
    initial['field_a'] = 'a_value'
    initial['field_b'] = 'b_value'
    initial['field_c'] = 'c_value'
    initial['field_d'] = 'd_value'
    initial['field_e'] = 'e_value'
    return initial


# At the end of the file, assign to replace the view's function
MyFormView.get_initial = get_initial_my_form_view

# When not needed, just erase the monkey-path code
