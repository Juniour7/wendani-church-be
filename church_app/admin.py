from django.contrib import admin
from .models import PrayerReqestForm, BaptismRequestForm, DedicationForm, MembershipTransferForm, Events, BenevolenceForm, ContactForm, Announcements

class AdminModel(admin.ModelAdmin):
    list_display = '__all__'
    

# Register your models here.
admin.site.register(PrayerReqestForm)
admin.site.register(BaptismRequestForm)
admin.site.register(DedicationForm)
admin.site.register(MembershipTransferForm)
admin.site.register(Events)
admin.site.register(BenevolenceForm)
admin.site.register(ContactForm)
admin.site.register(Announcements)