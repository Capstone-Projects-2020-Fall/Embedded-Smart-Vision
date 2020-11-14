import struct

from .MessageWrappers.CommandMessage import StreamCommand, CommandMessage, CmdTypes


# Helper function to strip off the first "cnt" bytes from a byte array and remove them from the remaining array
def strip_bytes(cnt, data):
    if cnt > len(data) or cnt <= 0:
        print("Requested data out of bounds!")
        return b'', data

    stripped_bytes = data[0:cnt]
    data = data[cnt:]

    return stripped_bytes, data


# Parse raw bytes to a stream command
def bytes_to_stream_command(raw_data):
    mode, raw_data = strip_bytes(4, raw_data)
    mode = struct.unpack('i', mode)[0]

    result = StreamCommand(mode)
    return result


# Parse raw bytes into a command message
def bytes_to_command(raw_data):
    # strip the first 4 bytes off to figure out the command type
    cmd_type, raw_data = strip_bytes(4, raw_data)

    # Recover the command type
    cmd_type = CmdTypes(struct.unpack('i', cmd_type)[0])

    if cmd_type == CmdTypes.STREAM_COMMAND:
        # We are parsing a stream command
        return bytes_to_stream_command(raw_data)
    else:
        print("BYTES_TO_COMMAND: UNKNOWN COMMAND TYPE PASSED IN")


def stream_command_to_bytes(str_cmd: StreamCommand):
    command_type = struct.pack('i', int(CmdTypes.STREAM_COMMAND))
    mode = struct.pack('i', str_cmd.mode)
    data = b''
    data = command_type + mode
    return data


# Turn a command message into raw bytes
def command_to_bytes(cmd):
    if cmd.command_type == CmdTypes.STREAM_COMMAND:
        # We are making a stream so pass it over to the proper function
        return stream_command_to_bytes(cmd)


def message_to_bytes(data):
    # If we are requesting to change a command message into bytes
    if isinstance(data, CommandMessage):
        return command_to_bytes(data)
