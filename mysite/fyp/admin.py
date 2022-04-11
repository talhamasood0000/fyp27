from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Video, VideoOutput

admin.site.unregister(Group)


User = get_user_model()

class AccountAdmin(BaseUserAdmin):
    list_display=('email','username','phonenumber','date_joined','last_login','is_admin','is_staff')
    search_fields=('email','username')
    readonly_fields=('date_joined','last_login')
    filter_horizontal=()
    list_filter=()
    fieldsets=()

admin.site.register(User, AccountAdmin)
admin.site.register(Video)
admin.site.register(VideoOutput)
