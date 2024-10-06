from django import forms
from django.forms import ModelForm # A form that feeds data to one of our models.
from .models import Round, RoundStats
from mainapp.models import Player
from mainapp.models import Course, Tee
from django.contrib.auth.models import User

class RoundForm(ModelForm):
	course = forms.ModelChoiceField(queryset=Course.objects.all(), label='Course Played',
		widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Course'}))
	tee_name = forms.ModelChoiceField(queryset=Tee.objects.none(), label='Select Tee',
		widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Tee'}))

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super().__init__(*args, **kwargs)
		if 'course' in self.data:
			try:
				course_id = int(self.data.get('course'))
				self.fields['tee_name'].queryset = Tee.objects.filter(course_id=course_id).order_by('tee_name')
			except (ValueError, TypeError):
				pass
		elif self.instance.pk:
			self.fields['tee_name'].queryset = Tee.objects.filter(course_id=self.instance.course_id).order_by('tee_name')

	def save(self, commit=True):
		instance = super().save(commit=False)
		if self.user:
			instance.player = self.user
		if commit:
			instance.save()
		return instance

	class Meta:
		model = Round
		fields = ('course', 'tee_name', 'date_played', 'round_type', 'weather', 'wind', 'comments')
		labels = {
			'course': 'Course Played',
			'tee_name': 'Tee Played',
			'date_played': 'Date Played',
			'round_type': 'Round Type',
			'weather': 'Weather',
			'wind': 'Wind',
			'comments': 'Comments',
		}
		widgets = {
			'date_played': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Select date of round'}),
			'round_type': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select round type'}),
			'weather': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select weather'}),
			'wind': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select wind'}),
			'comments': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter round comments', 'rows': 2}),
		}

# class RoundForm(ModelForm):
# 	course = forms.ModelChoiceField(queryset=Course.objects.all(), label='Course Played',
# 		widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Course'}))
# 	tee_name = forms.ModelChoiceField(queryset=Tee.objects.none(), label='Select Tee',
# 		widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Tee'}))
	
# 	def __init__(self, *args, **kwargs):
# 		super().__init__(*args, **kwargs)
# 		if 'course' in self.data:
# 			try:
# 				course_id = int(self.data.get('course'))
# 				self.fields['tee_name'].queryset = Tee.objects.filter(course_id=course_id).order_by('tee_name')
# 			except (ValueError, TypeError):
# 				pass
# 		elif self.instance.pk: # added due to copilot suggestion.
# 			self.fields['tee_name'].queryset = Tee.objects.filter(course_id=self.instance.course_id).order_by('tee_name')


# 	class Meta:
# 		model = Round
# 		fields = ('course', 'tee_name', 'date_played', 'round_type', 'weather', 'wind', 'comments') # Removed 'player' as will be set to logged in user.

# 		labels = {
# 			'course': 'Course Played',
# 			'tee_option': 'Tee Played',
# 			'date_played': 'Date Played',
# 			'round_type': 'Round Type',
# 			'weather': 'Weather',
# 			'comments': 'Comments',
# 		}

# 		widgets = {
# 			# 'player': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Select player'}), E Removed, will be logged in user.
# 			#'course': forms.ModelChoiceField(queryset=Course.objects.all(), label='Course Played', attrs={'class':'form-control', 'placeholder': 'Select course'}),
# 			#'tee_option': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Select tee option'}),
# 			'date_played': forms.DateInput(attrs={'class':'form-control', 'type': 'date', 'placeholder': 'Select date of round'}),
# 			'round_type': forms.Select(attrs={'class':'form-control', 'placeholder': 'Select round type'}),
# 			#'round_type': forms.RadioSelect(attrs={'class': 'custom-radio'})
# 			'weather': forms.Select(attrs={'class':'form-control', 'placeholder': 'Select weather'}),
# 			'wind': forms.Select(attrs={'class':'form-control', 'placeholder': 'Select wind'}),
# 			'comments': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Enter round comments', 'rows': 2}),
# 		}


class RoundStatsForm(forms.ModelForm):
	#green = forms.ChoiceField(choices=RoundStats.GREEN_CHOICES, widget=forms.RadioSelect())
	# number = forms.IntegerField(label='Score', initial=4, 
	# 	widget=forms.NumberInput(attrs={'id': 'id_score'}))

	#score = forms.IntegerField(initial='hole.par')

	class Meta:
		model = RoundStats
		fields = [
			'round_number',
			'hole_number',
			'par',
			'score',
			'fairway',
			'drivedistance',
			'green',
			'putts',
			'firstputtdistance',
			'updown',
			'sandsave',
			'penalties'
		]
		
		labels = {
			'fairway': 'Fairway',
			'drivedistance': 'Drive Distance:',
			'green': 'Green',
			'putts': 'Putts',
			'firstputtdistance': 'First Putt Distance',
			'updown': 'Up/Down',
			'sandsave': 'Sand Save',
			'penalties': 'Penalties',
		}

		widgets = {
            'score': forms.NumberInput(attrs={
                'class': 'number-input',
                #'id': 'number-input',
                'min': '1',
                'max': '20',
                #'style': 'border-bottom: 2px solid #000; border-left: none; border-right: none; border-top: none;'
            }),
            'drivedistance': forms.NumberInput(attrs={
                'class': 'custom-numeric-input-dd',
                'id': 'custom-numeric-input-dd',
                'min': '-1',
                'max': '400',
                'style': 'border-bottom: 2px solid #000; border-left: none; border-right: none; border-top: none;'
            }),
            'firstputtdistance': forms.NumberInput(attrs={
                'class': 'custom-numeric-input-fp',
                'id': 'custom-numeric-input-fp',
                'min': '-1',
                'max': '200',
                'style': 'border-bottom: 2px solid #000; border-left: none; border-right: none; border-top: none;'
            }),
            'penalties': forms.NumberInput(attrs={
                #'class': 'custom-numeric-input-fp',
                'id': 'id_penalties',
                # 'min': '0',
                # 'max': '200',
                # 'style': 'border-bottom: 2px solid #000; border-left: none; border-right: none; border-top: none;'
            }),
        }


	# def __init__(self, *args, **kwargs):
	#         super(RoundStatsForm, self).__init__(*args, **kwargs)
	#         self.fields['round'].initial = round
	#         self.fields['hole_number'].initial = hole_number
	#         self.fields['par'].initial = hole.par
	#         self.fields['round'].widget = forms.HiddenInput()
	#         self.fields['hole_number'].widget = forms.HiddenInput()
	#         self.fields['par'].widget = forms.HiddenInput()


	# def __init__(self, *args, **kwargs):
	# 	par = kwargs.pop('par', None)
	# 	super(RoundStatsForm, self).__init__(*args, **kwargs)
	# 	if par is not None:
	# 		self.fields['score'].initial = par


class StatsTestForm(ModelForm):
	class Meta:
		model = RoundStats
		fields = ['score', 'fairway', 'drivedistance', 'green', 'putts', 'firstputtdistance', 'updown', 'sandsave', 'penalties']
		labels = {
			'score': 'Score',
			'fairway': 'Fairway',
			'drivedistance': 'Drive Distance (metres)',
			'green': 'Green',
			'putts': '', # Don't need label as doing this with javascript on the page.
			'firstputtdistance': 'First Putt Distance (feet)',
			'updown': 'Up/Down',
			'sandsave': 'Sand Save',
			'penalties': '', # Don't need label as doing this with javascript on the page.
		}
		widgets = {
            'score': forms.NumberInput(attrs={
                'class': 'custom-numeric-input-score',
                'id': 'id_score',
                'min': '0',
                'max': '100',
                'style': 'border-bottom: 2px solid #000; border-left: none; border-right: none; border-top: none; text-align: center; width: 100px; height: 60px; font-size: 30px; font-weight: semibold;'
            }),
			'drivedistance': forms.NumberInput(attrs={
                'class': 'custom-numeric-input-dd',
                'id': 'custom-numeric-input-dd',
                'min': '-1',
                'max': '400',
                'style': 'border-bottom: 2px solid #000; border-left: none; border-right: none; border-top: none;'
            }),
            'firstputtdistance': forms.NumberInput(attrs={
                'class': 'custom-numeric-input-fp',
                'id': 'custom-numeric-input-fp',
                'min': '-1',
                'max': '200',
                'style': 'border-bottom: 2px solid #000; border-left: none; border-right: none; border-top: none;'
            }),
		}

