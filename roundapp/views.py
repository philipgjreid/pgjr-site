from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RoundForm, RoundStatsForm
from mainapp.models import Course, Tee, Hole, Player
from .models import Round, RoundStats
from .forms import StatsTestForm

from django.core.serializers.json import DjangoJSONEncoder
import json
import pandas as pd
import csv


# Test to check for incomplete rounds.
def check_incomplete_rounds(request):	
	if request.user.is_authenticated:
		incomplete_round = Round.objects.filter(player_id=request.user.id, is_complete=False).first()
		# messages.success(request, ("You have an incomplete round..."))
		if incomplete_round:
			# messages.success(request, ("To continue updating round or delete..."))
			return redirect('continue-round', round_number_id=incomplete_round.id)
			# return redirect('continue-round', round_id=incomplete_round.id)
		return redirect('golf-home')
	return None


def continue_round(request, round_number_id):
	round_instance = get_object_or_404(Round, id=round_number_id)
	if request.method =="POST":
		if 'continue'in request.POST:
			return redirect('stats-test', round_number_id=round_number_id, hole_number=1)
		elif 'delete' in request.POST:
			round_instance.delete()
			return redirect('golf-home')

	return render(request, 'roundapp/continue_round.html', {'round_instance': round_instance})

	# if request.method == 'POST':
	# 	if 'continue' in request.POST:
	# 		return redirect('enter_hole_stats', round_id=round.id)
	# 	elif 'delete' in request.POST:
	# 		round.delete()
	# 		return redirect('start_new_round')
	# return render(request, 'continue_round.html', {'round': round})





# Testing how to allow user values to show in summary page.

ROUND_TYPE_CHOICES = {
	'regular': 'Regular',
	'practice': 'Practice',
	'tournament': 'Tournament'
}

WEATHER_CHOICES = {
	'sunny': 'Sunny',
	'overcast': 'Overcast',
	'rain': 'Rain'
}

WIND_CHOICES = {
	'nowind': 'No Wind',
	'lightwind': 'Light Wind',
	'strongwind': 'Strong Wind'
}

GREEN_CHOICES = {
    'longleft': 'Long Left',
    'long': 'Long',
    'longright': 'Long Right',
    'left': 'Left',
    'hit': 'Hit',
    'right': 'Right',
    'shortleft': 'Short Left',
    'short': 'Short',
    'shortright': 'Short Right',
    'notreach': 'Could Not Reach',
    'na': 'na'
}

FAIRWAY_CHOICES = {
    'wayleft': 'Way Left',
    'left': 'Left',
    'hit': 'Hit',
    'right': 'Right',
    'wayright': 'Way Right',
    'na': 'na'
}

UPDOWN_CHOICES = {
    'yes': 'Yes',
    'no': 'No',
    'na': 'na'
}

SANDSAVE_CHOICES = {
    'yes': 'Yes',
    'no': 'No',
    'na': 'na'
}


