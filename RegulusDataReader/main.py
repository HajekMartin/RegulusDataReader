import yaml

with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

external_hostname = next((item for item in config['options'] if item['name'] == 'external_hostname'), None)
print(external_hostname)
additional_hosts = next((item for item in config['options'] if item['name'] == 'additional_hosts'), None)
print(additional_hosts)

# Print the details of the 'username' option
if external_hostname is not None:
    print(external_hostname)
else:
    print("Username option not found")

print(f"Test print!")
