#------------------------------------------------
from configparser import ConfigParser
import json
import os
from typing import List
#------------------------------------------------
class Config:
    calendar_ics_file_path = ""

    def read_configuration_files(path) -> List[ConfigParser]:
        conf_file_list = []

        for filename in os.listdir(path):
            if filename.endswith(".ini"):
                config_parser = ConfigParser()
                config_parser.read(os.path.join(path, filename))
                conf_file_list.append(config_parser)

        return conf_file_list

    def from_ini_to_json(ini_file_path):
        config = ConfigParser()
        config.read(ini_file_path)

        config_dict = {}
        for section in config.sections():
            config_dict[section] = dict(config.items(section))

        # Convert the dictionary to JSON format
        json_data = json.dumps(config_dict)

        return json_data

    def from_json_to_ini(json_obj, ini_file_path):
        json_data = json_obj

        config_dict = json.loads(json_data)

        config = ConfigParser()

        # Write dictionary data to ConfigParser
        for section, options in config_dict.items():
            config.add_section(section)
            for option, value in options.items():
                config.set(section, option, str(value))

        with open(ini_file_path, 'w') as config_file:
            config.write(config_file)