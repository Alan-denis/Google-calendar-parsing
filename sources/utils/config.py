#------------------------------------------------
from configparser import ConfigParser
import os
from typing import List
#------------------------------------------------

def read_configuration_files(path) -> List[ConfigParser]:
    conf_file_list = []

    for filename in os.listdir(path):
        if filename.endswith(".ini"):
            config_parser = ConfigParser()
            config_parser.read(os.path.join(path, filename))
            conf_file_list.append(config_parser)

    return conf_file_list

