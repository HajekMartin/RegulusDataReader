import yaml
import time
import requests

def read_config():
    file_path = '/usr/src/app/config.yaml'
    #file_path = './RegulusDataReader/config.yaml'
    with open(file_path, 'r') as config_file:
        config = yaml.safe_load(config_file)

    interval = config['options'].get('interval')
    print("interval:", interval)

def read_xml():
    url = 'https://regulusroute.tecomat.com/HOME.XML'
    
    print(f"Reading XML {time}")
    response = requests.get(url)
    xml_content = response.text

    # Print XML content
    print(xml_content)

if __name__ == '__main__':
    read_config()
    while True:
        read_xml()

        time.sleep(1)