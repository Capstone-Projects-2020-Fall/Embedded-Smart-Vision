from Camera_Module import CameraDriver
from Classification_Module import ClassificationDriver
from Webportal_Module import WebDriver
from Action_Module import ActionDriver


module_list = [
    CameraDriver.__module_info__(),
    ClassificationDriver.__module_info__(),
    WebDriver.__module_info__(),
    #ActionDriver.__module_info__()
]
