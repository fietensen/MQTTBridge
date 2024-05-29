from websockets.server import serve
from packet import Packet
import asyncio
import logging
import websockets
import queue
import socket

"""
Proxy class that handles all incoming connections
"""
class Proxy(object):
    def __init__(self, broker_host: str, broker_port: int, /, proxy_host: str = '127.0.0.1', proxy_port: int = 1883, broker_connect_timeout: int = 15) -> None:
        self.__broker_address = (broker_host, broker_port)
        self.__proxy_address = (proxy_host, proxy_port)
        self.__event_loop = None
        self.__broker_connect_timeout = broker_connect_timeout
        self.__done = True

    """
    Asynchronously starts the proxy server, handling incoming connections
    """
    def serve_forever(self, event_loop: asyncio.AbstractEventLoop) -> None:
        logging.debug("Starting proxy server")

        self.__done = False
        self.__event_loop = event_loop
        self.__event_loop.run_until_complete(self._serve_forever())
    

    async def _forward_server_messages_forever(self, websocket: websockets.WebSocketServerProtocol, connection: socket.socket) -> None:
        while not self.__done:
            pkt: Packet = await Packet.from_connection(connection, event_loop=self.__event_loop)
            if not pkt:
                # Server closed the connection
                break
            
            try:
                data = pkt.as_bytes()
                logging.debug("Server sent {} bytes to Client {}:{}".format(len(data), *websocket.remote_address))
                await websocket.send(data)

            except websockets.exceptions.ConnectionClosedError:
                logging.info("Client {}:{} disconnected".format(*websocket.remote_address))
                break
                
            except Exception as e:
                logging.error("Exception in server forwarder for {}:{}: {}".format(*websocket.remote_address, e))
                break


    async def _handle_client(self, websocket: websockets.WebSocketServerProtocol) -> None:
        assert self.__event_loop != None, "Event Loop not set in Proxy. Make sure to not directly call _handle_client."

        # establish connection to server
        broker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        broker_socket.settimeout(self.__broker_connect_timeout)
        
        try:
            broker_socket.connect(self.__broker_address)
        except TimeoutError:
            logging.warning("Could not connect to broker. Terminating client connection.")
            websocket.close(1011, "Could not connect to broker.")
            return
        
        # set socket blocking to false so that we can instead
        # use the socket asynchronously with asyncio
        broker_socket.setblocking(False)

        logging.info("New client connection from {}:{}".format(*websocket.remote_address))

        # forward server messages
        server_message_task = self.__event_loop.create_task(self._forward_server_messages_forever(websocket, broker_socket))

        try:
            while not server_message_task.done():
                message = await websocket.recv()
                logging.debug("Client {}:{} sent {} bytes".format(*websocket.remote_address, len(message)))
                await self.__event_loop.sock_sendall(broker_socket, message)


        except asyncio.CancelledError:
            pass    
        
        except websockets.exceptions.ConnectionClosedError:
            logging.info("Client {}:{} disconnected".format(*websocket.remote_address))
            
        finally:
            server_message_task.cancel()
            try:
                # wait for task to cancel
                await server_message_task
            except asyncio.CancelledError:
                pass

    def shutdown(self):
        self.__done = True 

    async def _serve_forever(self) -> None:
        assert self.__event_loop != None, "Event Loop not set in Proxy. Make sure to not directly call _serve_forever."
        try:
            async with serve(self._handle_client, *self.__proxy_address):
                logging.info("Started serving.")
                await asyncio.Future() # prevents function from returning
        
        except Exception as e:
            # TODO: clean this mess up
            if not self.__done:
                raise e
            else:
                pass