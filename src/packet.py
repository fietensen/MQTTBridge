from typing import Optional, Tuple
import socket
import asyncio

"""
Packet class that receives MQTT Packets from a socket connection and parses them
"""
class Packet(object):
    def __init__(self, data: bytes) -> None:
        self.__data = data


    """
    Returns the MQTT Packet's raw byte data
    """
    def as_bytes(self) -> bytes:
        return self.__data


    async def _read_remaining_length(connection: socket.socket, event_loop: asyncio.AbstractEventLoop) -> Tuple[int, bytes]:
        remaining_length = 0
        rl_data = b""

        # mqtt packets use variable-size encoding for the remaining packet
        # size. The maximum length is 4 bytes though. We just break out
        # in case the current byte is the last one. (MSB unset)
        for i in range(4):
            byte = await event_loop.sock_recv(connection, 1)
            rl_data += byte
            value = ord(byte)

            # discard msb because it holds the info for variable-size encoding
            remaining_length += (value & 0b0111_1111) << (7 * i)
            
            if value & 0b1000_0000 == 0:
                break

        return remaining_length, rl_data


    """
    Reads an MQTT message from a socket connection and returns a Packet instance. None on failure.
    """
    async def from_connection(connection: socket.socket, / , event_loop: asyncio.AbstractEventLoop = None) -> Optional['Packet']:
        if event_loop == None:
            event_loop = asyncio.get_event_loop()
        
        required_remaining = 1
        data = b""

        header = await event_loop.sock_recv(connection, 1)
        data += header

        if not header:
            # Connection closed by server
            return None

        remaining_length, rl_data = await Packet._read_remaining_length(connection, event_loop)
        data += rl_data

        data += await event_loop.sock_recv(connection, remaining_length)

        return Packet(data)