# Import pyscript related items to manipulate the DOM based on the following documentation:
# https://docs.pyscript.net/2024.11.1/user-guide/dom/
from pyscript import window, document

# https://docs.pyscript.net/2024.11.1/user-guide/configuration/
# https://docs.pyscript.net/2024.11.1/user-guide/dom/#working-with-javascript
from pyscript.js_modules import outputScript

# Access the DOM elements to programatially change the visibility of the output page sections
loading_el = document.querySelector("#loading-screen")
result_el = document.querySelector("#model-results")
fitness_el = document.querySelector("#fitness-results")

# Try to ignore warnings. known error in pyscript described at:
# https://github.com/pandas-dev/pandas/issues/54466
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings(
        "ignore",
        message=r'\nPyarrow will become',
        category=DeprecationWarning,
    )
    import pandas as pd
warnings.filterwarnings("ignore")

# Import necessarily libraries. Also configured in the json file
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

def model_init():
    print("initializing model")

# Load the dataset
data = pd.read_csv("data.csv")

# Selecting relevant features and target variables
columns = ['Gender', 'Age', 'Weight', 'Height', 'Body Fat Percentage', 'Workout Type', 'Workout Frequency', 'Session Duration']
df = data[columns]

# Encode 'Gender' as 0 (Male) and 1 (Female)
df['Gender'] = df['Gender'].apply(lambda x: 0 if x in ['M', 'Male'] else 1)

# Encode 'Workout Type' using LabelEncoder
label_encoder = LabelEncoder()
df['Workout Type'] = label_encoder.fit_transform(df['Workout Type'])

# Step 1: Data for Body Fat Percentage Prediction
# Use rows that include `['Gender', 'Age', 'Weight', 'Height', 'Body Fat Percentage']`
df_body_fat = df[['Gender', 'Age', 'Weight', 'Height', 'Body Fat Percentage']].dropna(subset=['Body Fat Percentage'])

# Step 2: Data for Workout Prediction
# Use rows that include all target variables
df_workout = df.dropna(subset=['Workout Type', 'Workout Frequency', 'Session Duration'])

# Separate datasets for Body Fat Prediction and Workout Predictions
X_body_fat = df_body_fat[['Gender', 'Age', 'Weight', 'Height']]
y_body_fat = df_body_fat['Body Fat Percentage']

X_workout = df_workout[['Gender', 'Age', 'Weight', 'Height', 'Body Fat Percentage']]
y_workout_type = df_workout['Workout Type']
y_workout_frequency = df_workout['Workout Frequency']
y_session_duration = df_workout['Session Duration']

# Imputers for specific datasets
imputer_body_fat = SimpleImputer(strategy='median')  # For Body Fat features
imputer_workout = SimpleImputer(strategy='median')   # For Workout-related features

# Impute Body Fat Percentage dataset
X_body_fat.iloc[:, :] = imputer_body_fat.fit_transform(X_body_fat)

# Impute Workout-related dataset
X_workout.iloc[:, :] = imputer_workout.fit_transform(X_workout)

# Split data into training and testing sets for Body Fat Prediction
X_train_body_fat, X_test_body_fat, y_train_body_fat, y_test_body_fat = train_test_split(
    X_body_fat, y_body_fat, test_size=0.2, random_state=42
)

# Train Random Forest Regressor for Body Fat Prediction
model_body_fat = RandomForestRegressor(random_state=42)
model_body_fat.fit(X_train_body_fat, y_train_body_fat)

# Split data into training and testing sets for Workout Predictions
X_train_workout, X_test_workout, y_train_workout_type, y_test_workout_type = train_test_split(
    X_workout, y_workout_type, test_size=0.2, random_state=42
)
_, _, y_train_workout_frequency, y_test_workout_frequency = train_test_split(
    X_workout, y_workout_frequency, test_size=0.2, random_state=42
)
_, _, y_train_session_duration, y_test_session_duration = train_test_split(
    X_workout, y_session_duration, test_size=0.2, random_state=42
)

# Train models for Workout Predictions
model_workout_type = RandomForestRegressor(random_state=42)
model_workout_type.fit(X_train_workout, y_train_workout_type)

model_workout_frequency = RandomForestRegressor(random_state=42)
model_workout_frequency.fit(X_train_workout, y_train_workout_frequency)

model_session_duration = RandomForestRegressor(random_state=42)
model_session_duration.fit(X_train_workout, y_train_session_duration)

