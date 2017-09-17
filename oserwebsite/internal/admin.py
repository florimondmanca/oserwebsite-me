"""Admin models."""

from django.contrib import admin
from . import models


# Register your models here.


address_fields = [field.name for field in models.AddressMixin._meta.fields]
address_fields = list(filter(lambda name: name != 'id', address_fields))

admin.site.register(models.Level)
admin.site.register(models.Country)


@admin.register(models.Branch)
class BranchAdmin(admin.ModelAdmin):
    """Admin model for Branch."""

    list_display = ('name', 'short_name')


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    """Admin model for Student."""

    list_display = (
        'full_name', 'user', 'email', 'phone', 'grade', 'tutoring_group',)

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


@admin.register(models.Tutor)
class TutorAdmin(admin.ModelAdmin):
    """Admin model for Tutor."""

    list_display = (
        'full_name', 'email', 'phone', 'tutoring_group')

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


@admin.register(models.TutoringGroup)
class TutoringGroupAdmin(admin.ModelAdmin):
    """Admin model for TutoringGroup."""

    list_display = ('name', 'num_students', 'num_tutors')

    def num_students(self, obj):
        return obj.student_set.count()
    num_students.short_description = 'Lycéens'

    def num_tutors(self, obj):
        return obj.tutor_set.count()
    num_tutors.short_description = 'Tuteurs'


@admin.register(models.TutoringMeeting)
class TutoringMeetingAdmin(admin.ModelAdmin):
    """Admin model for TutoringMeeting."""

    list_display = ('id', 'date', 'high_school',)


@admin.register(models.HighSchool)
class HighSchoolAdmin(admin.ModelAdmin):
    """Admin model for HighSchool."""

    list_display = ('name',)

    fieldsets = (
        (None, {
            'fields': ('name',),
        }),
        ('Addresse', {
            'fields': address_fields,
        })
    )


@admin.register(models.Rope)
class RopeAdmin(admin.ModelAdmin):
    """Admin model for Rope."""

    list_display = ('name',)
