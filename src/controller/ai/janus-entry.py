#!/usr/local/bin/python

import sys
import json
from janus import Janus

if __name__ == "__main__":
    #Convert To JSON
    dataJson = json.loads(sys.argv[1])

    #Initialize Janus
    janus = Janus(dataJson, 'y')

    #Execute Janus
    janus.launch_janus()

    #Return Predicted Values
    result = {'x': ["20200512"], 'y': janus.predict_next_value(), 'dayCount': 1}
    
    print(json.dumps(result))