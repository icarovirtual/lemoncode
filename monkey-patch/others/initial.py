class MyFormView(FormView):

    def get_initial(self):
        initial = super(MyFormView, self).get_initial()
        # An actual initial value that dependes on some logic
        initial['my_field'] = 1 if self.request.GET.get('param') == 'value' else 2
        # Not really part of the logic, just to avoid typing the fields myself
        initial['field_a'] = 'a_value'
        initial['field_b'] = 'b_value'
        initial['field_c'] = 'c_value'
        initial['field_d'] = 'd_value'
        initial['field_e'] = 'e_value'
        return initial
