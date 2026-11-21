from disk_to_ram_operations.prepare_html_files_for_service import (
  index_html, login_html, register_html,
  ping_response, not_available )
  
from disk_to_ram_operations.prepare_js_files_for_service import (
  ping_js, datetime_js, register_js)

def return_file_if_found(type_of_static_file, static_file):
    
    file_types_dict = {
    'html': {
           'index.html': index_html,
           'login.html': login_html,
           'register.html': register_html,
        },
    'js': {
        'ping.js': ping_js,
        'datetime.js': datetime_js,
        'register.js': register_js,            
    }
        }
        
    if type_of_static_file is None:
      to_be_returned = not_available      
    else:    
      appropriate_dict_of_static_files = file_types_dict[type_of_static_file]
      to_be_returned = appropriate_dict_of_static_files[static_file]
         
    return to_be_returned

from http_requests_functions import break_down_incoming, process_post_request

async def parse_incoming_then_respond(stream_reader, stream_writer):
    
    incoming = await stream_reader.read(1024) # type bytes
    incoming_as_str = incoming.decode('utf-8')
    print("incoming as str:", incoming_as_str)
    
    incoming_broken_as_dict = break_down_incoming(incoming_as_str)
    print(incoming_broken_as_dict)
    

    method_type = incoming_broken_as_dict["method_type"]
    
    
    response = None
    if method_type == 'get':
       type_of_static_file = incoming_broken_as_dict["type_of_static_file"]
       static_file = incoming_broken_as_dict["static_file"]
       response = return_file_if_found(type_of_static_file, static_file)
    elif method_type == 'post':
       response = process_post_request(incoming_broken_as_dict)
        

    stream_writer.write(response)
    await stream_writer.drain()
    
    stream_writer.close()
    await stream_writer.wait_closed() 

    
    
