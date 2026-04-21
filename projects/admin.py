from django.contrib import admin

from projects.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'owner',
        'status',
        'participants_count',
        'skills_list',
        'created_at',
    )
    list_display_links = ('id', 'name')
    list_editable = ('status',)
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'description', 'owner__email')
    filter_horizontal = ('participants', 'interested_users', 'skills')

    @admin.display(description='Кол-во участников')
    def participants_count(self, obj):
        return obj.participants.count()

    @admin.display(description='Скиллы')
    def skills_list(self, obj):
        return ', '.join(obj.skills.values_list('name', flat=True))
