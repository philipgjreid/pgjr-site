from django.db import models
from django.contrib.auth.models import User
from mainapp.models import Course, Tee, Hole, Player

class Round(models.Model):
	ROUND_TYPE_CHOICES = [
			('regular', 'Regular'),
			('practice', 'Practice'),
			('tournament', 'Tournament'),
		]

	WEATHER_CHOICES = [
			('sunny', 'Sunny'),
			('overcast', 'Overcast'),
			('rain', 'Rain'),
		]

	WIND_CHOICES = [
			('nowind', 'No Wind'),
			('lightwind', 'Light Wind'),
			('strongwind', 'Strong Wind'),
		]

	player = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
	course = models.ForeignKey(Course, on_delete=models.PROTECT, blank=True, null=True)
	tee_name = models.ForeignKey(Tee, on_delete=models.PROTECT, blank=True, null=True)
	date_played = models.DateField(blank=True, null=True)
	round_type = models.CharField(max_length=30, choices=ROUND_TYPE_CHOICES, blank=True, null=True)
	weather = models.CharField(max_length=50, choices=WEATHER_CHOICES, blank=True, null=True)
	wind = models.CharField(max_length=50, choices=WIND_CHOICES, blank=True, null=True)
	comments = models.CharField(max_length=300, blank=True, null=True)

	def __str__(self):
		return f'Round on {self.date_played} {self.course.name if self.course else "Unknown Course"}'

class RoundStats(models.Model):
	FAIRWAY_CHOICES = [
			('wayleft', 'Way Left'),
			('left', 'Left'),
			('hit', 'Hit'),
			('right', 'Way Left'),
			('wayright', 'Way Right'),
			('na', 'na')
		]

	GREEN_CHOICES = [
			('longleft', 'Long Left'),
			('long', 'Long'),
			('longright', 'Long Right'),
			('left', 'Left'),
			('hit', 'Hit'),
			('right', 'Right'),
			('shortleft', 'Short Left'),
			('short', 'Short'),
			('shortright', 'Short Right'),
			('notreach', 'Could Not Reach'),
			('na', 'na')
		]

	UPDOWN_CHOICES = [
			('yes', 'Yes'),
			('no', 'No'),
			('na', 'na')
		]

	SANDSAVE_CHOICES = [
			('yes', 'Yes'),
			('no', 'No'),
			('na', 'na')
		]

	round_number = models.ForeignKey(Round, on_delete=models.CASCADE, related_name='round_stats')
	hole_number = models.ForeignKey(Hole, on_delete=models.PROTECT, related_name='round_stats')
	par = models.IntegerField()
	score = models.IntegerField()
	fairway = models.CharField(max_length=50, choices=FAIRWAY_CHOICES, blank=True, null=True)
	drivedistance = models.IntegerField(blank=True, null=True)
	green = models.CharField(max_length=50, choices=GREEN_CHOICES, blank=True, null=True)
	putts = models.IntegerField(blank=True, null=True)
	firstputtdistance = models.IntegerField(blank=True, null=True)
	updown = models.CharField(max_length=50, choices=UPDOWN_CHOICES, blank=True, null=True)
	sandsave = models.CharField(max_length=50, choices=SANDSAVE_CHOICES, blank=True, null=True)
	penalties = models.IntegerField(blank=True, null=True)

	def __str__(self):
		return f'Stats for Hole {self.hole_number.hole_number} - Par {self.par}'
