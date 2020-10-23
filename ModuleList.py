from ExampleModule import ExampleModule
from AnotherModule import AnotherModule
from HostUserIOModule import HostUserIOModule
from Webportal import Webportal
from Camera_Module import CameraDriver


module_list = [
    ExampleModule.__module_info__(),
    HostUserIOModule.__module_info__(),
    Webportal.__module_info__(),
    CameraDriver.__module_info__()
]