def stats_test(request, round_number_id=None, hole_number=1):
	submitted = False
	round_instance = get_object_or_404(Round, id=round_number_id)
	hole_instance = get_object_or_404(Hole, course=round_instance.course, hole_number=hole_number)
	#messages.success(request, f'Request Method: {request.method}')

	if request.method == "POST":
		form = StatsTestForm(request.POST)
		if form.is_valid():
			#Check if round/hole entry already exists.
			try:
				updated_stats = RoundStats.objects.get(round_number=round_instance, hole_number=hole_instance)
				form = StatsTestForm(request.POST, instance=updated_stats)
				form.save()
				#messages.success(request, 'Existing data updated!')

			except RoundStats.DoesNotExist:
				stats = form.save(commit=False)
				# save the round id, hole number, and par as they are set already.
				stats.round_number = round_instance
				stats.hole_number = hole_instance
				stats.par = hole_instance.par
				stats.save()
				# messages.success(request, 'New data created!')

			if 'next' in request.POST:
				hole_number += 1
				par=hole_instance.par # This is for testing the par value only.
				#messages.success(request, f'Next worked!! Moving to hole {hole_number} with par {par}!')
				if hole_number > 3: #18: # Changed to 3 for testing purposes.
					#messages.success(request, f'Finishing round worked!! Moving to summary page!')

					# Retrieve the relevant model instances
					round_instance = get_object_or_404(Round, id=round_number_id)
					# messages.success(request, f'Round_number_id = {round_number_id}; Round_instance = {round_instance}')
					rnd = Round.objects.get(id=round_number_id)
					rnd.is_complete = True
					rnd.save(update_fields=['is_complete'])
					# messages.success(request, f'Round is_complete = {rnd.is_complete}')

					stats = RoundStats.objects.filter(round_number=round_instance)
					# messages.success(request, f'Update round #{round_number_id}')

					# Loop through the instances and update the fields based on your conditions
					for stat in stats:
						if stat.drivedistance == None:
							stat.drivedistance = -1
						if stat.firstputtdistance == None:
							stat.firstputtdistance = -1
						# Save the updated instance
						stat.save()

					return redirect('round-summary', round_number_id=round_number_id)
				return redirect('stats-test', round_number_id=round_number_id, hole_number=hole_number)
			if 'back' in request.POST:
				hole_number -= 1
				if hole_number < 1:
 					hole_number = 1
				#messages.success(request, f'Back worked!! Moving to hole {hole_number}!')
				return redirect('stats-test', round_number_id=round_number_id, hole_number=hole_number)
	else:
		#Retrieve existing data for the current hole
		try:
			previous_stats = RoundStats.objects.get(round_number=round_instance, hole_number=hole_instance)
			form = StatsTestForm(instance=previous_stats)
			#messages.success(request, 'Previous data retrieved.')
		
		except RoundStats.DoesNotExist:
			form = StatsTestForm(initial={'score': hole_instance.par})
			#messages.success(request, f'Blank form loaded - request type {request.method}!')

		# if 'submitted' in request.GET:
		# 	submitted = True

	context = {
		'form': form,
		'submitted': submitted,
		'round_number': round_instance,
		'hole': hole_instance,
		'hole_number': hole_number,
		#'next_hole_number': hole_number + 1 if hole_number < 18 else None,
		# 'previous_hole_number': hole_number - 1 if hole_number > 1 else None,
	}
	return render(request, 'roundapp/stats_test.html', context)


# def round_stats(request, round_number_id=None, hole_number=1):
# 	round_instance = get_object_or_404(Round, id=round_number_id)
# 	hole_instance = get_object_or_404(Hole, course=round_instance.course, hole_number=hole_number)
# 	messages.success(request, f"Hole stats form submitted. Request method {request.method}")
	
# 	if request.method == "POST":
# 		form = RoundStatsForm(request.POST)
# 		if form.is_valid():
# 			messages.success(request, 'Form submitted successfully!')
# 			#Check if round/hole entry already exists.
# 			try:
# 				round_stats = RoundStats.objects.get(round_number=round_instance, hole_number=hole_instance)
# 				form = RoundStatsForm(request.POST, instance=round_stats)
# 				form.save()
# 			except RoundStats.DoesNotExist:
# 				round_stats = form.save(commit=False)
# 				round_stats.round_number = round_instance
# 				round_stats.hole_number = hole_instance
# 				round_stats.par = hole_instance.par

# 				round_stats.save()
# 				print(round_stats)
# 				print(form)

#             # Determine the next or previous hole number based on the button clicked
# 			if 'next' in request.POST:
# 				next_hole_number = hole_number + 1
# 				#console.log(f"New hole is:" + hole_number)
# 				messages.success(request, 'Moving to next hole!')
# 				if next_hole_number > 18:
# 					return redirect('round-summary', round_number_id=round_number_id)
# 				return redirect('round-stats', round_number_id=round_number_id, hole_number=next_hole_number)
# 			elif 'back' in request.POST:
# 				previous_hole_number = hole_number - 1
# 				messages.success(request, 'Moving to previous hole!')
# 				if previous_hole_number < 1:
# 					previous_hole_number = 1
# 				return redirect('round-stats', round_number_id=round_number_id, hole_number=previous_hole_number)
# 	else:
#         # Retrieve existing data for the current hole
# 		try:
# 			round_stats = RoundStats.objects.get(round_number=round_instance, hole_number=hole_instance)
# 			form = RoundStatsForm(instance=round_stats)
# 			messages.success(request, 'Existing data retrieved.')
# 		except RoundStats.DoesNotExist:
# 			form = RoundStatsForm()
# 			messages.success(request, 'Blank form loaded!')

