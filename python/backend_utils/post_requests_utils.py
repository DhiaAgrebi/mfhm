import bcrypt

def hash_password(body_as_a_dict):
    """Hashes the 'password' field of a dict using bcrypt."""
    password = body_as_a_dict["password"]
    
    # bcrypt requires bytes
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    
    # Store the hash as a string (common practice)
    user_email_and_hashed_password_dict = dict()
    user_email_and_hashed_password_dict["user_email"] = body_as_a_dict["user_email"]
    user_email_and_hashed_password_dict["password"] = password_hash.decode("utf-8")
    
    return user_email_and_hashed_password_dict
    
import json

def append_header_to_body_then_return_post_response(body, special_headers = None):
    header = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: application/json; charset=utf-8\r\n"
        "Content-Length: {length}\r\n\r\n"
    )

    body_bytes = json.dumps(body).encode("utf-8")
    
    if special_headers:
        for special_header in special_headers:
            header = header + special_header

    updated_header = header.replace("{length}", str(len(body_bytes))).encode("utf-8")


    return updated_header + body_bytes


    
def verify_password(plain_password, stored_hash):
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        stored_hash.encode("utf-8"),
    )
