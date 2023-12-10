print("Username option not found")
exit(1)

import yaml

with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# Find the 'username' option in the list
username_option = next((item for item in config['options'] if item['name'] == 'username'), None)

# Print the details of the 'username' option
if username_option is not None:
    print(username_option)
else:
    print("Username option not found")

print(f"Test print!")
