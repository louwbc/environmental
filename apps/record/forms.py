#from django
from django import forms
from django.utils.translation import ugettext_lazy as _

# from record
from record.models import Record

class RecordForm(forms.ModelForm):
    """
    Record Form: form associated to the Record model
    """

    def __init__(self, *args, **kwargs):
        super(RecordForm, self).__(*args, **kwargs)
        self.is_update = False

    def clean(self):
        """Do validation stuff. """
        # title is mandatory
        if 'title' not in self.cleaned_data:
            return
        # if a record with that title already exists...
        if not self.is_update:
            if Record.objects.filter(title=self.cleaned_data['title']).count() > 0:
                raise forms.ValidationError(_("There is already this record in the web."))
        return self.cleaned_data

    class Meta:
        model = Record
        fields = ('author', 'description', 'title')
