from django.contrib import admin
from .resource import *

admin.site.register(User, User_Admin)
admin.site.register(Feed, Feed_Admin)
admin.site.register(Threat, Threat_Admin)
admin.site.register(ThreatLog, ThreatLog_Admin)