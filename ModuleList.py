from HostUserIOModule import HostUserIOModule
from Webportal_Module import Webportal
from Camera_Module import CameraDriver


module_list = [
    HostUserIOModule.__module_info__(),
    Webportal.__module_info__(),
    CameraDriver.__module_info__()
]
