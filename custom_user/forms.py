from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.files.images import get_image_dimensions
from django.utils.translation import ugettext_lazy as _

from .models import User, UserManager


class UserCreationForm(forms.ModelForm):
    # 사용자 생성 폼
    phone = forms.RegexField(
        regex=r'010\d{7,8}',
        label=_('phone'),
        required=True,
        error_messages={'error': '010으로 시작하는 10자리 혹시 11자리 숫자'},
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Phone'),
                'required': 'True',
            }
        )
    )
    name = forms.CharField(
        label=_('name'),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('name'),
                'required': 'True',
            }
        )
    )
    password1 = forms.CharField(
        label=_('Password'),
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Password'),
                'required': 'True',
            }
        )
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Password confirmation'),
                'required': 'True',
            }
        )
    )

    class Meta:
        model = User
        fields = ('phone', 'name', 'password1', 'password2')

    def clean_password2(self):
        # 두 비밀번호 입력 일치 확인
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    # 사용자 변경 폼
    phone = forms.RegexField(
        regex=r'010\d{7,8}',
        label=_('phone'),
        required=True,
        error_messages={'error': '010으로 시작하는 10자리 혹시 11자리 숫자'},
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Phone'),
                'required': 'True',
            }
        )
    )
    name = forms.CharField(
        label=_('name'),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('name'),
                'required': 'True',
            }
        )
    )

    password = ReadOnlyPasswordHashField(
        label=_('비밀번호')
    )

    class Meta:
        model = User
        fields = ('phone', 'name', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]