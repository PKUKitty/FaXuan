import json


class Config:
    __CONFIG_FILE__ = "/home/yujun/PycharmProjects/FaXuan/fx_login.conf"

    json_config_obj = None

    def __init__(self):
        self.read_config()
        pass

    def read_config(self):
        config_file = open(self.__CONFIG_FILE__)
        self.json_config_obj = json.load(config_file)
        config_file.close()

    @staticmethod
    def get_str(self, section, key):
        return self.json_config_obj[section][key]

    @staticmethod
    def get_int(self, section, key):
        return int(self.json_config_obj[section][key])
