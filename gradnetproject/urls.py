"""gradnetproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from gradnet.views import (CountryListView, AlumniListView, AlumniDetailView, ProgramListView, UniversityListView, AlumniSignUp, login_view, logout_view, alumni_dashboard, services_view, services_per_alumni_view, send_message_to_alumni, faq_view, message_view, student_dashboard, about_view, contact_view, roadmap_view, AlumniStoriesListView, AlumniStoryDetailView, videos_view)

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # program listing
    url(r'^$', ProgramListView.as_view(), name='program-list'),

    # country listing (program-wise)
    url(r'^program/(?P<program_slug>[-\w]+)/country/$', CountryListView.as_view(), name='country-list'),

    # university listing (program-wise and country-wise)
    url(r'^program/(?P<program_slug>[-\w]+)/country/(?P<country_slug>[-\w]+)/university/$',
        UniversityListView.as_view(), name='university-list'),

    # alumni listing (program and university-wise)
    url(r'^program/(?P<program_slug>[-\w]+)/university/(?P<university_slug>[-\w]+)/alumni/$', AlumniListView.as_view(),
        name='alumni-list'),

    # alumni sign up page
    url(r'^alumni/signup/$', AlumniSignUp.as_view() , name='alumni-signup'),

    # alumni details page
    url(r'^alumni/(?P<slug>[-\w]+)/$', AlumniDetailView.as_view(), name='alumni-detail'),

    # login
    url(r'^login$', login_view , name='login'),

    # logout
    url(r'^logout$', logout_view, name='logout'),

    # alumni-dashboard
    url(r'^alumni-dashboard$', alumni_dashboard, name='alumni-dashboard'),

    # student-dashboard
    url(r'^student-dashboard$', student_dashboard, name='student-dashboard'),

    # services
    url(r'^services$', services_view, name='services'),

    # services per alumni
    url(r'^alumni/(?P<slug>[-\w]+)/services$', services_per_alumni_view, name='services-per-alumni'),

    # message to alumni
    url(r'^alumni/(?P<slug>[-\w]+)/message$', send_message_to_alumni, name='message-to-alumni'),

    # message
    url(r'^message$', message_view, name='message'),

    # faq
    url(r'^faq$', faq_view , name='faq'),

    # about
    url(r'^about$', about_view, name='about'),

    # roadmap
    url(r'^roadmap$', roadmap_view, name='roadmap'),

    # contact
    url(r'^contact$', contact_view, name='contact'),

    # alumni-stories
    url(r'^alumni-stories', AlumniStoriesListView.as_view(), name='alumni-stories'),

    # alumni-story-detail-view
    url(r'^alumni-story/(?P<pk>\d+)/$', AlumniStoryDetailView.as_view(), name='alumni-story-detail'),

    # contact
    url(r'^videos', videos_view, name='videos'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)