print("All models trained successfully.")

# Function for handling user input and predicting
def predict_user_metrics(user_data):
    """
    Predicts Body Fat Percentage and then uses it to predict Workout Type, Workout Frequency, and Session Duration.
    """
    # Step 1: Predict Body Fat Percentage
    body_fat_data = pd.DataFrame([user_data[:4]], columns=['Gender', 'Age', 'Weight', 'Height'])
    body_fat_data = imputer_body_fat.transform(body_fat_data)  # Use the Body Fat imputer
    predicted_body_fat = model_body_fat.predict(body_fat_data)[0]

    # Step 2: Predict Workout Metrics using Body Fat Percentage
    workout_data = pd.DataFrame([user_data + [predicted_body_fat]], columns=['Gender', 'Age', 'Weight', 'Height', 'Body Fat Percentage'])
    workout_data = imputer_workout.transform(workout_data)  # Use the Workout imputer
    predicted_workout_type = model_workout_type.predict(workout_data)[0]
    predicted_workout_frequency = int(round(model_workout_frequency.predict(workout_data)[0]))
    predicted_session_duration = model_session_duration.predict(workout_data)[0]

    return predicted_body_fat, predicted_workout_type, predicted_workout_frequency, predicted_session_duration

# User Input
# print("Enter your details to predict metrics:")

# Gather user input by accessing the javascript specified in the json file
user_units = outputScript.unit
user_name = outputScript.nickname #input("Please enter your name: ").strip()
user_gender = outputScript.sex #input("Gender (Male/Female): ").strip().lower()
user_age = int(outputScript.age) #int(input("Age: "))
user_weight = float(outputScript.weight)

# Set placeholder heights of 0. to be set based on user unit selection
user_height = 0
user_height_m = 0
user_height_ft = 0
user_height_in = 0

# If metric, set the user height variable equal to the url height parameter.
# If imperial, conver the feet and inches to meters, and lbs to kgs
if user_units == "metric":
    user_height = float(outputScript.height_m) #float(input("Height (m): "))
elif user_units == "imperial":
    user_height_ft = float(outputScript.height_ft)
    user_height_in = float(outputScript.height_in)
    # Convert to Metric units for input to the model
    user_height = ((user_height_ft*12)+user_height_in)* 0.0254
    user_weight = user_weight * 0.453592

# Encode gender input
user_gender_encoded = 0 if user_gender == 'male' else 1

# Prepare user data
user_data = [user_gender_encoded, user_age, user_weight, user_height]

# Predict metrics
predicted_body_fat, predicted_workout_type, predicted_workout_frequency, predicted_session_duration = predict_user_metrics(user_data)

# Decode Workout Type
decoded_workout_type = label_encoder.inverse_transform([int(predicted_workout_type)])[0]

# Additional Calculations
def calculate_bmi(weight, height):
    return round(weight / (height ** 2), 2)

def calculate_body_fat_weight(weight, body_fat_percentage):
    return round((body_fat_percentage / 100) * weight, 2)

def calculate_fat_free_body_weight(weight, body_fat_weight):
    return round(weight - body_fat_weight, 2)

def calculate_body_water_percentage(weight, fat_free_body_weight):
    # Average adult body water percentage is about 73% of fat-free mass
    return round((fat_free_body_weight * 0.73) / weight * 100, 2)

def calculate_bmr(weight, height, age, gender):
    # BMR formula: Harris-Benedict equation
    if gender == 'male':
        return round(88.362 + (13.397 * weight) + (4.799 * height * 100) - (5.677 * age), 2)
    else:
        return round(447.593 + (9.247 * weight) + (3.098 * height * 100) - (4.330 * age), 2)

# Calculate Metrics
user_body_fat_weight = calculate_body_fat_weight(user_weight, predicted_body_fat)
user_fat_free_body_weight = calculate_fat_free_body_weight(user_weight, user_body_fat_weight) #user_weight is still metric, so convert output to imperial
user_body_water_percentage = calculate_body_water_percentage(user_weight,user_fat_free_body_weight)
user_bmi = calculate_bmi(user_weight, user_height)
user_bmr = calculate_bmr(user_weight, user_height, user_age, user_gender)

# Output Results
print(f"\nHi {user_name}, here are your predicted metrics:")
print(f"Body Fat Percentage: {predicted_body_fat:.2f}%")
print(f"Your BMI: {user_bmi}")

