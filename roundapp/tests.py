from django.test import TestCase

# Create your tests here.

# This is a copy of the round_stats page on 1/10/24 to allow adjustments to be made and reuse this if required.
{% extends 'mainapp/base.html' %}

{% block content%}

<!-- 	<h1>Round stats page - to add form for each hole and next / back navigation here.</h1>
	<br> -->

	<h1>Round Details</h1>
	<p>Round ID: {{ round.id }}</p>
	<p>Date Played: {{ round.date_played }}</p>
	<p>Course: {{ round.course.name }}</p>
	<p>Weather: {{ round.weather }}</p>
	<!-- Add more fields as needed -->


<style>
/*    .form-check-label {
        display: block;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        text-align: center;
        cursor: pointer;
        margin-bottom: 10px;
        background-color: transparent;
    }
    .form-check-input {
        display: none;
    }
    .form-check-input:checked + .form-check-label {
        background-color: transparent;
    }
    .form-check-input:checked + .red-box {
        background-color: red;
    }
    .form-check-input:checked + .orange-box {
        background-color: orange;
    }
    .form-check-input:checked + .green-box {
        background-color: green;
    }


    .form-check-label.selected {
        background-color: transparent;
    }
    .form-check-label.selected.red-box {
        background-color: red;
    }
    .form-check-label.selected.orange-box {
        background-color: orange;
    }
    .form-check-label.selected.green-box {
        background-color: green;
    }

    /* Styling for selection boxes for fairway, updown, sandsave etc. */
    .btn-group .btn {
        margin-right: 1px; /* Adjust the margin as needed */
        width: 70px;
        font-size: 20px; 
    }
    .btn-group .btn:last-child {
        margin-right: 0; /* Remove margin for the last button */
    }*/

    /* Styling for form input labels */
/*    .form-group {
        display: flex;
        align-items: center;
    } */
/*    .form-group label {
        margin-right: 10px; /* Adjust the margin as needed *//*
    }*/


/* Styling for numeric inputs */
.numeric-input {}
/*    font-weight: bold;
    color: #333;
    padding: 5px;
    width: 100%;
    box-sizing: border-box;
    font-size: 80px;*/

/*    width: 100%;  Adjust width as needed*/
    /*font-size: 50px; Increase font size 
    size: 100px;
    color: red;
    text-align: center; Center align text*/
/*    padding: 5px;*/
  /*  box-sizing: border-box;
    border-bottom: 2px solid #000;
    border-left: none;
    border-right: none;
    border-top: none;*/
/*    border-width: 400px;
    -moz-appearance: textfield;  Remove arrows in Firefox */
/*}*/

/* Custom formatting to override bootstrap for drive and first putt distance formats. */
#custom-numeric-input-fp,
#custom-numeric-input-dd {
    max-width: 250px;
    width: 100%; /* Adjust width as needed */
    font-size: 25px; /* Increase font size */
    font-weight: bold;
    text-align: center; /* Center align text */
    padding: 1px;
    box-sizing: border-box;
    border-bottom: 2px solid #000;
    border-left: none;
    border-right: none;
    border-top: none;
    -moz-appearance: textfield; /* Remove arrows in Firefox */

}

/* Remove arrows in Chrome, Safari, Edge, and Opera */
.custom-numeric-input-dd::-webkit-outer-spin-button,
.custom-numeric-input-dd::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

/* Remove arrows in Chrome, Safari, Edge, and Opera */
.custom-numeric-input-fp::-webkit-outer-spin-button,
.custom-numeric-input-fp::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

/*.form-label {
    display: inline-block;
    width: 150px; /* Adjust as needed *//*
    text-align: left;
    margin-right: 10px;
    color: red;
}*/


/* Styling for Green button options (3x3 box with not reach underneath) */
/*    .btn-group-vertical .btn {
        width: 100px; /* Set the desired width *//*
        padding: 20px; /* Set consistent padding *//*
        margin: 0px; /* Add margin for spacing *//*
        text-align: center; /* Center the text *//*
    }
    .btn-group-vertical .btn-wide {
        width: calc(100px * 3 + 0px * 2); /* Width of three buttons plus margins *//*
    }*/


	.form-group {
        display: flex;
        align-items: center;
    }
    .form-group label {
        margin-right: 10px; /* Adjust the margin as needed */
    }

    .btn-group-vertical {
        display: flex;
        flex-direction: column;
        align-items: flex-start; /* Align buttons to the left */
    }
