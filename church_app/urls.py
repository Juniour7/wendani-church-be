from django.urls import path
from . import views

# Church App Urls
urlpatterns = [
    # Prayer endpoints
    path('prayers/', views.prayer_form_submit_view, name='prayer_form_submit'),
    path('prayers/list/', views.prayer_form_list_view, name='prayer_form_list'),

    # Baptism endpoints
    path('baptisms/', views.baptism_form_submit_view, name='baptism_form_submit'),
    path('baptisms/list/', views.baptism_form_list_view, name='baptism_form_list'),

    # Dedication endpoints
    path('dedications/', views.dedication_form_submit_view, name='dedication_form_submit'),
    path('dedications/list/', views.dedication_form_list_view, name='dedication_form_list'),

    # Memebership transfer endpoints
    path('membership/', views.membership_submit_view, name='membership-form-submit'),
    path('membership/list/', views.membership_form_view, name='membership-form-lidt'),

    # Contact Form Submission
    path('contact/', views.contact_form_submit, name='contact-form-submit'),
    path('contact/list/', views.contact_form_view, name='contact-form-list'),

    # Events Handling endpoints
    path('events/', views.events_submit, name='events-create'), # update, post and delete
    path('events/list/', views.events_list_view, name='events-list'), # Events list view
    path('events/<int:pk>/', views.events_list_view, name='events-ddetail'), # Events detail view

    # Announcement File ENDPOINTS
    path('announcements/', views.announcements_submit, name='annoucemnets-create'),
    path('annoncements/list/', views.announcements_list_view, name='announcements-list')
]