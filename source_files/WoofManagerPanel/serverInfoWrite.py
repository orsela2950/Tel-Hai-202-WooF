import json
import os
import filelock
from typing import Dict, Any

# File usage:
current_dir = os.path.dirname(os.path.realpath(__file__))
server_properties_dir = os.path.join(current_dir, '..', 'WoofSourceFiles')
server_properties_name = 'server_properties.json'

def set_settings_json_argument(new_args_dict: Dict[str, Any]):
    """Writes a settings key-value pairs to the server_properties.json file, ensuring file integrity and consistency.

    Args:
        key (str): The key to be updated.
        value: The new value to be assigned to the key.
        @param new_args_dict:
    """

    with filelock.FileLock(os.path.join(server_properties_dir,
                                        server_properties_name+'.lock')):  # Acquire a lock to prevent race conditions
        with open(os.path.join(server_properties_dir, server_properties_name),
                  'r+') as f:  # Open file for reading and writing
            try:
                data = json.load(f)  # Load existing JSON data

                for key in new_args_dict:
                    data[key] = new_args_dict[key]  # Update the value for the specified key

                f.seek(0)  # Move the file pointer to the beginning
                f.truncate()
                json.dump(data, f, indent=4)  # Write the updated data back to the file in a readable format
            except json.JSONDecodeError:
                print('Cant find "server_properties.json" file for changing proparties exiting...')
                exit(1)

def set_rules_json_argument(new_args_dict: Dict[str, Any]):
    """Writes a rules key-value pair to the server_properties.json file, ensuring file integrity and consistency.
    sets all rules to false and then sets the rules that are in the dict to true
    Args:
        key (str): The key to be updated.
        value: The new value to be assigned to the key.
        @param new_args_dict:
    """
    with filelock.FileLock(os.path.join(server_properties_dir,
                                        server_properties_name+'.lock')):  # Acquire a lock to prevent race conditions
        with open(os.path.join(server_properties_dir, server_properties_name),
                  'r+') as f:  # Open file for reading and writing
            try:
                data = json.load(f)  # Load existing JSON data
                for key in data["rules"]:
                    data["rules"][key] = False
                for key in new_args_dict:
                    data["rules"][key] = True  # Update the value for the specified key

                f.seek(0)  # Move the file pointer to the beginning
                f.truncate()
                json.dump(data, f, indent=4)  # Write the updated data back to the file in a readable format
            except json.JSONDecodeError:
                print('Cant find "server_properties.json" file for changing proparties exiting...')
                exit(1)


if __name__ == '__main__':
    # tests
    # newdict = {'ip': 'new ip xd'}
    # set_settings_json_argument(newdict)
    d = {'DDOS': 'on'}
    set_rules_json_argument(d)
