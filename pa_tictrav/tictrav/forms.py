from django import forms

from tictrav import models

class DateTimeInput(forms.DateTimeInput):
        input_type = 'datetime'



class EditUserForm(forms.ModelForm):
    email = forms.EmailField(label='email',max_length=254, required=True)
    full_name = forms.CharField(label='full_name',max_length=300, required=False)
    age = forms.IntegerField(label='age', required=False)
    location = forms.CharField(label='location',max_length=1000, required=False)
    password = forms.CharField(widget=forms.PasswordInput, label='password', required=True, max_length=500)

    class Meta:
        model = models.AccountCustom
        fields = ('email','full_name','age','location', 'password')

    """
        Pengaturan Password
    """
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class ReservationForm(forms.ModelForm):
    user = forms.IntegerField()
    place = forms.IntegerField()
    due_date = forms.DateTimeField(required=False, widget=forms.TextInput(attrs={'type':'datetime-local'}))
    
    class Meta:
        model = models.Reservation
        fields = ('user','place','due_date')