# 	context = {
# 		'form': form,
# 		'round_number': round_instance,
# 		'hole': hole_instance,
# 		'hole_number': hole_number,
# 		'next_hole_number': hole_number + 1 if hole_number < 18 else None,
# 		'previous_hole_number': hole_number - 1 if hole_number > 1 else None,

# 	}
# 	return render(request, 'roundapp/round_stats.html', context)



def golf_home(request):
	return render(request, 'roundapp/golf_home.html', {})

def load_tees(request):
	course_id = request.GET.get('course_id')
	tees = Tee.objects.filter(course_id=course_id).order_by('tee_name')
	return JsonResponse(list(tees.values('id', 'tee_name')), safe=False)

def new_round(request):
	submitted = False
	if request.method == "POST":
		form = RoundForm(request.POST, user=request.user)
		if form.is_valid():
			# This is where i need to delay the commit and add: round.player = request.user after changing model to point to User instead of Player.
			new_round = form.save(commit=False)
			# # save the round id, hole number, and par as they are set already.
			# new_round.player = request.user
			new_round.save()
			# new_round = form.save()
			#form.save()
			#messages.success(request, 'New round data created!')

			# cleaned_data = form.cleaned_data
			# cleaned_data['player'] = cleaned_data['player'].full_name
			# cleaned_data['date_played'] = cleaned_data['date_played'].strftime('%Y-%m-%d')
			# cleaned_data['course'] = cleaned_data['course'].id
			# cleaned_data['tee_name'] = cleaned_data['tee_name'].id

			# request.session['form_data'] = json.dumps(cleaned_data, cls=DjangoJSONEncoder) #form.cleaned_data
			# print(form.cleaned_data) # for testing.
			#return redirect('round-stats', round_id=new_round.id, hole_number=1) # Draft from copilot.
			return redirect('stats-test', round_number_id=new_round.id, hole_number=1)
			# #return HttpResponseRedirect('/round_details?submitted=True') #redirect('success_url')
	else:
		# To put incomplete round check here before getting new form.
		incomplete_round = Round.objects.filter(player_id=request.user.id, is_complete=False).first()
		# messages.success(request, ("You have an incomplete round..."))
		if incomplete_round:			
			return redirect('continue-round', round_number_id=incomplete_round.id)

		form = RoundForm(user=request.user)
		if 'submitted' in request.GET:
			submitted = True
	return render(request, 'roundapp/new_round.html', {'form': form, 'submitted': submitted})



def round_statsZ(request):
    if request.method == "POST":
        round_number_id = request.POST.get('round_number')
        hole_number_id = request.POST.get('hole_number')
        par = request.POST.get('par')
        score = request.POST.get('score')
        fairway = request.POST.get('fairway')
        # Add other fields similarly

        try:
            round_number = Round.objects.get(id=round_number_id)
            hole_number = Hole.objects.get(id=hole_number_id)

            new_round_stats = RoundStats(
                round_number=round_number,
                hole_number=hole_number,
                par=par,
                score=score,
                fairway=fairway,
                # Add other fields similarly
            )
            new_round_stats.save()
            messages.success(request, 'Round stats submitted successfully!')
            return redirect('success_page')  # Replace with your success page URL
        except Round.DoesNotExist:
            messages.error(request, 'Invalid round number.')
        except Hole.DoesNotExist:
            messages.error(request, 'Invalid hole number.')
        except ValueError:
            messages.error(request, 'Invalid input. Please check your data.')

    return render(request, 'roundapp/new_round_stats.html')



def round_statsX(request, round_number_id=None, hole_number=1):
	if request.method == "POST":
		#player = request.POST.get('player').strip()
		hole_number = hole_number
		score = request.POST.get('score').strip()
		par = 4

		# Basic validation
		if not score:
			messages.error(request, 'Score is required.')
		else:
			new_round = RoundStats(score=score, par=par, hole_number=hole_number)
			new_round.save()
			messages.success(request, 'New hole data submitted successfully!')
			return redirect('round-stats', round)

		if 'next' in request.POST:
			next_hole_number = hole_number + 1
			#console.log(f"New hole is:" + hole_number)
			messages.success(request, 'Moving to next hole!')
			if next_hole_number > 18:
				return redirect('round-summary', round_number_id=round_number_id)
			return redirect('round-stats', round_number_id=round_number_id, hole_number=next_hole_number)
		elif 'back' in request.POST:
			previous_hole_number = hole_number - 1
			messages.success(request, 'Moving to previous hole!')
			if previous_hole_number < 1:
				previous_hole_number = 1
			return redirect('round-stats', round_number_id=round_number_id, hole_number=previous_hole_number)
	return render(request, 'roundapp/round_stats.html',{})

