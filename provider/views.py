from provider.mixin import CleanedDataProviderMixin, KwargsOrGetProviderMixin


class MyForm(CleanedDataProviderMixin, Form):
    # Your form goes here
    pass


class MyView(KwargsOrGetProviderMixin, FormView):
    form_class = MyForm

    def get(self, request, *args, **kwargs):
        var_x = self.arg_1 * self.arg_2
        self.some_func(var_x, self.param)

    def form_valid(self, form):
        var_1 = self.field_1 + self.field_2
        var_2 = self.field_1 * self.field_3
        self.other_func(var_1, var_2)
