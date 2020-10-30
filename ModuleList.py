from HostUserIOModule import HostUserIOModule
from Camera_Module import CameraDriver
from Classification_Module import ClassificationDriver
from Webportal_Module import WebDriver


module_list = [
    HostUserIOModule.__module_info__(),
    CameraDriver.__module_info__(),
    ClassificationDriver.__module_info__(),
    WebDriver.__module_info__()
]