def round_statsXX(request, round_number_id=None, hole_number=1):
	round_instance = get_object_or_404(Round, id=round_number_id)
	hole_instance = get_object_or_404(Hole, course=round_instance.course, hole_number=hole_number)
	messages.success(request, f"Hole stats form submitted. Request method {request.method}")
	
	if request.method == "POST":
		#form = RoundStatsForm(request.POST)
		round_number = round_instance
		hole_number = hole_instance
		par = hole_instance.par
		score = request.POST.get('score')

		round_stats = Round(
			round_number=round_number,
			hole_number=hole_number,
			par=par,
			score=score
			)
		round_stats.save()

	# 	if form.is_valid():
	# 		messages.success(request, 'Form submitted successfully!')
	# 		#Check if round/hole entry already exists.
	# 		try:
	# 			round_stats = RoundStats.objects.get(round_number=round_instance, hole_number=hole_instance)
	# 			form = RoundStatsForm(request.POST, instance=round_stats)
	# 			form.save()
	# 		except RoundStats.DoesNotExist:
	# 			round_stats = form.save(commit=False)
	# 			round_stats.round_number = round_instance
	# 			round_stats.hole_number = hole_instance
	# 			round_stats.par = hole_instance.par
				
	# 			# fairway_value = request.POST.get('fairway_value')
	# 			# #dd_value = form.cleaned_data.get('drivedistance')
	# 			# dd_value = request.POST.get('drivedistance')
	# 			# green_value = request.POST.get('green_value')
	# 			# fp_value = request.POST.get('firstputtdistance')
	# 			# putts_value = request.POST.get('putts_value')
	# 			# updown_value = request.POST.get('updown_value')
	# 			# sandsave_value = request.POST.get('sandsave_value')
	# 			# penalties_value = request.POST.get('penalties_value')

	# 			# if not fairway_value:
	# 			# 	form.instance.fairway = "na"
	# 			# else:
	# 			# 	form.instance.fairway = fairway_value
				
	# 			# if not dd_value:
	# 			# 	dd_value = -1
	# 			# else:
	# 			# 	form.instance.drivedistance = dd_value

	# 			# form.instance.green = green_value
		
	# 			# if not putts_value:
	# 			# 	form.instance.putts = 2
	# 			# 	#form.add_error('putts', 'Please select how many putts.')
	# 			# else:
	# 			# 	form.instance.putts = putts_value
				
	# 			# if not updown_value:
	# 			# 	form.instance.updown = "na"
	# 			# else:
	# 			# 	form.instance.updown = updown_value
				
	# 			# if not sandsave_value:
	# 			# 	form.instance.sandsave = "na"
	# 			# else:
	# 			# 	form.instance.sandsave = sandsave_value
				
	# 			# if not penalties_value:
	# 			# 	form.instance.penalties = 0
	# 			# else:
	# 			# 	form.instance.penalties = penalties_value

	# 			round_stats.save()

    #         # Determine the next or previous hole number based on the button clicked
	# 		if 'next' in request.POST:
	# 			next_hole_number = hole_number + 1
	# 			#console.log(f"New hole is:" + hole_number)
	# 			messages.success(request, 'Moving to next hole!')
	# 			if next_hole_number > 18:
	# 				return redirect('round-summary', round_number_id=round_number_id)
	# 			return redirect('round-stats', round_number_id=round_number_id, hole_number=next_hole_number)
	# 		elif 'back' in request.POST:
	# 			previous_hole_number = hole_number - 1
	# 			messages.success(request, 'Moving to previous hole!')
	# 			if previous_hole_number < 1:
	# 				previous_hole_number = 1
	# 			return redirect('round-stats', round_number_id=round_number_id, hole_number=previous_hole_number)
	# else:
    #     # Retrieve existing data for the current hole
	# 	try:
	# 		round_stats = RoundStats.objects.get(round_number=round_instance, hole_number=hole_instance)
	# 		form = RoundStatsForm(instance=round_stats)
	# 		messages.success(request, 'Existing data retrieved.')
	# 	except RoundStats.DoesNotExist:
	# 		form = RoundStatsForm()
	# 		messages.success(request, 'Blank form loaded!')

	# context = {
	# 	'form': form,
	# 	'round_number': round_instance,
	# 	'hole': hole_instance,
	# 	'hole_number': hole_number,
	# 	'next_hole_number': hole_number + 1 if hole_number < 18 else None,
	# 	'previous_hole_number': hole_number - 1 if hole_number > 1 else None,

	# }
	return render(request, 'roundapp/round_stats.html')#, context)

