from django.contrib import admin
from .models import Visit, Arm

class VisitAdmin(admin.ModelAdmin):
	list_display = ('date', 'arm', 'reward', 'expired', 'deducted')

class ArmAdmin(admin.ModelAdmin):
	list_display = ('number', 'count', 'av_reward', 'prob')

admin.site.register(Visit, VisitAdmin)
admin.site.register(Arm, ArmAdmin)