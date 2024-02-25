import requests
import json
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import os
import datetime
import xml.etree.ElementTree as ET

DEF_FODLER = 'usr/src/app/'

def send_temperatures():
    guid = read_config('guid')
    get_objects_url = 'https://dphajek-windows.azurewebsites.net/Api/Regulus/GetAllObjects'
    try:
        print_log("Downloading regulus objects", "send_temperatures")
        response = requests.get(get_objects_url)
        objects = response.text
    except Exception as e:
        print_log("Failed to download regulus objects " + str(e), "send_temperatures")
        return

    set_regulus_objects_url = 'https://dphajek-windows.azurewebsites.net/Api/Regulus/SetObjectData'
    for object in objects:
        try:
            url = object['url']
            response = requests.get(url)
            code = object['code']
            xml_data = response.text
            root = ET.fromstring(xml_data)
            diag = root.find(".//*[@NAME='{}']".format(code))
            post_data = {
                'guid': guid,
                'code': object['code'],
                'value': diag.attrib['VALUE']
            }
            response = requests.post(set_regulus_objects_url, data=post_data)
            print_log("Temperature sent for object: " + code + "(" + str(post_data) + ", " + str(response.status_code) + ")", "send_temperatures")
        except Exception as e:
            print_log("Failed to send temperatures for object: " + code + " " + str(e), "send_temperatures")

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

    scheduler = BlockingScheduler()
    scheduler.add_job(send_temperatures, 'cron', minute='0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59')

    scheduler.start()
    