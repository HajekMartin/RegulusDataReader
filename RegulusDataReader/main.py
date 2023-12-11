import yaml
import time
import uuid

print ("The MAC address in formatted way is : ", end="")
print (':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
for ele in range(0,8*6,8)][::-1]))

file_path = '/usr/src/app'
#file_path = './RegulusDataReader/config.yaml'

with open(file_path, 'r') as config_file:
    config = yaml.safe_load(config_file)

interval = config['options'].get('interval')

print("interval:", interval)

while True:
    print("I'm alive!")
    time.sleep(interval)
    
