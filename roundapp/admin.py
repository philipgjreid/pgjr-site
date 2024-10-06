from django.contrib import admin
from .models import Round, RoundStats

#admin.site.register(Round)
@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
	list_display = ('id', 'player', 'course', 'tee_name', 'date_played', 'round_type', 'weather', 'wind', 'comments')
	ordering = ('-id',)
	search_fields = ('course', 'player')

#admin.site.register(RoundStats)
@admin.register(RoundStats)
class RoundStatsAdmin(admin.ModelAdmin):
	list_display = ('id', 'round_number_id', 'round_number', 'hole_number', 'par', 'score', 'fairway', 'drivedistance', 'green', 'putts', 'firstputtdistance', 'updown', 'sandsave', 'penalties')
	ordering = ('-id',)
	search_fields = ('par', 'score')