# V1 - TO REPLACE WITH stats_test AS THAT VERSION WORKS.
def round_stats(request, round_number_id=None, hole_number=1):
	round_instance = get_object_or_404(Round, id=round_number_id)
	hole_instance = get_object_or_404(Hole, course=round_instance.course, hole_number=hole_number)
	messages.success(request, f"Hole stats form submitted. Request method {request.method}")
	
	if request.method == "POST":
		form = RoundStatsForm(request.POST)
		if form.is_valid():
			messages.success(request, 'Form submitted successfully!')
			#Check if round/hole entry already exists.
			try:
				round_stats = RoundStats.objects.get(round_number=round_instance, hole_number=hole_instance)
				form = RoundStatsForm(request.POST, instance=round_stats)
				form.save()
			except RoundStats.DoesNotExist:
				round_stats = form.save(commit=False)
				round_stats.round_number = round_instance
				round_stats.hole_number = hole_instance
				round_stats.par = hole_instance.par
				
				# fairway_value = request.POST.get('fairway_value')
				# #dd_value = form.cleaned_data.get('drivedistance')
				# dd_value = request.POST.get('drivedistance')
				# green_value = request.POST.get('green_value')
				# fp_value = request.POST.get('firstputtdistance')
				# putts_value = request.POST.get('putts_value')
				# updown_value = request.POST.get('updown_value')
				# sandsave_value = request.POST.get('sandsave_value')
				# penalties_value = request.POST.get('penalties_value')

				# if not fairway_value:
				# 	form.instance.fairway = "na"
				# else:
				# 	form.instance.fairway = fairway_value
				
				# if not dd_value:
				# 	dd_value = -1
				# else:
				# 	form.instance.drivedistance = dd_value

				# form.instance.green = green_value
		
				# if not putts_value:
				# 	form.instance.putts = 2
				# 	#form.add_error('putts', 'Please select how many putts.')
				# else:
				# 	form.instance.putts = putts_value
				
				# if not updown_value:
				# 	form.instance.updown = "na"
				# else:
				# 	form.instance.updown = updown_value
				
				# if not sandsave_value:
				# 	form.instance.sandsave = "na"
				# else:
				# 	form.instance.sandsave = sandsave_value
				
				# if not penalties_value:
				# 	form.instance.penalties = 0
				# else:
				# 	form.instance.penalties = penalties_value

				round_stats.save()
				print(round_stats)
				print(form)

            # Determine the next or previous hole number based on the button clicked
			if 'next' in request.POST:
				next_hole_number = hole_number + 1
				#console.log(f"New hole is:" + hole_number)
				messages.success(request, 'Moving to next hole!')
				if next_hole_number > 18:
					return redirect('round-summary', round_number_id=round_number_id)
				return redirect('round-stats', round_number_id=round_number_id, hole_number=next_hole_number)
			elif 'back' in request.POST:
				previous_hole_number = hole_number - 1
				messages.success(request, 'Moving to previous hole!')
				if previous_hole_number < 1:
					previous_hole_number = 1
				return redirect('round-stats', round_number_id=round_number_id, hole_number=previous_hole_number)
	else:
        # Retrieve existing data for the current hole
		try:
			round_stats = RoundStats.objects.get(round_number=round_instance, hole_number=hole_instance)
			form = RoundStatsForm(instance=round_stats)
			messages.success(request, 'Existing data retrieved.')
		except RoundStats.DoesNotExist:
			form = RoundStatsForm()
			messages.success(request, 'Blank form loaded!')

	context = {
		'form': form,
		'round_number': round_instance,
		'hole': hole_instance,
		'hole_number': hole_number,
		'next_hole_number': hole_number + 1 if hole_number < 18 else None,
		'previous_hole_number': hole_number - 1 if hole_number > 1 else None,

	}
	return render(request, 'roundapp/round_stats.html', context)