/*    .btn-group-vertical {
        display: flex;
        flex-direction: column;
        align-items: center;
    }*/
    .btn-group-vertical .btn {
        width: 100px; /* Set the desired width */
        height: 50px; /* Set the desired height */
        margin: 0px; /* Add margin for spacing */
        text-align: center; /* Center the text */
        padding: 0; /* Ignore internal padding */
    }
    .btn-group-vertical .btn-wide {
        width: calc(100px * 3 + 0px * 2); /* Width of three buttons plus margins */
        margin-left: 0px;
        align-self: flex-start;
        padding-left: 0; /* Remove left padding */
	    padding-right: 0; /* Remove right padding */
    }

	.btn-group-vertical .row-wide {
		width: 300px;
	    padding-left: 0; /* Remove left padding */
	    padding-right: 0; /* Remove right padding */
	}

    .btn-group-vertical .row {
        margin: 0; /* Remove default row margin */
    }
    .btn-group-vertical .col-4 {
        padding: 0; /* Remove default column padding */
    }



    .custom-button {
    padding: 0 !important;
    margin: 0 !important;
    width: 100%;
    box-sizing: border-box;
}


/* Styling for score box and buttons */       
	 .number-input {
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 20px 0;
        -moz-appearance: textfield; /* Remove arrows in Firefox */
    }

	/* Remove arrows in Chrome, Safari, Edge, and Opera */
	.number-input::-webkit-outer-spin-button,
	.number-input::-webkit-inner-spin-button {
	    -webkit-appearance: none;
	    margin: 0;
	}

    .number-input input {
        font-size: 2em;
        width: 100px;
        text-align: center;
        margin: 0 10px;
    }
    .number-input button {
        font-size: 2em;
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
    }


</style>


<h1>Round Stats for Hole {{ hole.hole_number }}: Par {{ hole.par }}</h1>

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}

<div class="container mt-4 mx-auto" sytle="width: 400px">
    <form method="post">
        {% csrf_token %}

<!--         <div class="form-group">
            {{ form.score.label_tag }} {{ form.score }}
        </div> <br> -->

test par: {{ hole.par }}
test score value: {{ score_value }}

		<input type="hidden" id="score_value" name="score_value">
        <div class="number-input">
            <button type="button" onclick="decrease()">&#8722;</button>

            <!-- {% if form.score %} -->

            	{{ form.score }}

<!--             {% else %}

            	{{ hole.par }}

            {% endif%} -->
            <button type="button" onclick="increase()">&#43;</button>
        </div>



<!--         <div class="form-group">
            {{ form.fairway.label_tag }} {{ form.fairway }}
        </div> <br> -->
		
        <input type="hidden" id="fairway_value" name="fairway_value">
        {{ form.fairway.label_tag }} 
        <div class="btn-group" role="group" aria-label="Fairway:">
        	<button type="button" class="btn btn-outline-danger"
        		onclick="selectOption(this, 'fairway_value', 'wayleft')">Way Left</button>
        	<button type="button" class="btn btn-outline-warning"
        		onclick="selectOption(this, 'fairway_value', 'left')">Left</button>
        	<button type="button" class="btn btn-outline-success"
        		onclick="selectOption(this, 'fairway_value', 'hit')">Hit</button>
        	<button type="button" class="btn btn-outline-warning"
        		onclick="selectOption(this, 'fairway_value', 'right')">Right</button>
        	<button type="button" class="btn btn-outline-danger"
        		onclick="selectOption(this, 'fairway_value', 'right')">Way Right</button>
        </div><br><br>

        <div class="form-group">
            {{ form.drivedistance.label_tag }} {{ form.drivedistance }}
        </div> <br>
