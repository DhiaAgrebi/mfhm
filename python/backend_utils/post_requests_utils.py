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

def append_header_to_body_then_return_post_response(body, special_headers=None):
    body_bytes = json.dumps(body).encode("utf-8")

    # Build the header block WITHOUT the blank line first
    header_lines = [
        "HTTP/1.1 200 OK",
        "Content-Type: application/json; charset=utf-8",
        f"Content-Length: {len(body_bytes)}",
    ]

    # Add each special header as its own line, WITHOUT its own \r\n
    if special_headers:
        for h in special_headers:
            # Strip any stray trailing CRLF so we control it here
            header_lines.append(h.rstrip("\r\n"))

    # Join with CRLF, then the blank line that terminates the header block
    header_block = "\r\n".join(header_lines) + "\r\n\r\n"

    return header_block.encode("utf-8") + body_bytes
    
def verify_password(plain_password, stored_hash):
   print("÷"*20)
   print("from backed_utils.post_resquests_utils, line 40") 
   verdict = bcrypt.checkpw(
        plain_password.encode("utf-8"),
        stored_hash.encode("utf-8"))
   print('plain==hash:', verdict)
   print('÷'*20)
    
   return verdict
