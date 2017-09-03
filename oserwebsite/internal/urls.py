"""Internal website urls."""

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.BrandView.as_view(), name='brand'),
    url(r'^index/$', views.IndexView.as_view(), name='index'),
    url(r'^inscription/$', views.RegisterView.as_view(), name='register'),
    url(r'^faq/$', views.FaqView.as_view(), name='faq'),
]

# Student views
urlpatterns += [
    url(r'^tutore/(?P<pk>\d+)/$', views.StudentDetailView.as_view(),
        name='student-detail'),
]

# Tutor views
urlpatterns += [
    url(r'^tuteur/(?P<pk>\d+)/$', views.TutorDetailView.as_view(),
        name='tutor-detail'),
]

# HighSchool views
urlpatterns += [
    url(r'^lycee/(?P<pk>\d+)/$', views.HighSchoolDetailView.as_view(),
        name='highschool-detail'),
    url(r'^lycees/$', views.HighSchoolListView.as_view(), name='highschools'),
]

# Tutoring group views
urlpatterns += [
    url(r'^groupe/(?P<pk>\d+)/$', views.TutoringGroupDetailView.as_view(),
        name='tutoringgroup-detail'),
    url(r'^groupes/$', views.TutoringGroupListView.as_view(),
        name='tutoringgroups'),
]