<!-- 	    <div class="form-group">
	        <label for="{{ form.drivedistance.id_for_label }}" class="form-label">{{ form.drivedistance.label }}</label>
	        {{ form.drivedistance }}
	    </div> -->

<input type="hidden" id="green_value" name="green_value">

            <div class="form-group">
                {{ form.green.label_tag }}
                <div class="btn-group-vertical">
                    <div class="row">
                        <div class="col-4">
                            <button type="button" class="btn btn-outline-danger"
                                onclick="selectgreenOption(this, 'green_value', 'longleft')">Long Left</button>
                        </div>
                        <div class="col-4">
                            <button type="button" class="btn btn-outline-warning"
                                onclick="selectgreenOption(this, 'green_value', 'long')">Long</button>
                        </div>
                        <div class="col-4">
                            <button type="button" class="btn btn-outline-danger"
                                onclick="selectgreenOption(this, 'green_value', 'longright')">Long Right</button>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-4">
                            <button type="button" class="btn btn-outline-warning"
                                onclick="selectgreenOption(this, 'green_value', 'left')">Left</button>
                        </div>
                        <div class="col-4">
                            <button type="button" class="btn btn-outline-success"
                                onclick="selectgreenOption(this, 'green_value', 'hit')">Hit</button>
                        </div>
                        <div class="col-4">
                            <button type="button" class="btn btn-outline-warning"
                                onclick="selectgreenOption(this, 'green_value', 'right')">Right</button>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-4">
                            <button type="button" class="btn btn-outline-danger"
                                onclick="selectgreenOption(this, 'green_value', 'shortleft')">Short Left</button>
                        </div>
                        <div class="col-4">
                            <button type="button" class="btn btn-outline-warning"
                                onclick="selectgreenOption(this, 'green_value', 'short')">Short</button>
                        </div>
                        <div class="col-4">
                            <button type="button" class="btn btn-outline-danger"
                                onclick="selectgreenOption(this, 'green_value', 'shortright')">Short Right</button>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-12">
                            <button type="button" class="btn btn-outline-danger btn-wide col-12 custom-button"
                                onclick="selectgreenOption(this, 'green_value', 'notreach')">Not Able to Reach</button>
                        </div>
                    </div>
                </div>
            </div><br>






<!--         <div class="form-group">
            {{ form.putts.label_tag }} {{ form.putts }}
        </div> <br> -->

        <input type="hidden" id="putts_value" name="putts_value">
        {{ form.putts.label_tag }}
        <div class="btn-group" role="group" aria-label="Putts:">
        	<button type="button" class="btn btn-outline-success"
        		onclick="selectOption(this, 'putts_value', 0)">0</button>
        	<button type="button" class="btn btn-outline-success"
        		onclick="selectOption(this, 'putts_value', 1)">1</button>
        	<button type="button" class="btn btn-outline-success"
        		onclick="selectOption(this, 'putts_value', 2)">2</button>
        	<button type="button" class="btn btn-outline-danger"
        		onclick="selectOption(this, 'putts_value', 3)">3</button>
        	<button type="button" class="btn btn-outline-danger"
        		onclick="selectOption(this, 'putts_value', 4)">4</button>
        </div><br><br>



        <div class="form-group">
            {{ form.firstputtdistance.label_tag }} {{ form.firstputtdistance }}
        </div> <br>

<!--         <div class="form-group">
            {{ form.updown.label_tag }} {{ form.updown }}
        </div>  -->

        <input type="hidden" id="updown_value" name="updown_value">
        {{ form.updown.label_tag }}
        <!-- <label for="updown_value">Up/Down:</label> -->
        <div class="btn-group" role="group" aria-label="Up/Down:">
        	<button type="button" class="btn btn-outline-success"
        		onclick="selectOption(this, 'updown_value', 'yes')">Yes</button>
        	<button type="button" class="btn btn-outline-danger"
        		onclick="selectOption(this, 'updown_value', 'no')">No</button>
        </div><br><br>
        
