#!/usr/bin/env python

import textwrap
import os
import re
import ModMention
import json

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

##Simple server deployed on Heroku.com to handle the post data from the Group me Call back
class GroupMeHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        
        json1=json.loads(post_data)
        
        
        #searches Json to see if /mods was in "text" field
        #ignores data if no match
        match=re.match('/mods',json1['text'])

        if match:
            ModMention.sendJson()
        else:
            print "ignore message"




        # self.send_response(200)



port=port = int(os.environ.get('PORT', 5000))
server_address = ('', port)
httpd = HTTPServer(server_address, GroupMeHandler)
httpd.serve_forever()