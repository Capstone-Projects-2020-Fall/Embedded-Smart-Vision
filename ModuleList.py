from ExampleModule import ExampleModule
from AnotherModule import AnotherModule
from HostUserIOModule import HostUserIOModule

module_list = [
    AnotherModule.__module_info__(),
    HostUserIOModule.__module_info__(),
    Camera_Module.__module_info__()
]
