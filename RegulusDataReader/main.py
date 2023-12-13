import yaml
import time
import requests

print("Starting RegulusDataReader...")
"""
Reading config
"""
file_path = '/usr/src/app/config.yaml'
#file_path = './RegulusDataReader/config.yaml'
with open(file_path, 'r') as config_file:
    config = yaml.safe_load(config_file)

interval = config['options'].get('interval')
print("interval:", interval)


"""
While loop
"""
    
while True:
    print(f"Reading XML {time.ctime()}")
    time.sleep(interval)