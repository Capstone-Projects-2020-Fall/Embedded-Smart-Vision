from Camera_Module import CameraDriver
from Classification_Module import ClassificationDriver
from Webportal_Module import WebDriver
from SocketConnection_Module import SocketClient_Module

module_list = [
    CameraDriver.__module_info__(),
    ClassificationDriver.__module_info__(),
    WebDriver.__module_info__(),
    SocketClient_Module.__module_info__()
]
