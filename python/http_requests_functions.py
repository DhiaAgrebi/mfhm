def break_down_incoming(incoming_as_str):
    list_of_lines = incoming_as_str.split("\r\n") 
    method_type = list_of_lines[0].split()[0].lower()
    
    uri = None
    if len(list_of_lines) > 1:
        uri = list_of_lines[0].split()[1]
    type_of_static_file = None
    static_file = None
    
    to_be_returned = dict()
    
    if method_type == "get":
        if uri == "/":
            type_of_static_file = "html"
            static_file = "index.html"
            
        elif "js" in uri:
            path_into_its_parts = uri[1:].split( '/' )
            type_of_static_file = path_into_its_parts[0]
            static_file = path_into_its_parts[1] 
        
        elif "html" in uri:
            path_into_its_parts = uri[1:].split( '/' )
            type_of_static_file = path_into_its_parts[0]
            static_file = path_into_its_parts[1]
            
        to_be_returned = {
           "method_type": method_type,
           "uri": uri,
           "type_of_static_file": type_of_static_file,
           "static_file": static_file,
            }    
            
    elif method_type == 'post':  
        payload = {
          "method_type": method_type,
          "uri": uri,
          "body": incoming_as_str.split("\r\n\r\n", 1)[1]
        }        
        to_be_returned = process_post_request(payload)
        
    return to_be_returned

import asyncio
import json

from backend_utils.db_utils import get_pool
from backend_utils.post_requests_utils import hash_password


async def process_post_request(incoming_broken_as_dict):
    uri = incoming_broken_as_dict["uri"]
    body = incoming_broken_as_a_dict["body"]

    match uri:
        case "/register":
            body_as_a_dict = json.loads(body)
            hashed_payload = await asyncio.to_thread(hash_password, body_as_a_dict)

            email = hashed_payload["user_email"]
            password_hash = hashed_payload["password"]

            async with get_pool().acquire() as conn:
                row = await conn.fetchrow(
                    """
                    INSERT INTO users (email, password_hash)
                    VALUES ($1, $2)
                    RETURNING uuid, email, created_at
                    """,
                    email,
                    password_hash,
                )
                body = dict(row)
                response = await asyncio.to_thread(append_header_to_body_then_return_post_response(body))
                response["metgod_type"] = "post"
                return response
