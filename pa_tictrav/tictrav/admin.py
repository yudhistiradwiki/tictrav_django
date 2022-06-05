from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from tictrav.models import AccountCustom, TourismPlace

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
# Register your models here.

# Bagian Admin untuk melakukan pembuatan akun
class UserCreationForm(forms.ModelForm):
	password = forms.CharField(label='password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='password_confirm', widget=forms.PasswordInput)


	class Meta:
		model = AccountCustom
		fields = ('email','full_name','age','location')

	def clean_password(self):
		password = self.cleaned_data.get('password')
		password2 = self/cleaned_data.get('password2')

		if password and password2 and password != password2:
			raise forms.ValidationError('Password tidak sama')
		return password2

	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password'])
		if commit:
			user.save()
		return user

# Modifikasi akun
class UserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = AccountCustom
		fields = ('email', 'password','is_admin', 'is_active','is_staff','is_superuser')

	def clean_password(self):
		return self.initial['password']


# Class admin
class UserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'full_name', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name','location')}),
        ('Permissions', {'fields': ('is_admin', 'is_active','is_staff','is_superuser')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(AccountCustom, UserAdmin)
admin.site.register(TourismPlace)