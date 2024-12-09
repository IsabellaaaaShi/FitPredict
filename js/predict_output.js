// Update the Prediction Output Page using JavaScript

// Reference PUI HW 6 in order to get params sent from form in the predict_input.html page
const queryString = window.location.search; 
const params = new URLSearchParams(queryString); 

// Get the main data from the url parameters.
const unit = params.get('unit');
const sex = params.get('sex');
const age = params.get('age');
const nickname = params.get('nickname');
const weight = params.get('weight');

// Ensure that the variabels can be changed programatically: https://stackoverflow.com/questions/65046136/typeerror-assignment-to-constant-variable
let height_m = 0;
let height_ft = 0;
let height_in = 0; 

// Based on user input for metric/imperial set the height. The fields change so choose metric or feet and inches
if (unit == "metric") {
    height_m = params.get('height-metric');
    height_ft = 0;
    height_in = 0; 
} else if (unit == "imperial") {
    height_m = 0
    height_ft = params.get('height-feet');
    height_in = params.get('height-inches'); 
}

// JS defined as module as per PyScript tutorial referenced in the predict_output.html page. Export variables so they are accessible in Model.py
export {unit, age, sex, height_m, height_ft, height_in, weight, nickname};

// Get the loading element and the results elements (Sections 1 and 2)
const loading_el = document.querySelector("#loading-screen")
const result_el = document.querySelector("#model-results")
const fitness_el = document.querySelector("#fitness-results")

// On start, hide the results sections and show the loading section
loading_el.classList.remove("hidden")
result_el.classList.add("hidden")
fitness_el.classList.add("hidden")

// Add the gif image to the loading section
const loadgif_el = document.querySelector("#loading-gif")
const loadgif = document.createElement("img")
loadgif.src = "./assets/loading.gif"
loadgif_el.appendChild(loadgif)

// Run function to update the user input section on the output page
updateUserInputSection();

// Define function to update the user input section on the output page
function updateUserInputSection() {

    // Find and update the user input sections (sex and age do not depend on unit selection)
    const sexElement = document.querySelector("#sex-info"); 
    sexElement.innerText = sex; 
    const ageElement = document.querySelector("#age-info"); 
    ageElement.innerText = age; 

    // Update height and weight text based on user input
    const heightElement = document.querySelector("#height-info");
    const weightElement = document.querySelector("#weight-info");  
    if (unit == "metric") {
        heightElement.innerText = height_m + " m"; 
        weightElement.innerText = weight + " kg"; 
    } else if (unit == "imperial") {
        heightElement.innerText = height_ft + " ft " + height_in + " in";
        weightElement.innerText = weight + " lbs"; 
    }

    // Is string empty for name? https://www.freecodecamp.org/news/check-if-string-is-empty-or-null-javascript/
    const nameElement = document.querySelector("#name-info"); 
    if (typeof nickname === "string" && nickname.length === 0) {
        nameElement.innerText = "Hi, Anonymous User!";
    } else {
        nameElement.innerText = "Hi, " + nickname + "!";
    }

}