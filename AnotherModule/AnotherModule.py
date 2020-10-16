# Runs the modules functionality
def __load__(conn):
    # print("Loading Another module!")
    pass


# Returns a dictionary containing information that describes the module
def __module_info__():
    return {"version": 1,
            "name": "Another Module",
            "entry_point": __load__,
            # The code used to issue messages and establish pipes to the module
            "message_code": "ANM",
            }
