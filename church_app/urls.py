from django.urls import path,include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('prayers', views.PrayerRequestViewSet, basename='prayers')
router.register('baptism', views.BaptismRequestViewSet, basename='bapstism')
router.register('dedication', views.DedicationViewSet, basename='dedication')

# Church App Urls
urlpatterns = [
    # Prayer endpoints
    path('', include(router.urls)),

    # Memebership transfer endpoints
    path('membership/', views.membership_submit_view, name='membership-form-submit'),
    path('membership/list/', views.membership_form_view, name='membership-form-lidt'),

    # Contact Form Submission
    path('contact/', views.contact_form_submit, name='contact-form-submit'),
    path('contact/list/', views.contact_form_view, name='contact-form-list'),

    # Benevolence form handling endpoints
    path('benevolence/', views.benevolence_list_view, name='benevolence-list'),
    path('benevolence/submit/', views.benevolence_submit_view, name='benevolence-submit'),

    # Events Handling endpoints
    path('events/', views.events_submit, name='events-create'), # update, post and delete
    path('events/list/', views.events_list_view, name='events-list'), # Events list view
    path('events/<int:pk>/', views.events_list_view, name='events-ddetail'), # Events detail view

    # Announcement File ENDPOINTS
    path('announcements/', views.AnnouncementsListCreateView.as_view(), name='annoucemnets-create'),
    path('announcements/<int:pk>/', views.AnnouncementsDetailView.as_view(), name='announcements-detail'),
]