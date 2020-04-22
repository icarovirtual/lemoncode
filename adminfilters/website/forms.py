from django import forms


class BaseFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # Receive the filter instances from the view
        filters = kwargs.pop('filters', [])
        super(BaseFilterForm, self).__init__(*args, **kwargs)
        for f in filters:
            # Create dynamic form fields from the filter
            self.fields[f.parameter_name] = \
                forms.ChoiceField(label=f.title, choices=[('', "Select")] + f._lookups(), required=False)
