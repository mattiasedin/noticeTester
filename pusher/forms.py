from django import forms
from django.forms.utils import ErrorList
from django.forms.models import modelformset_factory
# -*- coding: utf-8 -*-
from .models import *

class BaseParticipantFormSet(forms.models.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(ParticipantFormSet, self).__init__(*args, **kwargs)
        self.forms[0].empty_permitted = False

    def clean(self):
        super(ParticipantFormSet, self).clean()


class ParticipantForm(forms.ModelForm):
    push = forms.BooleanField(required=False)

    class Meta:
        model = Participant
        fields = ['push',]
        exclude=('deviceId',
            'gender',
            'occupation',
        )
    def clean(self):
        cleaned_data = super(ParticipantForm, self).clean()

ParticipantFormSet = modelformset_factory(Participant, form=ParticipantForm, extra=0)