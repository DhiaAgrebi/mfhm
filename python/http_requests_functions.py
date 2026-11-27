import asyncio
import datetime
import json
import uuid

from backend_utils.db_utils import get_pool
from backend_utils.post_requests_utils import (
    append_header_to_body_then_return_post_response,
    hash_password, verify_password
)

from termcolor import colored


def break_down_incoming(incoming_as_str):
    first_line, _, rest = incoming_as_str.partition("\r\n")
    headers_part, has_body, body_part = rest.partition("\r\n\r\n")
    body = body_part if has_body else None
    print(colored(f"{'#' *  5}", "yellow"), "http_request_first_line:", first_line)
    print("this is first line:", first_line)
    if not first_line:
        return

    session_token = None
    for line in headers_part.splitlines():
        if line.lower().startswith("cookie:"):
            for pair in line.split(":", 1)[1].split(";"):
                key, _, value = pair.strip().partition("=")
                if key.strip() == "session_token":
                    session_token = value.strip()
                    break


    
    first_line_into_list = first_line.split()
    method_type = first_line_into_list[0].lower()
    uri = first_line_into_list[1]

    type_of_static_file = None
    static_file = None

    to_be_returned = None

    if method_type == "get":
        if uri == "/":
            type_of_static_file = "html"
            static_file = "index.html"

        elif uri and ("js" in uri or "html" in uri or "css" in uri):
            path_into_its_parts = uri.strip("/").split("/", 1)
            type_of_static_file = path_into_its_parts[0]
            static_file = (
                path_into_its_parts[1] if len(path_into_its_parts) > 1 else None
            )

        to_be_returned = {
            "method_type": method_type,
            "uri": uri,
            "type_of_static_file": type_of_static_file,
            "static_file": static_file,
        }

    elif method_type == "post":
        parts = incoming_as_str.split("\r\n\r\n", 1)
        body = parts[1] if len(parts) > 1 else ""
        to_be_returned = {
            "method_type": method_type,
            "uri": uri,
            "body": body,
        }

    print(colored(f"{'#' * 5}, break_down_incoming's to_be_returned is:", "yellow"))
    print(to_be_returned)
    print(colored(f"{'#' * 10} End of break_down_incoming def, {'#' * 10}", "yellow"))
    
    return to_be_returned

import asyncpg
import secrets

async def process_post_request(incoming_broken_as_dict):
    uri = incoming_broken_as_dict.get("uri")
    body = incoming_broken_as_dict.get("body", "")

    match uri:
        case "/register":
            try:
                body_as_a_dict = json.loads(body)
            except json.JSONDecodeError:
                return await asyncio.to_thread(
                    append_header_to_body_then_return_post_response,
                    {"Type": "error", "message": "Invalid JSON body"},
                )

            hashed_payload = await asyncio.to_thread(hash_password, body_as_a_dict)

            email = hashed_payload["user_email"].strip().lower()
            password_hash = hashed_payload["password"]

            async with get_pool().acquire() as conn:
                try:
                    row = await conn.fetchrow(
                        """
                        INSERT INTO users (email, password_hash)
                        VALUES ($1, $2)
                        RETURNING uuid, email, created_at
                        """,
                        email,
                        password_hash,
                    )
                except asyncpg.exceptions.UniqueViolationError:
                    return await asyncio.to_thread(
                        append_header_to_body_then_return_post_response,
                        {"Type": "error", "message": "email already exists"},
                    )

                row_dict = dict(row)
                serialized_body = {
                    k: (
                        str(v)
                        if isinstance(v, uuid.UUID)
                        else v.isoformat() if isinstance(v, datetime.datetime) else v
                    )
                    for k, v in row_dict.items()
                }
                return await asyncio.to_thread(
                    append_header_to_body_then_return_post_response,
                    serialized_body,
                )

        case "/login":
            try:
                body_as_a_dict = json.loads(body)
            except json.JSONDecodeError:
                return await asyncio.to_thread(
                    append_header_to_body_then_return_post_response,
                    {"status": "error", "message": "Invalid JSON body"},
                )

            user_email = body_as_a_dict["user_email"]
            user_password = body_as_a_dict["user_password"]
            print("÷" * 20)
            print("÷" * 20)
            print("User email:", user_email)
            print("User password:", user_password)
            print("÷" * 20)
            print("÷" * 20)

            async with get_pool().acquire() as conn:
                user = await conn.fetchrow(
                    """
                    SELECT uuid, email, password_hash, created_at
                    FROM users
                    WHERE email = $1
                    """,
                    user_email,
                )

                if not user:
                    return await asyncio.to_thread(
                        append_header_to_body_then_return_post_response,
                        {"status": "error", "message": "User not found"},
                    )

                password_ok = await asyncio.to_thread(
                    verify_password,
                    user_password,
                    user["password_hash"],
                )

                if not password_ok:
                    return await asyncio.to_thread(
                        append_header_to_body_then_return_post_response,
                        {"status": "error", "message": "Password incorrect"},
                    )

                session_token = secrets.token_urlsafe(32)
                expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)

                await conn.execute(
                    """
                    INSERT INTO sessions (token, user_uuid, expires_at)
                    VALUES ($1, $2, $3)
                    """,
                    session_token,
                    user["uuid"],
                    expires_at,
                )

            serialized_user = {
                "status": "ok",
                "user": {
                    "uuid": str(user["uuid"]),
                    "email": user["email"],
                    "created_at": user["created_at"].isoformat()
                    if isinstance(user["created_at"], datetime.datetime)
                    else user["created_at"],
                },
                    "message":"You have been authed",
            }
            cookie_header = f"Set-Cookie: session_token={session_token}; HttpOnly; Path=/; SameSite=LAX"
            return await asyncio.to_thread(
                append_header_to_body_then_return_post_response,
                serialized_user, special_headers=[cookie_header]
            )

        case _:
            return await asyncio.to_thread(
                append_header_to_body_then_return_post_response,
                {"Type": "error", "message": f"Unknown POST endpoint: {uri}"},
            )
