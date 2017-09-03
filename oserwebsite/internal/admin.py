"""Admin models."""

from django.contrib import admin
from .models import Level, Branch, HighSchool, Tutor, Student, \
    TutoringGroup, Country, TutoringMeeting


# Register your models here.


address_fields = ('line1', 'line2', 'post_code', 'city', 'country')

admin.site.register(Level)
admin.site.register(Country)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    """Admin model for Branch."""

    list_display = ('id', 'short_name', 'name',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Admin model for Student."""

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

    list_display = ('id', 'name', 'num_students', 'num_tutors')

    def num_students(self, obj):
        return obj.student_set.count()

    def num_tutors(self, obj):
        return obj.tutor_set.count()


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
