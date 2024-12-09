// Update the Prediction Input Page using JavaScript
// Used to get user selection of unit type and update the form accordingly 

// Get the html elements for height and weight to manipulate based on user unit selection
const heightmetric_element = document.getElementById('height-metric');
const heightimperial_element = document.getElementById('height-imperial');
const heightmetric_label_element = document.getElementById('metric-label');
const heightimperial_label_element = document.getElementById('imperial-label');
const heightfeet_element = document.getElementById('height-feet');
const heightinches_element = document.getElementById('height-inches');
const unitselect_element = document.getElementById('unit')
const weight_element = document.getElementById('weight');

// Make metric display by default
weight_element.placeholder = 'kg';

// By default hide the imperial input selections, show the metric
heightmetric_element.classList.remove("hidden");
heightimperial_element.classList.add("hidden");
heightmetric_label_element.classList.remove("hidden");
heightimperial_label_element.classList.add("hidden");

// Disable the input of the imperial form elements so they do not appear in the url when sent to the output page
heightfeet_element.disabled = true;
heightinches_element.disabled = true;
heightmetric_element.disabled = false;

// Set an event listener to update the input form fields based on user input selection
// https://stackoverflow.com/questions/24865177/add-an-onchange-event-listener-to-an-html-input-field
// https://www.w3schools.com/jsref/prop_text_disabled.asp
unitselect_element.addEventListener("change", function(){

    // If metric, hide the imperial and disable the inputs so they are not sent in the form output
    if (unitselect_element.value == "metric") {

        weight_element.placeholder = 'kg';

        heightmetric_element.classList.remove("hidden");
        heightimperial_element.classList.add("hidden");
        heightmetric_label_element.classList.remove("hidden");
        heightimperial_label_element.classList.add("hidden");

        heightfeet_element.disabled = true;
        heightinches_element.disabled = true;
        heightmetric_element.disabled = false;

    // If imperial, hide the metric and disable the inputs so they are not sent in the form output
    } else if (unitselect_element.value == "imperial") {

        weight_element.placeholder = 'lbs';

        heightmetric_element.classList.add("hidden");
        heightimperial_element.classList.remove("hidden");
        heightmetric_label_element.classList.add("hidden");
        heightimperial_label_element.classList.remove("hidden");

        heightfeet_element.disabled = false;
        heightinches_element.disabled = false;
        heightmetric_element.disabled = true;
    }

});