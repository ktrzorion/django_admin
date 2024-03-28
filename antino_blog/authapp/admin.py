from django.contrib import admin
from .models import MyUser
from django.contrib.auth.admin import UserAdmin

class MyUserAdmin(UserAdmin):

    list_display = ('id', 'email', 'name', 'tc', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields' : ('email', 'password',)}),
        ('Personal info', {'fields' : ('name', 'tc',)}),
        ('Permissions', {'fields' : ('is_admin',)}),
    ) 

    add_fieldsets = (
        (None, {
            'classes' : ('wide',),
            'fields' : ('email', 'name', 'tc', 'password', 're_password',),
        }),
    )
    search_fields = ('email',)
    ordering = ('email', 'id',)
    filter_horizontal = ()

admin.site.register(MyUser, MyUserAdmin)