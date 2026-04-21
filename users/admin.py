from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from users.models import Skill, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ('id',)
    list_display = (
        'avatar_preview',
        'email',
        'name',
        'surname',
        'is_staff',
        'is_active',
    )
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'name', 'surname')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            'Личные данные',
            {
                'fields': (
                    'name',
                    'surname',
                    'avatar',
                    'phone',
                    'github_url',
                    'about',
                    'skills',
                ),
            },
        ),
        (
            'Права',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        ('Даты', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'name',
                    'surname',
                    'password1',
                    'password2',
                    'is_staff',
                    'is_active',
                ),
            },
        ),
    )
    filter_horizontal = ('groups', 'user_permissions', 'skills')

    @admin.display(description='Аватар')
    def avatar_preview(self, obj):
        if not obj.avatar:
            return '—'
        return format_html(
            '<img src="{}" width="40" height="40" '
            'style="object-fit: cover; border-radius: 50%;" />',
            obj.avatar.url,
        )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'users_count')
    search_fields = ('name',)
    ordering = ('name',)

    @admin.display(description='Пользователи')
    def users_count(self, obj):
        return obj.users.count()
