import unittest
from janus import Janus
from datetime import datetime, timedelta

class TestStringMethods(unittest.TestCase):

    def create_raw_data_1(self):
        d = []
        skip = False
        i = 1
        dec = 150

        while i < 150:
            date = (datetime.today().date() - timedelta(dec)).strftime('%m/%d/%Y')
            
            d.append({'Day': date, 'Value': i})
            
            dec -= 1

            if not skip:
                i += 1
                skip = True
            else:
                i += 2
                skip = False

        return d

    def create_raw_data_2(self):
        d = []
        i = 1
        dec = 150

        for i in range(150):
            date = (datetime.today().date() - timedelta(dec)).strftime('%m/%d/%Y')
            
            d.append({'Day': date, 'Value': i * i})

            dec -= 1

        return d

    def test_janus_1(self):
        df = self.create_raw_data_1()

        ai = Janus(df, 'Value')

        ai.launch_janus()

        predicted = ai.predict_next_value()
        
        test = float(predicted) > 150

        self.assertEqual(ai.is_model_trained, True)

    def test_janus_2(self):
        df = self.create_raw_data_2()

        ai = Janus(df, 'Value')

        ai.launch_janus()

        predicted = ai.predict_next_value()
        
        test = float(predicted) > 150

        self.assertEqual(ai.is_model_trained, True)

if __name__ == '__main__':
    unittest.main()