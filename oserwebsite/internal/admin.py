"""Admin models."""

from django.contrib import admin
from .models import Level, Branch, HighSchool, Tutor, Tutoree, \
    TutoringGroup, Country, TutoringMeeting


# Register your models here.


address_fields = ('line1', 'line2', 'post_code', 'city', 'country')

admin.site.register(Level)
admin.site.register(Country)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    """Admin model for Branch."""

    list_display = ('id', 'short_name', 'name',)


@admin.register(Tutoree)
class TutoreeAdmin(admin.ModelAdmin):
    """Admin model for Tutoree."""

    list_display = (
        'id', 'user', 'full_name', 'email', 'phone', 'grade', 'tutoring_group',)

    fieldsets = (
        (None, {
            'fields': ('user', 'first_name', 'last_name', 'birthday')
        }),
        ('Contact', {
            'fields': ('email', 'phone', *address_fields),
        }),
        ('Tutorat', {
            'fields': ('high_school', 'level', 'branch', 'tutoring_group')
        })
    )

    def get_readonly_fields(self, request, obj=None):
        readonly = ['first_name', 'last_name', 'email']
        if obj:  # This is the case when obj is already created i.e. on edit
            readonly.append('user')
        return readonly


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    """Admin model for Tutor."""

    list_display = (
        'id', 'full_name', 'email', 'phone', 'tutoring_group')

    fieldsets = (
        (None, {
            'fields': ('user', 'first_name', 'last_name', 'birthday')
        }),
        ('Contact', {
            'fields': ('email', 'phone', *address_fields),
        }),
        ('Tutorat', {
            'fields': ('tutoring_group',)
        })
    )

    def get_readonly_fields(self, request, obj=None):
        readonly = ['first_name', 'last_name', 'email']
        if obj:  # This is the case when obj is already created i.e. on edit
            readonly.append('user')
        return readonly


@admin.register(TutoringGroup)
class TutoringGroupAdmin(admin.ModelAdmin):
    """Admin model for TutoringGroup."""

    list_display = ('id', 'name', 'number_tutorees', 'number_tutors')


@admin.register(TutoringMeeting)
class TutoringMeetingAdmin(admin.ModelAdmin):
    """Admin model for TutoringMeeting."""

    list_display = ('id', 'date', 'high_school',)


@admin.register(HighSchool)
class HighSchoolAdmin(admin.ModelAdmin):
    """Admin model for HighSchool."""

    list_display = ('id', 'name',)

    fieldsets = (
        (None, {
            'fields': ('name',),
        }),
        ('Addresse', {
            'fields': address_fields,
        })
    )
