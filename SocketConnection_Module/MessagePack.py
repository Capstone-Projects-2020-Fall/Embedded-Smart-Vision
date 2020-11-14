
from socket import socket


# Helper function to read and reconstruct bytes that may have been coalesced by the socket
def get_bytes(cnt: int, conn: socket):
    buf_size = 4096
    remaining_bytes = cnt
    data = bytearray()
    while True:
        if remaining_bytes < buf_size:
            # If we have less bytes remaining
            # to receive then the buffer size receive only those bytes
            tmp = conn.recv(remaining_bytes)
            data.extend(tmp)
            break
        else:
            # If we are still taking full buffers take full buffers
            data += conn.recv(buf_size)
            # Keep track of how many bytes we have consumed
            remaining_bytes = remaining_bytes - buf_size

    return data
