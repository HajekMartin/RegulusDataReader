import requests
import json
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import os
import datetime

DEF_FODLER = 'usr/src/app/'

def send_temperatures():
    url = read_config("url")
    guid = read_config("guid")
    regulus_url = read_config("regulus_url")
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    regulus_url = regulus_url + "/SDC/Datalog/teploty/" + yesterday.strftime('%Y/%m/%d') + "000000.CSV"

    # Download CSV file
    print_log("Downloading CSV file from " + regulus_url, "send_temperatures")
    response = requests.get(regulus_url)
    if response.status_code == 200:
        print_log("CSV file downloaded successfully", "send_temperatures")
        csv_data = response.content

        # Send CSV data via POST
        data = {'csvData': csv_data, 'guid': guid, 'date': yesterday.strftime('%Y-%m-%d')}
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print_log("CSV file sent successfully", "send_temperatures")
        else:
            print_log("Failed to send CSV file", "send_temperatures")
    else:
        print_log("Failed to download CSV file", "send_temperatures")

    

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
    send_temperatures()
    scheduler = BlockingScheduler()
    scheduler.add_job(send_temperatures, 'cron', hour=1, minute=0)

    scheduler.start()
    