# 			next_hole_number = hole_number + 1
# 			if next_hole_number > 18:
# 				return redirect('round-summary', round_id=round_id)
# 			return redirect('round-stats',hole_number=next_hole_number) #round_id=round_id,
# 	else:
# 		form = RoundStatsForm()

# 	context = {
# 		'form': form,
# 		'round': round_instance,
# 		'hole': hole_instance,
# 		'hole_number': hole_number,
# 		'next_hole_number': hole_number + 1 if hole_number < 18 else None,
# 		'previous_hole_number': hole_number - 1 if hole_number > 1 else None,
# 	}
# 	return render(request, 'roundapp/round_stats.html', context)






# To consider this if i want to use temporary dataframes to hold round and stats data.
def new_round2(request):
	form = RoundForm(request.POST or None)

	if form.is_valid():
		initialise_dataframe(request)
		form_data = form.cleaned_data
		form_data['player'] = form_data['player'].id
		#form_data['player'] = form_data['player'].full_name
		form_data['course'] = form_data['course'].name
		form_data['tee_name'] = form_data['tee_name'].id
		form_data['date_played'] = form_data['date_played'].strftime('%Y-%m-%d')
		form_data['round_type'] = dict(Round.ROUND_TYPE_CHOICES).get(form_data['round_type'])
		form_data['weather'] = dict(Round.WEATHER_CHOICES).get(form_data['weather']) 
		form_data['wind'] = dict(Round.WIND_CHOICES).get(form_data['wind']) 
		temp_data = pd.DataFrame.from_dict(request.session['temp_data'])
		new_row = pd.DataFrame([form_data])
		temp_data = pd.concat([temp_data, new_row], ignore_index=True)
		request.session['temp_data'] = temp_data.to_dict('list')
		return redirect('review-data')
	return render(request, 'roundapp/new_round.html',{'form': form})
	#return redirect('round-stats', round_id=round_instances[-1].id, hole_number=1) 
	# round-stats needs to be rebuilt to not rely on the round model being updated.
	# To work out how to tell the round-stats page which course and hole to start on without the current structure.
	# Still need to confirm that all the dataframes can be collated and then saved at the end.


def initialise_dataframe(request):
	# if 'temp_data' not in request.session:
	request.session['temp_data'] = pd.DataFrame().to_dict('list')


WEATHER_CHOICES2 = [
    ('sunny', 'Sunny'),
    ('overcast', 'Overcast'),
    ('rain', 'Rain'),
]
weather_mapping = {display: value for value, display in WEATHER_CHOICES2}

# This is the alternate DataFrame process to handle guest data. Under development.
def save_round(request):
	temp_data = request.session.get('temp_data', {})
	if temp_data:
		df = pd.DataFrame.from_dict(temp_data)

		round_instances = []
		for index, row in df.iterrows():
			try:
				player = Player.objects.get(id=row['player'])
				course = Course.objects.get(name=row['course'])
				tee_name = Tee.objects.get(id=row['tee_name'])
				#round_type = dict(Round.ROUND_TYPE_CHOICES).get(form_data['round_type'])
				weather = weather_mapping.get(row['weather'], None)
				if weather is None:
					raise ValueError(f"Invalid weather option: {row['weather']}")

				round_instance = Round(
                    player=player, 
                    course=course, 
                    tee_name=tee_name,
                    date_played=row['date_played'],
                    round_type=row['round_type'],
                    weather=weather,
                    wind=row['wind'],
                    comments=row['comments'],
                    # Add other fields as necessary
                )
				round_instances.append(round_instance)
			except Player.DoesNotExist:
				print(f"Player with id {row['player']} does not exist!")
			except Course.DoesNotExist:
				print(f"Course with name {row['course']} does not exist!")
			except Tee.DoesNotExist:
				print(f"Tee with id {row['tee_name']} does not exist!")
			except Exception as e:
				print(f"An error occurred: {str(e)}")

        # Bulk create all round instances
		if round_instances:
			Round.objects.bulk_create(round_instances)

        # Clear the session data after saving
		request.session['temp_data'] = pd.DataFrame().to_dict('list')

        # Redirect to a success page or another appropriate page
		if round_instances:
			return redirect('round-stats', round_number_id=round_instances[-1].id, hole_number=1)

	return redirect('review-data')

	# 		form = RoundForm(row.to_dict())
	# 		if form.is_valid():
	# 			new_round = form.save()
	# 		else:
	# 			print(form.errors)
	# 		# new_round = Round.objects.create(
	# 		# 	player=row['player'],
	# 		# 	course=row['course'],
	# 		# 	tee_name=row['tee_name'],
	# 		# 	date_played=row['date_played'],
	# 		# 	round_type=row['round_type'],
	# 		# 	weather=row['weather'],
	# 		# 	wind=row['wind'],
	# 		# 	comments=row['comments'],
    #         #     # Add other fields as necessary
	# 		# )
    #     # Clear the session data after saving
	# 	request.session['temp_data'] = pd.DataFrame().to_dict('list')
	# 	if new_round:
	# 		return redirect('round-stats', round_id=new_round.id, hole_number=1)  # Redirect to a success page or another appropriate page
	# return redirect('review-data')

