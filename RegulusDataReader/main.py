import yaml
import time

def read_config():
    file_path = '/usr/src/app/config.yaml'
    #file_path = './RegulusDataReader/config.yaml'

    with open(file_path, 'r') as config_file:
        config = yaml.safe_load(config_file)

    interval = config['options'].get('interval')
    print("interval:", interval)

if __name__=='__main__':
    read_config()

    while True:
        print("I'm alive!")
        time.sleep(60)