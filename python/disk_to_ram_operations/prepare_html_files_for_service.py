not_available = (
    "HTTP/1.1 404 Not Found\r\n"
    "Content-Type: text/plain; charset=utf-8\r\n"
    "Content-Length: 0\r\n"
    "Connection: close\r\n"
    "\r\n")
    
not_available = not_available.encode('utf-8')

from pathlib import Path

disk_to_ram_operations_directory = \
  Path( __file__ ).parent
python_directory = disk_to_ram_operations_directory.parent
project_directory = python_directory.parent
html_css_js_directory = project_directory / "html_css_js"

html_directory = html_css_js_directory / "html"

header_html = html_directory / "header.html"
header_html = header_html.read_text( encoding='utf-8' )
appropriate_header_html_for_index_html = header_html.replace('@', "صَفحَةُ إِنشَاءُ حِسَابٍ أَو تَسجِيلُ الدُّخُولِ.")

index_html = html_directory / "index.html"
index_html = index_html.read_text( encoding='utf-8' )
index_html = appropriate_header_html_for_index_html + index_html
index_html = index_html.encode( 'utf-8' )

appropriate_http_header_for_index_html = (
  "HTTP/1.1 200 OK\r\n"
  "Content-Type: text/html; charset=utf-8\r\n"
  f"Content-Length: { len( index_html ) }\r\n"
  "Connection: close\r\n"
  "\r\n"
)
appropriate_http_header_for_index_html = appropriate_http_header_for_index_html.encode( 'utf-8' )

index_html = appropriate_http_header_for_index_html + index_html

login_html = html_directory / "login.html"
login_html = login_html.read_text( encoding='utf-8' )
appropriate_header_html_for_login_html = header_html.replace('@', "صَفحَةُ تَسجِيلِ الدُّخُولِ لِحِسَابٍ مُنشَئٍ.")
login_html = appropriate_header_html_for_login_html + login_html
login_html = login_html.encode( 'utf-8' )

appropriate_http_header_for_login_html = (
  "HTTP/1.1 200 OK\r\n"
  "Content-Type: text/html; charset=utf-8\r\n"
  f"Content-Length: { len( login_html ) }\r\n"
  "Connection: close\r\n"
  "\r\n"
  )
appropriate_http_header_for_login_html = appropriate_http_header_for_login_html.encode( 'utf-8' )

login_html = appropriate_http_header_for_login_html + login_html

register_html = html_directory / "register.html"
register_html = register_html.read_text( encoding='utf-8' )
appropriate_header_html_for_register_html = header_html.replace('@', 'صَفحَةُ إِنشَاءِ حِسَابٍ جَدِيدٍ.')
register_html = appropriate_header_html_for_register_html + register_html

register_html = register_html.encode( 'utf-8' )

appropriate_http_header_for_register_html = (
  "HTTP/1.1 200 OK\r\n"
  "Content-Type: text/html; charset=utf-8\r\n"
  f"Content-Length: { len( register_html ) }\r\n"
  "Connection: close\r\n"
  "\r\n"
  )
appropriate_http_header_for_register_html = appropriate_http_header_for_register_html.encode( 'utf-8' )
register_html = appropriate_http_header_for_register_html + register_html

ping_response = "HTTP/1.1 200 OK\r\nConnection: close\r\n"
ping_response = ping_response.encode( 'utf-8' )
