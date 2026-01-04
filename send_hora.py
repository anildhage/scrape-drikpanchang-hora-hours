hora_data = {
  "date": "04/01/2026",
  "location": "Brossard",
  "running_hora": "Jupiter - Fruitful",
  "horas": [
    {
      "row": 1,
      "hora": "Sun",
      "time_12hr": "Sun - Vigorous07:34AMto08:18AM",
      "time_24hr": "07:34-08:18"
    },
    {
      "row": 2,
      "hora": "Venus",
      "time_12hr": "Venus - Beneficial08:18AMto09:02AM",
      "time_24hr": "08:18-09:02"
    },
    {
      "row": 3,
      "hora": "Mercury",
      "time_12hr": "Mercury - Quick09:02AMto09:46AM",
      "time_24hr": "09:02-09:46"
    },
    {
      "row": 4,
      "hora": "Moon",
      "time_12hr": "Moon - Gentle09:46AMto10:30AM",
      "time_24hr": "09:46-10:30"
    },
    {
      "row": 5,
      "hora": "Saturn",
      "time_12hr": "Saturn - Sluggish10:30AMto11:15AM",
      "time_24hr": "10:30-11:15"
    },
    {
      "row": 6,
      "hora": "Jupiter",
      "time_12hr": "Jupiter - Fruitful11:15AMto11:59AM",
      "time_24hr": "11:15-11:59"
    },
    {
      "row": 7,
      "hora": "Mars",
      "time_12hr": "Mars - Aggressive11:59AMto12:43PM",
      "time_24hr": "11:59-12:43"
    },
    {
      "row": 8,
      "hora": "Sun",
      "time_12hr": "Sun - Vigorous12:43PMto01:27PM",
      "time_24hr": "12:43-13:27"
    },
    {
      "row": 9,
      "hora": "Venus",
      "time_12hr": "Venus - Beneficial01:27PMto02:12PM",
      "time_24hr": "13:27-14:12"
    },
    {
      "row": 10,
      "hora": "Mercury",
      "time_12hr": "Mercury - Quick02:12PMto02:56PM",
      "time_24hr": "14:12-14:56"
    },
    {
      "row": 11,
      "hora": "Moon",
      "time_12hr": "Moon - Gentle02:56PMto03:40PM",
      "time_24hr": "14:56-15:40"
    },
    {
      "row": 12,
      "hora": "Saturn",
      "time_12hr": "Saturn - Sluggish03:40PMto04:24PM",
      "time_24hr": "15:40-16:24"
    },
    {
      "row": 13,
      "hora": "Jupiter",
      "time_12hr": "Jupiter - Fruitful04:24PMto05:40PM",
      "time_24hr": "16:24-17:40"
    },
    {
      "row": 14,
      "hora": "Mars",
      "time_12hr": "Mars - Aggressive05:40PMto06:56PM",
      "time_24hr": "17:40-18:56"
    },
    {
      "row": 15,
      "hora": "Sun",
      "time_12hr": "Sun - Vigorous06:56PMto08:12PM",
      "time_24hr": "18:56-20:12"
    },
    {
      "row": 16,
      "hora": "Venus",
      "time_12hr": "Venus - Beneficial08:12PMto09:27PM",
      "time_24hr": "20:12-21:27"
    },
    {
      "row": 17,
      "hora": "Mercury",
      "time_12hr": "Mercury - Quick09:27PMto10:43PM",
      "time_24hr": "21:27-22:43"
    },
    {
      "row": 18,
      "hora": "Moon",
      "time_12hr": "Moon - Gentle10:43PMto11:59PM",
      "time_24hr": "22:43-23:59"
    },
    {
      "row": 19,
      "hora": "Saturn",
      "time_12hr": "Saturn - Sluggish11:59PMto01:15AM,Jan 05",
      "time_24hr": "23:59-01:15"
    },
    {
      "row": 20,
      "hora": "Jupiter",
      "time_12hr": "Jupiter - Fruitful01:15AMto02:30AM,Jan 05",
      "time_24hr": "01:15-02:30"
    },
    {
      "row": 21,
      "hora": "Mars",
      "time_12hr": "Mars - Aggressive02:30AMto03:46AM,Jan 05",
      "time_24hr": "02:30-03:46"
    },
    {
      "row": 22,
      "hora": "Sun",
      "time_12hr": "Sun - Vigorous03:46AMto05:02AM,Jan 05",
      "time_24hr": "03:46-05:02"
    },
    {
      "row": 23,
      "hora": "Venus",
      "time_12hr": "Venus - Beneficial05:02AMto06:18AM,Jan 05",
      "time_24hr": "05:02-06:18"
    },
    {
      "row": 24,
      "hora": "Mercury",
      "time_12hr": "Mercury - Quick06:18AMto07:33AM,Jan 05",
      "time_24hr": "06:18-07:33"
    }
  ]
}


from datetime import datetime
import json  # Optional: if loading from JSON string/file

def get_current_hora(data, current_time_str=None):
    if current_time_str is None:
        current_time = datetime.now().strftime('%H:%M')
    else:
        current_time = current_time_str
    
    current_h = int(current_time.split(':')[0])
    current_m = int(current_time.split(':')[1])
    
    for hora_entry in data['horas']:
        time_range = hora_entry['time_24hr']
        start_str, end_str = time_range.split('-')
        
        # Parse flexibly
        if ':' in start_str:
            sh, sm = map(int, start_str.split(':'))
        else:
            sh = int(start_str[:-2])
            sm = int(start_str[-2:])
        
        if ':' in end_str:
            eh, em = map(int, end_str.split(':'))
        else:
            eh = int(end_str[:-2])
            em = int(end_str[-2:])
        
        # Overnight check
        if eh < sh or (eh == sh and em < sm):
            if (current_h >= sh and (current_m >= sm or current_h > sh)) or \
               (current_h < eh or (current_h == eh and current_m <= em)):
                return hora_entry['hora'], hora_entry['time_12hr'], current_time
        else:
            if sh <= current_h <= eh and \
               (current_h > sh or current_h == sh and current_m >= sm) and \
               (current_h < eh or current_h == eh and current_m <= em):
                return hora_entry['hora'], hora_entry['time_12hr'], current_time
    
    return None, None, current_time



# Current time now
print(get_current_hora(hora_data))  # Uses datetime.now()

# Specific time (e.g., 17:26)
print(get_current_hora(hora_data, '05:03'))  # 'Jupiter'

# From JSON file/string
# with open('hora.json') as f: data = json.load(f)
# print(get_current_hora(data, '22:00'))  # 'Moon'
