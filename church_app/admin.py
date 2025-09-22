from django.contrib import admin
from .models import PrayerReqestForm, BaptismRequestForm, DedicationForm, MembershipTransferForm, Events, BenevolenceForm, ContactForm, Announcements

# Register your models here.
admin.register(PrayerReqestForm)
admin.register(BaptismRequestForm)
admin.register(DedicationForm)
admin.register(MembershipTransferForm)
admin.register(Events)
admin.register(BenevolenceForm)
admin.register(ContactForm)
admin.register(Announcements)