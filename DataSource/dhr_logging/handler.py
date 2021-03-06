#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import json
from logging.handlers import HTTPHandler

__author__ = 'Xiaoxiao.Xiong'

class JsonHTTPHandler(HTTPHandler):

    """
    A class which sends records to a Web server, using POST semantics.
    """
    def emit(self, record):
        """
        Emit a record.

        Send the record to the Web server as a json string
        """
        # instantiate the model
        try:
            import socket
            socket.setdefaulttimeout(4)

            import httplib, urllib
            host = self.host
            h = httplib.HTTP(host)
            url = self.url
            data = self.format(record)
            if self.method == "POST":
                h.putrequest(self.method, url)
                # support multiple hosts on one IP address...
                # need to strip optional :port from host, if present
                i = host.find(":")
                if i >= 0:
                    host = host[:i]
                h.putheader("Host", host)
                h.putheader("Content-type",
                            "application/json")
                h.putheader("dataType", "json")
                h.putheader("Content-length", str(len(data)))
                h.endheaders(data if self.method == "POST" else None)
                h.getreply()    #can't do anything with the result

        except Exception as e:
            status_code = 500
            response = json.dumps({
                "status_code": status_code,
                "message": ("{0}: {1}").format(
                    type(e).__name__,
                    repr(e)) + ': Error happened when send logs to logging server!'
            })
            # response.status_code = status_code
            return response
