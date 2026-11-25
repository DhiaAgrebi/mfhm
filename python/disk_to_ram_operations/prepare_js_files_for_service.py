from pathlib import Path

disk_to_ram_operations_directory = \
  Path( __file__ ).parent
python_directory = disk_to_ram_operations_directory.parent
project_directory = python_directory.parent
html_css_js_directory = project_directory / "html_css_js"

js_directory = html_css_js_directory / "js"

ping_js = js_directory / "ping.js"
ping_js = ping_js.read_text(encoding='utf-8')
ping_js = ping_js.encode('utf-8')

appropriate_http_header_for_ping_js = (
"HTTP/1.1 200 OK\r\n"
"Content-Type: application/javascript\r\n"
f"Content-Length: { len( ping_js ) }\r\n"
"Connection: close\r\n"
"\r\n"
)
appropriate_http_header_for_ping_js = appropriate_http_header_for_ping_js.encode('utf-8')

ping_js = appropriate_http_header_for_ping_js + ping_js

datetime_js = js_directory / "datetime.js"
datetime_js = datetime_js.read_text(encoding='utf-8')
datetime_js = datetime_js.encode('utf-8')

appropriate_http_header_for_datetime_js = (
"HTTP/1.1 200 OK\r\n"
"Content-Type: application/javascript\r\n"
f"Content-Length: { len( datetime_js ) }\r\n"
"Connection: close\r\n"
"\r\n"
)

appropriate_http_header_for_datetime_js = appropriate_http_header_for_datetime_js.encode('utf-8')
datetime_js = appropriate_http_header_for_datetime_js + datetime_js

register_js = js_directory / "register.js"
register_js = register_js.read_text(encoding='utf-8')
register_js = register_js.encode('utf-8')

appropriate_http_header_for_register_js = (
"HTTP/1.1 200 OK\r\n"
"Content-Type: application/javascript\r\n"
f"Content-Length: { len( register_js ) }\r\n"
"Connection: close\r\n"
"\r\n"
)

appropriate_http_header_for_register_js = appropriate_http_header_for_register_js.encode('utf-8')
register_js = appropriate_http_header_for_register_js + register_js

login_js = js_directory / "login.js"
login_js = login_js.read_text(encoding='utf-8')
login_js = login_js.encode('utf-8')

appropriate_http_header_for_login_js = (
"HTTP/1.1 200 OK\r\n"
"Content-Type: application/javascript\r\n"
f"Content-Length: { len( login_js ) }\r\n"
"Connection: close\r\n"
"\r\n"
)

appropriate_http_header_for_login_js = appropriate_http_header_for_login_js.encode('utf-8')
login_js = appropriate_http_header_for_login_js + login_js
