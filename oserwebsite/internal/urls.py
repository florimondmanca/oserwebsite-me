"""Internal website urls."""

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
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
