import os
from datetime import datetime
import threading
import time

from Webportal_Module.application import socketio, emit
import cv2


class VideoEmitter(threading.Thread):

	def __init__(self, video_stream, socketio):

		# Call the supers init function
		threading.Thread.__init__(self)
		self.video_stream = video_stream
		self.socketio = socketio

	def run(self):
		print("Starting: " + self.name)
		running = True
		while running:
			frame = self.video_stream.get_current_frame()
			# print(frame)
			# _, enc = cv2.imencode('.jpg', frame)
			# im_bytes = frame.tobytes()
			# im_b64 = base64.b64encode(im_bytes)
			self.socketio.emit('frame', frame)
			self.socketio.emit('test')
			time.sleep(1)
			print("emit")



	def set_running(self, option: bool):
		self.running = option

	def break_down(self):
		print("Breaking down thread: " + self.name)
