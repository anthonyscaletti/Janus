#!/usr/local/bin/python

import sys
import json
from datetime import datetime, timedelta
from janus import Janus

def generate_predicted_days(days, day_count):
    d = []

    for i in range(day_count):
        date = (datetime.strptime(days[len(days) - 1], '%m/%d/%Y') + timedelta(i + 1)).strftime('%m/%d/%Y')       
        d.append(date)

    return d

if __name__ == "__main__":
    #Convert To JSON
    data_json = json.loads(sys.argv[1])

    #Initialize Janus
    janus = Janus(data_json, 'y')

    #Execute Janus
    janus.launch_janus()

    #Return Predicted Values
    day_count = data_json['dayCount']
    result = {'x': generate_predicted_days(data_json['x'], day_count), 'y': janus.predict_next_values(day_count), 'dayCount': day_count}
    
    print(json.dumps(result))