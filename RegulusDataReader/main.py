import yaml
import time

if __name__=='__main__':
    file_path = '/usr/src/app/config.yaml'
    #file_path = './RegulusDataReader/config.yaml'

    with open(file_path, 'r') as config_file:
        config = yaml.safe_load(config_file)

    interval = config['options'].get('interval')

    print("interval:", interval)

    while True:
        print("I'm alive!")
        time.sleep(interval)