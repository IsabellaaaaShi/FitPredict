// -------- update detail page selection ------------------------------------------
// reference PUI HW 6
const queryString = window.location.search; 
const params = new URLSearchParams(queryString); 

const sex = params.get('sex');
const weight = params.get('weight');
const height = params.get('height');
const age = params.get('age');
const nickname = params.get('nickname');


console.log(sex)
console.log(weight)
console.log(height)
console.log(age)
console.log(nickname)


export {age, sex, height, weight, nickname};

const loading_el = document.querySelector("#loading-screen")
const result_el = document.querySelector("#model-results")
const fitness_el = document.querySelector("#fitness-results")

loading_el.classList.remove("hidden")
result_el.classList.add("hidden")
fitness_el.classList.add("hidden")

const loadgif_el = document.querySelector("#loading-gif")
const loadgif = document.createElement("img")

loadgif.src = "./assets/loading.gif"

loadgif_el.appendChild(loadgif)

updateUserInputSection();


function updateUserInputSection() {

    // update info
    const sexElement = document.querySelector("#sex-info"); 
    sexElement.innerText = sex; 

    const weightElement = document.querySelector("#weight-info"); 
    weightElement.innerText = weight + " kg"; 
    const heightElement = document.querySelector("#height-info"); 
    heightElement.innerText = height + "m"; 
    const ageElement = document.querySelector("#age-info"); 
    ageElement.innerText = age; 

    // is string empty for name? https://www.freecodecamp.org/news/check-if-string-is-empty-or-null-javascript/
    const nameElement = document.querySelector("#name-info"); 
    if (typeof nickname === "string" && nickname.length === 0) {
        nameElement.innerText = "Hi, Anonymous User!";
    } else {
        nameElement.innerText = "Hi, " + nickname + "!";
    }

}