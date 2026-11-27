from pathlib import Path

disk_to_ram_operations_directory = \
  Path( __file__ ).parent
python_directory = disk_to_ram_operations_directory.parent
project_directory = python_directory.parent
html_css_js_directory = project_directory / "html_css_js"

css_directory = html_css_js_directory / "css"

style_css = css_directory / "style.css"
style_css = style_css.read_text(encoding='utf-8')
style_css = style_css.encode('utf-8')

appropriate_http_header_for_style_css = (
"HTTP/1.1 200 OK\r\n"
"Content-Type: text/css\r\n"
f"Content-Length: { len( style_css ) }\r\n"
"Connection: close\r\n"
"\r\n"
)
appropriate_http_header_for_style_css = appropriate_http_header_for_style_css.encode('utf-8')

style_css = appropriate_http_header_for_style_css + style_css