#v1
# def save_round(request):
# 	temp_data = request.session.get('temp_data', {})
# 	if temp_data:
# 		df = pd.DataFrame.from_dict(temp_data)
# 		new_round = None
# 		for _, row in df.iterrows():
# 			form = RoundForm(row.to_dict())
# 			if form.is_valid():
# 				new_round = form.save()
# 			else:
# 				print(form.errors)
# 			# new_round = Round.objects.create(
# 			# 	player=row['player'],
# 			# 	course=row['course'],
# 			# 	tee_name=row['tee_name'],
# 			# 	date_played=row['date_played'],
# 			# 	round_type=row['round_type'],
# 			# 	weather=row['weather'],
# 			# 	wind=row['wind'],
# 			# 	comments=row['comments'],
#             #     # Add other fields as necessary
# 			# )
#         # Clear the session data after saving
# 		request.session['temp_data'] = pd.DataFrame().to_dict('list')
# 		if new_round:
# 			return redirect('round-stats', round_id=new_round.id, hole_number=1)  # Redirect to a success page or another appropriate page
# 	return redirect('review-data')


#v3
def review_data(request):
	temp_data = request.session.get('temp_data', {})
	if temp_data:
		df = pd.DataFrame.from_dict(temp_data)
		data_dict = df.to_dict(orient='records')  # Convert DataFrame to a list of dictionaries
	else:
		data_dict = []
	return render(request, 'roundapp/review_data.html', {'data_dict': data_dict})
#v2
# def review_data(request):
# 	temp_data = request.session.get('temp_data', {})
# 	if temp_data:
# 		df = pd.DataFrame.from_dict(temp_data)
# 		table_html = df.to_html(classes='table table-striped')
# 	else:
# 		table_html = "No data available."
# 	return render(request, 'roundapp/review_data.html', {'table_html': table_html})

#v1
# def review_data(request):
# 	temp_data = pd.DataFrame.from_dict(request.session['temp_data'])
# 	return render(request, 'roundapp/round_summary.html', {'temp_data': temp_data.to_html()})


def round_summary(request, round_number_id):
	round_instance = get_object_or_404(Round, id=round_number_id)
	round_stats = RoundStats.objects.filter(round_number=round_instance).order_by('hole_number')
	total_score = sum(stat.score for stat in round_stats) # Test to see if summary stats can be created here for more flexible use in html.
	total_par = sum(stat.par for stat in round_stats) # Test to see if summary stats can be created here for more flexible use in html.
	for stat in round_stats:
		stat.score_diff = stat.score - stat.par # Test to pass score values to par to summary to use in formatting.

	eagles = sum(1 for stat in round_stats if stat.score - stat.par < -1)
	birdies = sum(1 for stat in round_stats if stat.score - stat.par == -1)
	pars = sum(1 for stat in round_stats if stat.score - stat.par == 0)
	bogeys = sum(1 for stat in round_stats if stat.score - stat.par == 1)
	others = sum(1 for stat in round_stats if stat.score - stat.par > 1)
	
	fairway_wayleft = sum(1 for stat in round_stats if stat.fairway == 'wayleft')
	fairway_left = sum(1 for stat in round_stats if stat.fairway == 'left')
	fairway_hit = sum(1 for stat in round_stats if stat.fairway == 'hit')
	fairway_right = sum(1 for stat in round_stats if stat.fairway == 'right')
	fairway_wayright = sum(1 for stat in round_stats if stat.fairway == 'wayright')

	green_hit = sum(1 for stat in round_stats if stat.green == 'hit')
	green_small_miss = sum(1 for stat in round_stats if stat.green == 'left' 
		or stat.green == 'right' or stat.green == 'long' or stat.green == 'short')
	green_big_miss = sum(1 for stat in round_stats if stat.green == 'shortleft' 
		or stat.green == 'shortright' or stat.green == 'longleft' or stat.green == 'longright')
	green_notreach = sum(1 for stat in round_stats if stat.green == 'notreach')

	updown_yes = sum(1 for stat in round_stats if stat.updown == 'yes')
	updown_no = sum(1 for stat in round_stats if stat.updown == 'no')

	sandsave_yes = sum(1 for stat in round_stats if stat.updown == 'yes')
	sandsave_no = sum(1 for stat in round_stats if stat.updown == 'no')

	total_penalties = sum(stat.penalties for stat in round_stats)

	threshold = 0 # THIS MIGHT BE EASIER TO DO BY CREATING A DATAFRAME.
	total_putts = sum(stat.putts for stat in round_stats if stat.putts >= threshold)
	# drive_dist_total = sum(stat for stat in stat.drivedistance if stat.drivedistance >= threshold)
	# drive_dist_count = sum(1 for drive in drivedistance if drive >= threshold)

