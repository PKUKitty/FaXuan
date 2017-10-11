import json
import threading


class Config:
    __CONFIG_FILE__ = "/home/yujun/PycharmProjects/FaXuan/fx_login.conf"

    __json_config_obj = None

    __instance = None

    mutex = threading.Lock()

    def __init__(self):
        self.read_config()

    @staticmethod
    def get_instance():
        if Config.__instance is None:
            Config.mutex.acquire()
            if Config.__instance is None:
                Config.__instance = Config()
            Config.mutex.release()
        return Config.__instance

    def read_config(self):
        config_file = open(Config.__CONFIG_FILE__)
        self.__json_config_obj = json.load(config_file)
        config_file.close()

    def get_str(self, section, key):
        return self.__json_config_obj[section][key]

    def get_int(self, section, key):
        return int(self.__json_config_obj[section][key])

    def get_long(self, section, key):
        return long(self.__json_config_obj[section][key])