<!--         <div class="form-group">
            {{ form.sandsave.label_tag }} {{ form.sandsave }}
        </div>  -->
        <input type="hidden" id="sandsave_value" name="sandsave_value">
        {{ form.sandsave.label_tag }}
        <!-- <label for="sandsave_value">Sand Save:</label> -->
        <div class="btn-group" role="group" aria-label="Sandsave:">
        	<button type="button" class="btn btn-outline-success"
        		onclick="selectOption(this, 'sandsave_value', 'yes')">Yes</button>
        	<button type="button" class="btn btn-outline-danger"
        		onclick="selectOption(this, 'sandsave_value', 'no')">No</button>
        </div><br><br>

<!--         <div class="form-group">
            {{ form.penalties.label_tag }} {{ form.penalties }}
        </div> <br> -->

        <input type="hidden" id="penalties_value" name="penalties_value">
        {{ form.penalties.label_tag }}
        <div class="btn-group" role="group" aria-label="Penalties:">
        	<button type="button" class="btn btn-outline-success"
        		onclick="selectOption(this, 'penalties_value', 0)">0</button>
        	<button type="button" class="btn btn-outline-danger"
        		onclick="selectOption(this, 'penalties_value', 1)">1</button>
        	<button type="button" class="btn btn-outline-danger"
        		onclick="selectOption(this, 'penalties_value', 2)">2</button>
        	<button type="button" class="btn btn-outline-danger"
        		onclick="selectOption(this, 'penalties_value', 3)">3</button>
        	<button type="button" class="btn btn-outline-danger"
        		onclick="selectOption(this, 'penalties_value', 4)">4</button>
        </div><br><br>

        <button type="submit" class="btn btn-primary" name="save">Save</button>
<!--         <button type="submit" class="btn btn-secondary" name="back">Back</button>
        <button type="submit" class="btn btn-secondary" name="next">Next</button> -->

		<!-- <div> -->
		    {% if previous_hole_number %}
		        <button type="submit" class="btn btn-secondary" name="back">
		        <a href="{% url 'round-stats' round.id previous_hole_number %}">Back</a></button>
		    {% endif %}
		    {% if next_hole_number %}
		    	<button type="submit" class="btn btn-secondary" name="next">
		        <a href="{% url 'round-stats' round.id next_hole_number %}">Next</a></button>
		    {% endif %}
		<!-- </div> -->

    </form>
</div>




<script>
document.addEventListener('DOMContentLoaded', function() {
    const radioButtons = document.querySelectorAll('.form-check-input');
    radioButtons.forEach(radio => {
        radio.addEventListener('change', function() {
            radioButtons.forEach(rb => {
                rb.nextElementSibling.classList.remove('selected');
            });
            this.nextElementSibling.classList.add('selected');
        });
    });
});


    // To handle fairway selection buttons.
    function selectOption(button, hiddenInputId, value) {
        let hiddenInput = document.getElementById(hiddenInputId);
        let btnGroup = button.closest('.btn-group');
        let buttons = btnGroup.querySelectorAll('.btn');

        if (button.classList.contains('active')) {
            // If the button is already active, deselect it
            button.classList.remove('active');
            hiddenInput.value = '';
        } else {
            // If the button is not active, select it and deselect others
            buttons.forEach(btn => {
                btn.classList.remove('active');
            });
            button.classList.add('active');
            hiddenInput.value = value;
        }
    }


        function selectgreenOption(button, hiddenInputId, value) {
        let hiddenInput = document.getElementById(hiddenInputId);
        let btnGroup = button.closest('.btn-group-vertical');
        let buttons = btnGroup.querySelectorAll('.btn');

        if (button.classList.contains('active')) {
            // If the button is already active, deselect it
            button.classList.remove('active');
            hiddenInput.value = '';
        } else {
            // If the button is not active, select it and deselect others
            buttons.forEach(btn => {
                btn.classList.remove('active');
            });
            button.classList.add('active');
            hiddenInput.value = value;
        }
    }


    function increase() {
        var input = document.getElementById('id_score');
        input.value = parseInt(input.value) + 1;
    }

    function decrease() {
        var input = document.getElementById('id_score');
        input.value = parseInt(input.value) - 1;
    }

</script>

{% endblock%}
