# Contains information for reading in the general configuration as well as saving and updating config variables

import json


class config_tags:
    def __init__(self):
        pass

    CFG_GET = "cfg_get"
    CFG_SET = "cfg_set"


# Wrapper class to contain the information about a config update we want to do
class cfg_transaction:
    def __init__(self, key, data, set=True, reply=-1):
        # Which key do we want to access
        self.key = key
        # What do we want to set it to
        self.data = data
        self.set = set
        self.reply = reply


class Config:
    def __init__(self):
        self.vars = {}
        self.config_path = "config.json"

    def print_vars(self):
        print(self.vars)

    # Set a config variable
    def var_transaction(self, data: cfg_transaction):
        print(data.key)
        if data.set:
            if data.key in self.vars:
                # if the key in the data is a valid variable
                self.vars[data.key] = data.data
                with open(self.config_path, 'w') as outFile:
                    json.dump(self.vars, outFile)
        else:
            if data.key in self.vars:
                if data.reply == -1:
                    print("Error: attempting to get a variable without a reply pipe")
                else:
                    data.reply.send(self.vars[data.key])

    def load_config(self):
        print("Loading configuration...")
        with open(self.config_path) as read_file:
            self.vars = json.load(read_file)
