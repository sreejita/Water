from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import AuthenticationForm
import pandas as pd
from io import BytesIO
from .tasks import *
import re


class PersonalInfoForm(forms.Form):
    job_name = forms.CharField(label='Job Name', max_length=100,
                               widget=forms.TextInput(attrs={'placeholder': 'Enter Job Name'}))
    email = forms.EmailField(label='Email',
                             widget=forms.TextInput(attrs={'placeholder': 'Enter Email address to notify'}))
    email2 = forms.EmailField(label='Confirm Email',
                              widget=forms.TextInput(attrs={'placeholder': 'Confirm you Email address'}))


# YG
class UploadDatasetForm(forms.Form):
    wfid = forms.CharField(label='Workflow ID',
                           max_length=100, required=True,
                           widget=forms.TextInput(attrs={'placeholder': 'Workflow ID'}))
    fragid = forms.CharField(label='Fragment ID', max_length=100, required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Fragment ID'}))
    name = forms.CharField(label='Name*',
                           help_text='The file uploader will appear once you enter the dataset name',
                           max_length=100, required=True,
                           widget=forms.TextInput(attrs={'placeholder': 'Please enter your dataset name'}))
    description = forms.CharField(label='Description (optional)', max_length=100, required=False,
                                  widget=forms.Textarea(attrs={'placeholder': 'Describe your data here.', 'rows': '2'}))

    docfile = forms.FileField(label='Choose file')


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username',
                               max_length=100, required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Please enter a username'}))
    password1 = forms.CharField(label='Password',
                                max_length=100, required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Please enter a password'}))
    password2 = forms.CharField(label='Re-enter password',
                                max_length=100, required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Please reenter your password'}))
    # email = forms.CharField(label='Email*',max_length=100, required=True,
    #                        widget=forms.TextInput(attrs={'placeholder': 'Please enter a username'}))
    email = forms.EmailField(label='Email', required=True)

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords do not match.')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Username is already taken.')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))


class FileUploadForm(forms.Form):
    docfile = forms.FileField(label='Select a file',
                              help_text='max. 42 megabytes')
    days = forms.ChoiceField(widget=forms.Select(), choices=([('1', '1'), ('2', '2'), ('3', '3'), ]), initial=1,
                             required=False)


class FileUploadFormList(forms.Form):
    def __init__(self, *args, **kwargs):
        self.header = kwargs.pop('header')
        options = []
        for head in self.header:
            options.append((head, head))
        super(FileUploadFormList, self).__init__(*args, **kwargs)
        self.fields['list'] = forms.ChoiceField(widget=forms.Select(
            attrs={'class': 'selectpicker show-tick show-menu-arrow', 'data-width': "fit",
                   'data-style': "btn-warning"}), choices=[(o, o) for o in self.header], initial=self.header[0],
            required=False)


def getPairCountDropDownField():
    numbers = range(1, 21)
    return forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'selectpicker show-tick show-menu-arrow', 'data-width': "fit", 'data-style': "btn-warning"}),
        choices=[(i, i) for i in numbers], initial=numbers[4], required=True)


class SelectModeForm(forms.Form):
    pair_count = getPairCountDropDownField()
    docfile = forms.FileField(required=False, label='Select a file', help_text='max. 42 megabytes')


class SelectCrowdModeForm(forms.Form):
    docfile = forms.FileField(required=False, label='Select a file', help_text='max. 42 megabytes')
    pair_count = getPairCountDropDownField()
    reward_amount = forms.FloatField(label='Reward amount for labelling each batch',
                                     help_text='Tooltip description goes here for reward amount',
                                     widget=forms.TextInput(
                                         attrs={'type': 'number', 'step': 0.01, 'class': "form-control", 'min': 0}))
    assignment_duration_hit = forms.IntegerField(label='Assignment duration for this HIT (hours)',
                                                 help_text='Tooltip description goes here for assignment duration',
                                                 widget=forms.TextInput(
                                                     attrs={'type': 'number', 'class': "form-control", 'min': 0}))
    auto_approval_delay = forms.IntegerField(label='Auto Approval Delay (days)',
                                             help_text='Tooltip description goes here for auto approval delay',
                                             widget=forms.TextInput(
                                                 attrs={'type': 'number', 'class': "form-control", 'min': 0}))
    hit_lifetime = forms.IntegerField(label='HIT lifetime (days)',
                                      help_text='Tooltip description goes here for hit lifetime',
                                      widget=forms.TextInput(
                                          attrs={'type': 'number', 'class': "form-control", 'min': 0}))
    initial_assignment = forms.IntegerField(label='Number of Initial Assignment',
                                            help_text='Tooltip description goes here for initial assignment',
                                            widget=forms.TextInput(
                                                attrs={'type': 'number', 'class': "form-control", 'min': 0}))
    mturk_access_key = forms.CharField(label='MTurk Access Key', max_length=300,
                                       help_text='Tooltip description goes here for mturk_access_key',
                                       widget=forms.TextInput(attrs={'type': 'text', 'class': "form-control"}))
    mturk_secret_key = forms.CharField(label='MTurk Secret Key', max_length=300,
                                       help_text='Tooltip description goes here for mturk_secret_key',
                                       widget=forms.TextInput(attrs={'type': 'text', 'class': "form-control"}))


class JobProgressForm(forms.Form):
    job_id = forms.IntegerField(label='Job ID', help_text='Enter Job ID to get the progress',
                                widget=forms.TextInput(attrs={'type': 'number', 'class': "form-control", 'min': 1}))