# This section is to test creating a dataframe for use in the summary page.
	# Convert QuerySet to DataFrame
	df = pd.DataFrame.from_records(round_stats.values())

	filtered_dd_df = df[df['drivedistance'] >= 0]

	# Perform calculations
	drive_dist_total = filtered_dd_df['drivedistance'].sum()
	drive_dist_count = filtered_dd_df['drivedistance'].count()

	# Convert DataFrame to HTML
	df_html = df.to_html(classes='table table-striped', index=False)

	context = {
		'round_number': round_instance,
		'round_stats': round_stats,
		'round_type_choices': ROUND_TYPE_CHOICES,
		'weather_choices': WEATHER_CHOICES,
		'wind_choices': WIND_CHOICES,
		'green_choices': GREEN_CHOICES,
		'fairway_choices': FAIRWAY_CHOICES,
		'updown_choices': UPDOWN_CHOICES,
		'sandsave_choices': SANDSAVE_CHOICES,
		'total_score': total_score, # Test to see if summary stats can be created here for more flexible use in html.
		'total_par': total_par, # Test to see if summary stats can be created here for more flexible use in html.
		'total_putts': total_putts,
		'eagles': eagles,
		'birdies': birdies,
		'pars': pars,
		'bogeys': bogeys,
		'others': others,
		'fairway_wayleft': fairway_wayleft,
		'fairway_left': fairway_left,
		'fairway_hit': fairway_hit,
		'fairway_right': fairway_right,
		'fairway_wayright': fairway_wayright,
		'green_hit': green_hit,
		'green_small_miss': green_small_miss,
		'green_big_miss': green_big_miss,
		'green_notreach': green_notreach,
		'updown_yes': updown_yes,
		'updown_no': updown_no,
		'sandsave_yes': sandsave_yes,
		'sandsave_no': sandsave_no,
		'total_penalties': total_penalties,
		'drive_dist_total': drive_dist_total,
		'drive_dist_count': drive_dist_count,
		'df_html': df_html,

	}
	return render(request, 'roundapp/round_summary.html', context)

def round_csv(request, round_number_id):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=round.csv'
	# Create a csv writer.
	writer = csv.writer(response)
	#Designate the model
	round_instance = get_object_or_404(Round, id=round_number_id)
	stats = RoundStats.objects.filter(round_number=round_instance)
	# Add column headings to file.
	writer.writerow(['Round Number', 'Hole', 'Par', 'Score', 'Fairway', 'Drive Distance', 
		'Green', 'Putts', 'First Putt Distance', 'Up-Down', 'Sand Save', 'Penalties'])
	# Loop through and output.
	for stat in stats:
		if stat.drivedistance == None:
			stat.drivedistance = -1
		if stat.firstputtdistance == None:
			stat.firstputtdistance = -1

		writer.writerow([stat.round_number, stat.hole_number, stat.par, stat.score, stat.fairway, 
			stat.drivedistance, stat.green, stat.putts, stat.firstputtdistance, stat.updown,
			stat.sandsave, stat.penalties])
	return response