# Output results with weight measurements. Change based on unit selection
if user_units == "metric":
    print(f"Body Fat Weight: {user_body_fat_weight} kg")
    print(f"Fat-Free Body Weight: {user_fat_free_body_weight} kg")
elif user_units == "imperial":
    print(f"Body Fat Weight: {round(user_body_fat_weight* 2.20462, 2)} lbs")
    print(f"Fat-Free Body Weight: {round(user_fat_free_body_weight* 2.20462, 2)} lbs")

# Output the rest of the Results
print(f"Body Water Percentage: {user_body_water_percentage:.2f}%")
print(f"Basal Metabolic Rate (BMR): {user_bmr} kcal/day")
print(f"Workout Type: {decoded_workout_type}")
print(f"Workout Frequency: {predicted_workout_frequency} sessions/week")  # Rounded to int
print(f"Session Duration: {predicted_session_duration:.2f} hours")

# Display Similar Examples for Transparency
distances = np.linalg.norm(X_workout[['Gender', 'Age', 'Weight', 'Height']].values - user_data[:4], axis=1)
similar_examples = df_workout.iloc[np.argsort(distances)[:3]]

print("\nSimilar examples from our training data:")
for idx, row in similar_examples.iterrows():
    print(f"- Gender: {row['Gender']}, Age: {row['Age']}, Weight: {row['Weight']} kg, Height: {row['Height']} m → Body Fat: {row['Body Fat Percentage']:.2f}%")

# Update the DOM based on the results 

# First remove gif from the loading gif
loading_element = document.querySelector("#loading-gif")
loading_element.remove()

# Display the user results
bodyfatpercent_element = document.querySelector("#result-bodyfatpercent")
bodyfatpercent_element.innerText = f"{predicted_body_fat:.2f}"

bodyfatweight_element = document.querySelector("#result-bodyfatweight")
bodyfatweight_unit_element = document.querySelector("#result-bodyfatweight-unit")

fatfreebodyweight_element = document.querySelector("#result-fatfreebodyweight")
fatfreebodyweight_unit_element = document.querySelector("#result-fatfreebodyweight-unit")

# Change DOM units based on user input
if user_units == "metric":
    bodyfatweight_element.innerText = user_body_fat_weight
    fatfreebodyweight_element.innerText = user_fat_free_body_weight
    bodyfatweight_unit_element.innerText = "kg"
    fatfreebodyweight_unit_element.innerText = "kg"
elif user_units == "imperial":
    bodyfatweight_element.innerText = round(user_body_fat_weight* 2.20462, 2)
    fatfreebodyweight_element.innerText = round(user_fat_free_body_weight* 2.20462, 2)
    bodyfatweight_unit_element.innerText = "lbs"
    fatfreebodyweight_unit_element.innerText = "lbs"

bmi_element = document.querySelector("#result-bmi")
bmi_element.innerText = user_bmi

bmr_element = document.querySelector("#result-bmr")
bmr_element.innerText = user_bmr

bodywater_element = document.querySelector("#result-bodywater")
bodywater_element.innerText = f"{user_body_water_percentage:.2f}"

fitnesstype_element = document.querySelector("#result-fitnesstype")
fitnesstype_element.innerText = decoded_workout_type

fitnesstime_element = document.querySelector("#result-fitnessduration")
fitnesstime_element.innerText = f"{predicted_session_duration:.2f}"

fitnessfreq_element = document.querySelector("#result-fitnessfreq")
fitnessfreq_element.innerText = predicted_workout_frequency

fitnesstypeicon_element = document.querySelector("#fitnesstype-icon")
fitnessicon = document.createElement('img')

# Change the fitness image based on the recommended fitness type
if decoded_workout_type == 'CARDIO':
    fitnessicon.src = "./assets/workout icon/CARDIO.png"
elif decoded_workout_type == 'HIIT':
    fitnessicon.src = "./assets/workout icon/HIIT.png"
elif decoded_workout_type == 'STRENGTH':
    fitnessicon.src = "./assets/workout icon/STRENGTH.png"
elif decoded_workout_type == 'YOGA':
    fitnessicon.src = "./assets/workout icon/YOGA.png"

# Add the fitness icon to the DOM
fitnesstypeicon_element.appendChild(fitnessicon)

# Hide the loading message section, show the results section
loading_el.classList.add("hidden")
result_el.classList.remove("hidden")
fitness_el.classList.remove("hidden")