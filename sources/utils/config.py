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

        config_dict["DEFAULT"] = dict(config.items('DEFAULT'))

        for section in config.sections():
            tmp_dict = {}

            for key in config[section].keys():
                tmp_dict.update({key: config.get(section, key)})
            
            config_dict[section] = tmp_dict

        # Convert the dictionary to JSON format
        json_data = json.dumps(config_dict)

        return json_data

    def from_json_to_ini(json_obj, output_ini_file_path):
        config_dict = json.loads(json_obj)
        config = ConfigParser()
        
        default_options = config_dict.pop('DEFAULT', None)
        if default_options:
            with open(output_ini_file_path, 'w') as config_file:
                config_file.write('[DEFAULT]\n')
                for option, value in default_options.items():
                    config_file.write(f"{option} = {value}\n")
                config_file.write('\n')

        for section, options in config_dict.items():
            config.add_section(section)

            for option, value in options.items():
                if option not in default_options:
                    config.set(section, option, str(value))

        with open(output_ini_file_path, 'a') as config_file:
            config.write(config_file)