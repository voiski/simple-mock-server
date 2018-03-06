#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import yaml, re, os

def get_dictionary(path):
    yaml_dict = yaml.load(open(path))
    return yaml_dict[os.getenv('MOCK_PROFILE',yaml_dict.keys()[0])]

dictionary = get_dictionary(os.path.dirname(os.path.abspath(__file__))+'/../share/samples.yml')
if os.getenv('SAMPLE_PATH'):
    dicts = [ dictionary, get_dictionary(os.getenv('SAMPLE_PATH')) ]
    dictionary = {k: v for d in dicts for k, v in d.items()}
paths = list(dictionary.keys())

def retrieve_valid_path(path):
    matches = [x for x in paths if re.match('^'+x+'$',path)]
    if matches:
        return matches[0]

class S(BaseHTTPRequestHandler):
    def _set_headers(self,content_type='text/html',code=200):
        self.send_response(code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self):
        matched_key=retrieve_valid_path(self.path)
        content_type = 'text/html'
        if matched_key:
            content = dictionary[matched_key]
            if isinstance(content,dict):
                content_type = content['content-type']
                content = content['content']
            self._set_headers(content_type)
            self.wfile.write(dictionary[matched_key])
        else:
            self._set_headers(code=404)
            self.wfile.write("Not valid: " + self.path)

        
def run(server_class=HTTPServer, handler_class=S, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()