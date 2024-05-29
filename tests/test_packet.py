import unittest
import socket
import asyncio
from src.packet import Packet

class TestPacket(unittest.TestCase):
    def test_from_connection(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        addr = server.getsockname()

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(addr)
        client.setblocking(False)

        ccon, _ = server.accept()
        
        # example connack packet
        ccon.send(b"\x20\x02\x00\x00")
        self.assertIsNotNone(asyncio.run(Packet.from_connection(client)))
        
        ccon.close()
        client.close()
        server.close()
    

    def test_as_bytes(self):
        data = b"\x20\x02\x00"
        packet = Packet(data)

        self.assertEqual(packet.as_bytes(), data)