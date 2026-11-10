# Set of dummy data to replicate getting data from the sticker
sticker_data = [
    (36.4, 98, 90, 78, 1, 72, 4.3821, 102.3215),
    (30.9, 20, 92, 27, 1, 43, 7.6541, 83.4122),
    (37.2, 35, 100, 12, 0, 12, 6.0293, 100.0420),
    (38.0, 100, 87, 87, 0, 19, 76.8124, 58.1111),
    (32.8, 92, 98, 99, 0, 89, 12.6767, 67.6767),
    (35.4, 75, 91, 40, 1, 56, 10.3241, 112.4150),
    (31.4, 53, 95, 100, 0, 67, 8.9902, 99.9452),
    # BodyTemp, Heartrate, Oxygen, Battery Percentage, Charging Status, Stress, Latitude, Longitude
]

species_ranges = {
    # 0-1 Bodytemp range, 2-3 heartrate range
    "orangutan": (36.1, 36.5, 70, 120),
    "tapirus": (36.0, 37.0, 40, 70),
    "elephant": (36.0, 36.9, 25, 45),
    "tiger": (37.8, 39.4, 60, 100),
    "pangolin": (31.7, 34.2, 50, 100)
}
        
def process_sticker(species, dataset):
    range_data = species_ranges.get(species)

    temp_min, temp_max, hr_min, hr_max = range_data # Range data is the data of a particular species from "species range"
    body_temp, heart_rate, oxygen, battery_percentage, charging_status, stress_index, latitude, longitude = dataset

    # This will return values to be used in output later
    temp_status = check_bodytemp(body_temp, temp_min, temp_max)
    hr_status = check_heartrate(heart_rate, hr_min, hr_max)
    oxygen_status = check_oxygen(oxygen)
    stress_status = check_stress(stress_index)
    risk_status = check_risk(body_temp, temp_min, temp_max, heart_rate, hr_min, hr_max, oxygen, stress_index)
    battery_status = check_battery(battery_percentage, charging_status)
    gel_status = cool_gel(body_temp, temp_max)
    actions = get_action_plan(risk_status)
    # Return function statuses and variable data(bodytemp oxygen etc)
    return (body_temp, temp_status, heart_rate, hr_status, oxygen, oxygen_status, battery_status, stress_status, latitude, longitude, risk_status, gel_status, actions) 

# Calculate the animal's body temperature status and write the output message
def check_bodytemp(body_temp, temp_min, temp_max):
    if (body_temp > temp_max + 1.0) or (body_temp < temp_min - 1.0):
        return(f"Body Temperature: {body_temp} Celsius [ OVERWHELMING DANGER]")
    
    elif (body_temp > temp_max + 0.4) or (body_temp < temp_min - 0.4):
        return(f"Body Temperature: {body_temp} Celsius [ DANGER ]")
            
    elif (body_temp > temp_max) or (body_temp < temp_min):
        return(f"Body Temperature: {body_temp} Celsius [ MILD ]")
            
    else:
        return(f"Body Temperature: {body_temp} Celsius [ NORMAL ]")    
        
# Calculate the animal's heart rate status and format the output
def check_heartrate(heart_rate, hr_min, hr_max):
    if (heart_rate < 0):
        return ("!! Heart Rate Sensor Broken !!")
    elif (heart_rate > hr_max + 20):
        return (f"Heart Rate: {heart_rate} BPM [ HIGHLY ELEVATED ]")
            
    elif (heart_rate < hr_min - 20):
        return (f"Heart Rate: {heart_rate} BPM [ CRITICALLY LOW ]")
            
    elif (heart_rate > hr_max + 10):
        return (f"Heart Rate: {heart_rate} BPM [ ELEVATED ]")
            
    elif (heart_rate < hr_min - 10):
        return (f"Heart Rate: {heart_rate} BPM [ LOW ]")

    elif (heart_rate > hr_max):
        return (f"Heart Rate: {heart_rate} BPM [ SLIGHTLY ELEVATED ]")
            
    elif (heart_rate < hr_min):
        return (f"Heart Rate: {heart_rate} BPM [ SLIGHTLY LOW ]")

    else:
        return (f"Heart Rate: {heart_rate} BPM [ NORMAL ]")
            
# Calculate whether the animal's blood contains sufficient oxygen(risk of hypoxia)
def check_oxygen(oxygen):

    if (oxygen < 0):
        return("!! Oxygen Sensor Broken !!")
    
    elif (oxygen > 100):
        return (f"Oxygen: {oxygen}% [ SENSOR ERROR ]")
   
    elif (oxygen >= 95):
        return (f"Oxygen: {oxygen}% [ NORMAL ]")

    elif (oxygen >= 90):
        return (f"Oxygen: {oxygen}% [ SLIGHTLY LOW ]")

    elif (oxygen >= 85):
        return (f"Oxygen: {oxygen}% [ LOW ]")

    else:
        return (f"Oxygen: {oxygen}% [ CRITICALLY LOW ]")
            
# Calculate if cooling gel should be released to relieve the animal
def cool_gel(body_temp, temp_max):
    if body_temp > temp_max:
        return("Cool gel releasing")
    return("Cool gel on standby")

