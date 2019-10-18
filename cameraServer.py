# Camera Server
# (c) Jessie Newman 2019

# Thanks to github.com/patrickfuller/camp for the base code
# that helped me figure out what to do (though this code is
# only barely similar to the original)

# Streams a connected USB camera to a local port.
# When the raspberry pi on the robot is configured as a
# wireless access point, another computer can access this
# stream to see the robot's point of view.

# The plan is eventually to have this page also provide
# clickable buttons as an alternate way to control the
# robot remotely.


# still need to see how mcuh of this code I can remove, adn change the
# website look

import base64

import os

import cStringIO as io

import tornado.web
import tornado.websocket
from tornado.ioloop import PeriodicCallback

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("webpage/index.html", port=8000)

class ErrorHandler(tornado.web.RequestHandler):
    def get(self):
        self.send_error(status_code=403)

class WebSocket(tornado.websocket.WebSocketHandler):

    def on_message(self, message):
        """Evaluates the function pointed to by json-rpc."""

        # Start an infinite loop when this is called
        if message == "read_camera":
            self.camera_loop = PeriodicCallback(self.loop, 10)
            self.camera_loop.start()

        # Extensibility for other methods
        else:
            print("Unsupported function: " + message)

    def loop(self):
        """Sends camera images in an infinite loop."""
        sio = io.StringIO()

        _, frame = camera.read()
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        img.save(sio, "JPEG")

        try:
            self.write_message(base64.b64encode(sio.getvalue()))
        except tornado.websocket.WebSocketClosedError:
            self.camera_loop.stop()
            

import cv2
from PIL import Image
camera = cv2.VideoCapture(0)

resolutions = {"high": (1280, 720), "medium": (640, 480), "low": (320, 240)}
w, h = resolutions["low"]
camera.set(3, w)
camera.set(4, h)

ROOT = os.path.normpath(os.path.dirname(__file__))

handlers = [(r"/", IndexHandler), #(r"/login", LoginHandler),
            (r"/websocket", WebSocket),
            (r"/static/password.txt", ErrorHandler),
            (r'/static/(.*)', tornado.web.StaticFileHandler , {'path': ROOT})]
application = tornado.web.Application(handlers, cookie_secret="PASSWORD")
application.listen(8000)


tornado.ioloop.IOLoop.instance().start()