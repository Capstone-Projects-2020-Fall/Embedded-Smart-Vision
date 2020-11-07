
class QueueMessage:
    def __init__(self,
                 node_origin="NOT SET",
                 msg_package=None):

        # The name of the node that this message is from
        self.node_origin = node_origin
        # The actual message package
        self.msg_package = msg_package

    def print_message_content(self):
        print("\nOrigin node: ",
              self.node_origin,
              "\n",
              "message type: ",
              self.msg_package.header.messageType)