# Check the battery status
def check_battery(battery_percentage, charging_status):
    
    charging_text = ""
    if (charging_status == 1):
        charging_text = "Charging"  
    else: 
        charging_text = "Not Charging"
    # Print an alert if battery is low and not charging
    if (battery_percentage <= 20) and (charging_status == 0):
        return (f"Battery: {battery_percentage}% | Status: {charging_text} | [! ALERT: Low Battery]")
    else:
        return (f"Battery: {battery_percentage}% | Status: {charging_text}")

# Calculate the stress status for the animal
def check_stress(stress_index):
    if (stress_index < 0):
        return("!! Stress Sensor Broken !!")
    elif stress_index > 70:
        return(f"Stress Index: {stress_index}%  [! HIGH PANIC ]")
    elif stress_index > 40:
        return(f"Stress Index: {stress_index}%  [~ MODERATE ]")
    else:
        return(f"Stress Index: {stress_index}%  [+ CALM]")

# Calculate the risk status for the animal
def check_risk(body_temp, temp_min, temp_max, heart_rate, hr_min, hr_max, oxygen, stress_index):

    if (oxygen >= 95):
        oxygen_risk = 0
    elif (oxygen >= 90):
        oxygen_risk = 40
    elif (oxygen >= 85):
        oxygen_risk = 70
    else:
        oxygen_risk = 100

    if (body_temp > temp_max + 1.0) or (body_temp < temp_min - 1.0):
        body_temp_risk = 100
    elif (body_temp > temp_max + 0.4) or (body_temp < temp_min - 0.4):
        body_temp_risk = 80
    elif (body_temp > temp_max) or (body_temp < temp_min):
        body_temp_risk = 45
    else:
        body_temp_risk = 0

    if (heart_rate > hr_max + 20) or (heart_rate < hr_min - 20):
        heart_rate_risk = 100
    elif (heart_rate > hr_max + 10) or (heart_rate < hr_min - 10):
        heart_rate_risk = 70
    elif (heart_rate > hr_max) or (heart_rate < hr_min):
        heart_rate_risk = 35
    else:
        heart_rate_risk = 0

    risk_index = (oxygen_risk * 0.40) + (body_temp_risk * 0.30) + (heart_rate_risk * 0.15) + (stress_index * 0.15)

    return(risk_index)

# Determine action plan to recommend based on risk status
def get_action_plan(risk_status):
    if (risk_status >= 75):
        return ("Risk Level: CRITICAL", "Action Directive: Dispatch immediate veterinary and rescue unit")
    elif (risk_status >= 50):
        return ("Risk Level: HIGH", "Action Directive: Deploy field rangers for inspection")
    elif (risk_status >= 25):
        return ("Risk Level: MODERATE", "Action Directive: Monitor more frequently")
    else:
        return ("Risk Level: LOW", "Action Directive: Maintain background check")   
    

# This will determine what tuple we will use from dummy data
current_index = 0
# This is the code block that will execute our program
def make_line(text):
    return f"| {text:<{68}} |"
while True:
    animal_id = input("Enter Animal ID (or 0 to exit): ")
    if (animal_id == "0"):
        print("Exiting program.")
        break

    species = input("Enter animal species: ").lower()

    if (species) in (species_ranges):
        selected_reading = sticker_data[current_index]
        result = process_sticker(species, selected_reading)

        (body_temp, temp_status, heart_rate, hr_status, oxygen, oxygen_status, battery_status, stress_status, latitude, longitude, risk_status, gel_status, actions) = result
        # CREATE THE OUTPUT OVERLAY LATER
        print()
        print("|"+"=" * 70 +"|")
        print(make_line("                               ECHOTRACE"))
        print("|"+"=" * 70 +"|")
        print(make_line(f" Animal Selected - {species.upper()} | ID - {animal_id} "))
        print("|"+"=" * 70 +"|")
        print(make_line(" - Current Status (LIVE) - "))
        print(make_line(f"  • {temp_status} "))
        print(make_line(f"  • {hr_status} "))
        print(make_line(f"  • {stress_status} "))
        print(make_line(f"  • {oxygen_status} "))
        print(make_line(f"  • Cooling Gel Status: {gel_status} ")) # Make this formatted
        print(make_line(f"  • Current Risk Level: {risk_status} ")) # Make this formatted
        if (latitude) < (-90) or (longitude) < (-180) or (latitude) > (90) or (longitude) > (180):
            print(make_line(" !! GPS Sensor Broken !! "))
        else:
            print(make_line(f"  • Location: Latitude - {latitude}° N | Longitude - {longitude}° E ")) # Add symbols next to the long/lati
        print(make_line(f"  • {battery_status} "))

        risk_text, action_text = actions
        print(make_line(f"  • {risk_text} "))
        print(make_line(f"  • {action_text}"))
        print("|"+"=" * 70 +"|")
        print()
        # Cycle to the next tuple in our dummy data list
        current_index = (current_index + 1) % len(sticker_data)
    elif (species) not in (species_ranges):
        print(f"Species '{species}' not recognized, try again.")
