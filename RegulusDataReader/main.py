import yaml
import time
import requests

file_path = '/usr/src/app/config.yaml'
#file_path = './RegulusDataReader/config.yaml'

# Global
interval = 1

def read_config():
    with open(file_path, 'r') as config_file:
        config = yaml.safe_load(config_file)

    global interval
    interval = config['options'].get('interval')
    print("interval:", interval)

def read_xml():
    url = 'https://regulusroute.tecomat.com/HOME.XML'
    response = requests.get(url)
    xml_content = response.text

    # Print XML content
    print(xml_content)
    

if __name__ == '__main__':

    read_config()
    while True:
        
        read_xml()

        time.sleep(interval)
    
