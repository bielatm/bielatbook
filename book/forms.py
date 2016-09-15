from django import forms
from django.contrib.auth.models import User
from .models import Message, Group, Post


class SignUpForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                            'placeholder': 'User name'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                              'placeholder': 'First name'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                             'placeholder': 'Last name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control',
                                                                           'placeholder': 'Email'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                'placeholder': 'Password'}))
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                        'placeholder':
                                                                                            'Confirm password'}))
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control',
                                                                                 'type': 'date'}))
    city = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                        'placeholder': 'City'}))
    country = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                           'placeholder': 'Country'}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control',
                                                                               'placeholder': 'Description',
                                                                               'rows': '3'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_confirm_password(self):
        if self.data['password'] != self.data.get('confirm_password'):
            raise forms.ValidationError("Passwords don't match")
        return self.data['confirm_password']


class UserProfileForm(forms.Form):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                              'placeholder': 'First name'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                             'placeholder': 'Last name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control',
                                                                           'placeholder': 'Email'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                'placeholder': 'Password'}))
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                        'placeholder':
                                                                                            'Confirm password'}))
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control',
                                                                                 'type': 'date'}))
    city = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                        'placeholder': 'City'}))
    country = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                           'placeholder': 'Country'}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control',
                                                                               'placeholder': 'Description',
                                                                               'rows': '3'}))

    def clean_confirm_password(self):
        if self.data['password'] != self.data.get('confirm_password'):
            raise forms.ValidationError("Passwords don't match")
        return self.data['confirm_password']


class MessageForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '6'}))

    def __init__(self, *args, **kwargs):
        receiver_ids = kwargs.pop('receiver_ids', [])
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['receiver_id'] = forms.ChoiceField(
            choices=receiver_ids,
            widget=forms.Select(attrs={'class': 'form-control'})
        )


class InputMessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': '2'})
        }


class GroupForm(forms.ModelForm):

    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control',
                                                                               'placeholder': 'Description'}))

    class Meta:
        model = Group
        fields = ('name', 'description',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Group name'})
        }
