from Camera_Module import CameraDriver
from Classification_Module import ClassificationDriver
from Webportal_Module import WebDriver


module_list = [
    CameraDriver.__module_info__(),
    ClassificationDriver.__module_info__(),
    WebDriver.__module_info__()
]
