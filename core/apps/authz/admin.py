from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group as DjangoGroup
from django.utils.translation import gettext_lazy as _
from .models import LowProfile


class Group(DjangoGroup):
    """Instead of trying to get new user under existing `Aunthentication and Authorization`
    banner, create a proxy group model under our Accounts app label.
    Refer to: https://github.com/tmm/django-username-email/blob/master/cuser/admin.py
    """
    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')
        proxy = True
admin.site.unregister(DjangoGroup)


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin):
    pass

@admin.register(LowProfile)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "role_name", "phone_number")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ("username", "email", "first_name", "last_name", "role_name", "is_staff")
    list_filter = ("date_joined", "last_login", "is_staff")
