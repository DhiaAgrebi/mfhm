from disk_to_ram_operations.prepare_html_files_for_service import (
    index_html,
    login_html,
    not_available,
    ping_response,
    register_html,
)
from disk_to_ram_operations.prepare_js_files_for_service import (
    datetime_js,
    ping_js,
    register_js,
    login_js,
)

from disk_to_ram_operations.prepare_css_files_for_service import (
    style_css,
)

from backend_utils.db_utils import session_token_is_valid
from http_requests_functions import break_down_incoming, process_post_request
from termcolor import colored


async def parse_incoming_then_respond(stream_reader, stream_writer):
    header_bytes = await stream_reader.readuntil(b"\r\n\r\n")
    headers_text = header_bytes.decode("utf-8")

    content_length = 0
    for line in headers_text.split("\r\n")[1:]:
        if line.lower().startswith("content-length:"):
            try:
                content_length = int(line.split(":", 1)[1].strip())
            except ValueError:
                content_length = 0
            break

    body_bytes = await stream_reader.readexactly(content_length) if content_length > 0 else b""

    incoming_as_str = headers_text + body_bytes.decode("utf-8")

    print(colored(f"{'#' * 10} Begin parse_incoming_then_respond {'#' * 10}", "blue"))
    incoming_broken_as_dict = break_down_incoming(incoming_as_str)
    print('!'*20)
    print('line 44 from parsing_and_routing_functions.')
    print('incoming_as_str sent to break_down_incoming.')
    print('!'*20)

    if incoming_broken_as_dict is None:
        print('!'*20)
        print('from line 50 in parsing_and_routing_functions')
        print('method type is None droppinh down function')
        print('!'*20)
        stream_writer.close()
        await stream_writer.wait_closed()
        return

    method_type = incoming_broken_as_dict["method_type"]
    session_token = incoming_broken_as_dict.get("session_token")
    user_is_authed = await session_token_is_valid(session_token)
    print("!"*20)
    print("from parsing and routing line 54.\nsession_token", session_token)
    print("from parsing and routing line 55.\nUser is authed", user_is_authed)
    print('!'*20)
    response = None
    if method_type == "get":
        type_of_static_file = incoming_broken_as_dict["type_of_static_file"]
        static_file = incoming_broken_as_dict["static_file"]
        response = return_file_if_found(type_of_static_file, static_file)
    elif method_type == "post":
        response = await process_post_request(incoming_broken_as_dict)
        print('!'*20)
        print('line 72 from parsing_and_routing functions')
        print('incoming_broken_as_dict is now received from process_post_request')
        print('is now response')
        print('!'*20)
    else:
        response = not_available

    if isinstance(response, str):
        response = response.encode("utf-8")

    print("!"*20)
    print("line 82 in parsing_and_routing_functions")
    print("response is:", response)
    print("!"*20)
    stream_writer.write(response)
    await stream_writer.drain()

    stream_writer.close()
    await stream_writer.wait_closed()
    print('!'*20)
    print('line 88 from parsing_and_routing_functions')
    print('response sent back to client, stream_writer closed')
    print('!'*20)


def return_file_if_found(type_of_static_file, static_file):
    file_types_dict = {
        "html": {
            "index.html": index_html,
            "login.html": login_html,
            "register.html": register_html,
        },
        "js": {
            "ping.js": ping_js,
            "datetime.js": datetime_js,
            "register.js": register_js,
            "login.js": login_js,
        },
        "css": {
            "style.css": style_css,
        },
    }

    if type_of_static_file is None:
        to_be_returned = not_available
    else:
        appropriate_dict_of_static_files = file_types_dict.get(type_of_static_file)
        if appropriate_dict_of_static_files is None:
            to_be_returned = not_available
        else:
            to_be_returned = appropriate_dict_of_static_files.get(
                static_file, not_available
            )

    return to_be_returned
