"""Internal website urls."""

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.BrandView.as_view(), name='brand'),
    url(r'^index/$', views.IndexView.as_view(), name='index'),
    url(r'^faq/$', views.FaqView.as_view(), name='faq'),
    url(r'^donnees/$', views.DatabaseView.as_view(), name='database'),
]

# Register views
urlpatterns += [
    url(r'^inscription/$', views.RegisterView.as_view(), name='register'),
    url(r'^inscription/lyceen/(?P<pk>\d+)/$',
        views.RegisterStudentView.as_view(),
        name='register-student'),
    url(r'^inscription/tuteur/(?P<pk>\d+)/$',
        views.RegisterTutorView.as_view(),
        name='register-tutor'),
]

# Student views
urlpatterns += [
    url(r'^lyceen/(?P<pk>\d+)/$', views.StudentDetailView.as_view(),
        name='student-detail'),
    url(r'^lyceens/$', views.StudentListView.as_view(), name="student-list"),
]

# Tutor views
urlpatterns += [
    url(r'^tuteur/(?P<pk>\d+)/$', views.TutorDetailView.as_view(),
        name='tutor-detail'),
    url(r'^tuteurs/$', views.TutorListView.as_view(), name='tutor-list'),
]

# HighSchool views
urlpatterns += [
    url(r'^lycee/(?P<pk>\d+)/$', views.HighSchoolDetailView.as_view(),
        name='highschool-detail'),
    url(r'^lycees/$', views.HighSchoolListView.as_view(),
        name='highschool-list'),
]

# Tutoring group views
urlpatterns += [
    url(r'^groupe/(?P<pk>\d+)/$', views.TutoringGroupDetailView.as_view(),
        name='tutoringgroup-detail'),
    url(r'^groupes/$', views.TutoringGroupListView.as_view(),

        name='tutoringgroup-list'),
]

# Visit views
urlpatterns += [
    url(r'^sorties/$', views.VisitListView.as_view(), name='visit-list'),
]
