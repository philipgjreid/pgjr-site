from django.db import models

class Course(models.Model):
	name = models.CharField(max_length=100)
	total_par = models.IntegerField(null=True)

	def __str__(self):
		return self.name

class Tee(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tees', blank=True, null=True)
	tee_name = models.CharField(max_length=50)
	course_length = models.CharField(max_length=10, blank=True, null=True)

	def __str__(self):
		return self.tee_name
		#return f'{self.tee_name} - {self.course.name}'


class Hole(models.Model):
	par_choices = [(3, 'Par 3'),(4, 'Par 4'),(5, 'Par 5')]
	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='holes', blank=True, null=True)
	hole_number = models.IntegerField()
	par = models.IntegerField(choices=par_choices)

	def __str__(self):
		return f'{self.hole_number}'
		#return f'{self.course} - Hole {self.hole_number} - Par {self.par}'


# Won't need this as the Django User will replace this, unless I want special details (TBC?).
class Player(models.Model):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    home_course = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    handicap = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
