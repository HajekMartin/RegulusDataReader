import yaml
import time

#file_path = '/usr/src/app'
file_path = './RegulusDataReader/config.yaml'

with open(file_path, 'r') as config_file:
    config = yaml.safe_load(config_file)

interval = config['options'].get('interval')

print("interval:", interval)

while True:
    print("I'm alive!")
    time.sleep(interval)
