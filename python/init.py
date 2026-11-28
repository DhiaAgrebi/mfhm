lan_ip_address = None
ip_constant = "127.0.0.1"

from logging_utils.logging_script import logger

logger.info("server is about to start")

from socket import socket, AF_INET, SOCK_DGRAM
try:
    device_socket = socket(AF_INET, SOCK_DGRAM)
    device_socket.connect(("192.168.1.1", 80))

    lan_ip_address = device_socket.getsockname()[0]
    ip_constant = "0.0.0.0"

    device_socket.close()
except OSError:
    lan_ip_address = "N/A"

server_port = 8080

from asyncio import start_server, run
from backend_utils.db_utils import init_pool, close_pool
from parsing_and_routing_functions import parse_incoming_then_respond
from en import en_print_dict


from termcolor import colored

async def init_server():
    await init_pool()
    try:
        server = await start_server(parse_incoming_then_respond, ip_constant, server_port)

        print(colored(en_print_dict['server_is_operating'], "green") )
        print(colored(en_print_dict['lan_ip_of_server'], "blue"), f"{lan_ip_address}:{server_port}")

        async with server:
            await server.serve_forever()
    finally:
        await close_pool()


if __name__ == "__main__":
    run(init_server())
