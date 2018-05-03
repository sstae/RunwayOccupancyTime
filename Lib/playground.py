from Lib import Util
from Lib import Config
import os
import pprint

Util.test('Hello')
current_path = os.path.dirname(os.path.abspath(__file__))
pp = pprint.PrettyPrinter(indent=4)

# initial config
all_config = Config.initial_config(current_path, './../config.txt')
print("config:")
pp.pprint(all_config)
