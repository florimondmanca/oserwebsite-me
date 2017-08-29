"""Internal website urls."""

from django.conf.urls import url
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    url(r'^$', views.BrandView.as_view(), name='brand'),
    url(r'^index/$', views.IndexView.as_view(), name='index'),
    url(r'^faq/$', TemplateView.as_view(template_name='internal/faq.html'),
        name='faq'),
]

# Tutoree detail view
urlpatterns += [
    url(r'^tutore/(?P<pk>\d+)/$', views.TutoreeDetailView.as_view(),
        name='tutoree-detail'),
]

# Tutor detail view
urlpatterns += [
    url(r'^tuteur/(?P<pk>\d+)/$', views.TutorDetailView.as_view(),
        name='tutor-detail'),
]

# HighSchool detail view
urlpatterns += [
    url(r'^lycee/(?P<pk>\d+)/$', views.HighSchoolDetailView.as_view(),
        name='highschool-detail'),
]

# Tutoring group detail view
# HighSchool detail view
urlpatterns += [
    url(r'^groupe/(?P<pk>\d+)/$', views.TutoringGroupDetailView.as_view(),
        name='tutoringgroup-detail'),
]
