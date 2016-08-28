from django import forms


class UserProfileForm(forms.Form):
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
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control',
                                                                                 'type': 'date'}))
    city = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                        'placeholder': 'City'}))
    country = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                           'placeholder': 'Country'}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control',
                                                                               'placeholder': 'Description',
                                                                               'rows': '3'}))
