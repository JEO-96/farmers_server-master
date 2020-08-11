from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from .forms import UserCreationForm, UserChangeForm
from .models import User


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'name', 'phone', 'is_active', 'is_admin', 'date_joined', 'last_login',)
    list_display_links = ('id', 'name',)
    list_filter = ('is_admin', 'is_active',)
    fieldsets = (
        (_('개인정보'), {'fields': ('phone', 'name', 'password',)}),
        (_('권한'), {'fields': ('is_active', 'is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'name', 'password1', 'password2')}
         ),
    )
    search_fields = ('phone', 'name')
    ordering = ('-date_joined',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
