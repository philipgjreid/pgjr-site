from django.contrib import admin
from .models import Course, Tee, Hole, Player

admin.site.register(Course)

#admin.site.register(Tee)
@admin.register(Tee)
class TeeAdmin(admin.ModelAdmin):
	list_display = ('course', 'tee_name', 'course_length')
	ordering = ('course', 'tee_name', 'course_length')
	search_fields = ('course', 'tee_name')

#admin.site.register(Hole)
@admin.register(Hole)
class HoleAdmin(admin.ModelAdmin):
	list_display = ('course', 'hole_number', 'par')
	ordering = ('course', 'hole_number', 'par')
	search_fields = ('course',)

admin.site.register(Player)
