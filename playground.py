from Lib import Util
from Lib import Config
import os
import pprint
# import FlightSeparator

print('hello')
Util.test('world')

current_path = os.path.dirname(os.path.abspath(__file__))
pp = pprint.PrettyPrinter(indent=4)

# initial config
all_config = Config.initial_config(current_path, 'config.txt')
print("config:")
pp.pprint(all_config)

# aircraft = {}
# input_file = os.path.join(all_config['input_raw_data'], "data.csv.2018032214")
# FlightSeparator.process_file(all_config, aircraft, input_file)


# cb = Util.CircularBuffer(size=10)
# for i in range(20):
#     cb.append(i)
#     print ("@%s, Average: %s" ,cb, cb.average)
#
# x = Util.CircularBuffer(size=10)
# for i in range(20):
#     x.append(str(i))
#     print("@%s ", x)
#     if '1' not in x:
#         print ('1 not in x')
#     if '6' not in x:
#         print ('6 not in x')