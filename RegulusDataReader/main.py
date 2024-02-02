import requests
import json
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import os
import datetime
import xml.etree.ElementTree as ET

DEF_FODLER = 'usr/src/app/'

def download_heated_zones():
    try:
        print_log("Downloading heated zones", "download_heated_zones")
        url = read_config("heated_zones_list_url")
        response = requests.get(url, data={'guid': read_config('guid')})
        data = response.json()
        save_to_file(data)  # Save the heated zones to a file
        print_log("Heated zones downloaded", "download_heated_zones")
        return data
    except Exception as e:
        print_log("Failed to download heated zones: " + str(e), "download_heated_zones")
        return None

def save_to_file(data):
    file_path = DEF_FODLER + 'heated_zones.json'
    with open(file_path, 'w') as file:
        file.write(json.dumps(data))
        print_log("Heated zones saved to file", "save_to_file")

def read_from_file(file_name):
    try:
        print_log("Reading from file " + file_name, "read_from_file")
        file_path = DEF_FODLER + file_name
        with open(file_path) as file:
            data = json.load(file)
            print_log("Data read from file", "read_from_file")
            return data
    except Exception as e:
        print_log("Failed to read from file: " + str(e), "read_from_file")
        return None

def send_temperatures():
    guid = read_config('guid')
    heated_zones_temperatures_url = read_config('heated_zones_temperatures_url')
    try:
        print_log("Sending temperatures", "send_temperatures")
        heated_zones = read_from_file('heated_zones.json')
        for heated_zone in heated_zones:
            url = heated_zone['url']
            response = requests.get(url)
            xml_data = response.text
            root = ET.fromstring(xml_data)
            diag = root.find(".//*[@name='{}']".format(heated_zone['code']))
            post_data = {
                'guid': guid,
                'code': heated_zone['code'],
                'attribute_value': diag.attrib['value']
            }
            response = requests.post(heated_zones_temperatures_url, data=post_data)
            print_log("Temperature sent for zone: " + heated_zone['code'], "send_temperatures")
    except Exception as e:
        print_log("Failed to send temperatures: " + str(e), "send_temperatures")

def read_config(value_name):
    try:
        print_log("Reading config " + value_name, "read_config")
        file_path = 'data/' + 'options.json'
        
        with open(file_path) as file:
            data = json.load(file)
            if value_name in data:
                value = data[value_name]
                print_log("Config " + value_name + " = " + value, "read_config")
                return value
            else:
                raise Exception("Value not found")
    except Exception as e:
        print_log("Failed to read config: " + str(e), "read_config")
        return None

def print_log(message, method):
    string = "[ " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " ] " + method + " " + message
    create_log_file()
    
    log_file = DEF_FODLER + 'logs/' + datetime.datetime.now().strftime("%Y-%m-%d") + '.log'
    with open(log_file, 'a') as file:
        file.write(string + '\n')
    
def create_log_file():
    log_folder = DEF_FODLER + 'logs/'
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    
    log_file = log_folder + datetime.datetime.now().strftime("%Y-%m-%d") + '.log'
    if not os.path.exists(log_file):
        with open(log_file, 'w') as file:
            pass

if __name__ == '__main__':
    print_log("Starting RegulusDataReader", "main")

    download_heated_zones()

    scheduler = BlockingScheduler()
    scheduler.add_job(send_temperatures, 'cron', minute='0,15,30,45')

    scheduler.start()
    