# This is the interface used to send network messages to the central server
from SocketConnection_Module.NetworkSendMessage import NetworkSendMessage, NSM_TYPE


class NetworkMessageInterface:
    def __init__(self, queue_call_back):
        self.queue_call_back = queue_call_back


    def send_test_message(self, data):
        print("sending test message")
        nsm = NetworkSendMessage(message_type=NSM_TYPE.TEST_MESSAGE, var1=data)
        self.queue_call_back(nsm)

    # Send a video over the socket to the central server
    def send_video(self, link):
        print("Sending video")
        nsm = NetworkSendMessage(message_type=NSM_TYPE.SEND_VIDEO, var1=link)
        self.queue_call_back(nsm)
        pass

    def handle_network_message(self, sub_tag, data):
        print("Handling network message in interface")
        if sub_tag == 'send_test_message':
            self.send_test_message(data)
        elif sub_tag == 'send_video':
            self.send_video(data)
