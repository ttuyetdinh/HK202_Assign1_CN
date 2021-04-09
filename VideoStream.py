import cv2
import os
import struct
class VideoStream:
	def __init__(self, filename):
		self.filename = filename
		self.wholeVideo = []
		try:
			self.file = open(filename, 'rb')
			print ('-'*60 +  "\nVideo file : |" + filename +  "| read\n" + '-'*60)
		except:
			print ("read " + filename + " error")
			raise IOError
		self.frameNum = 0

	def nextFrame(self):
		"""Get next frame."""

		data = self.file.read(5) # Get the framelength from the first 5 bytes
		#data_ints = struct.unpack('<' + 'B'*len(data),data)
		data = bytearray(data)

		data_int = (data[0] - 48) * 10000 + (data[1] - 48) * 1000 + (data[2] - 48) * 100 + (data[3] - 48) * 10 + (data[4] - 48)# = #int(data.encode('hex'),16)

		final_data_int = data_int

		if data:

			framelength = final_data_int#int(data)#final_data_int/8  # xx bytes
			# Read the current frame
			frame = self.file.read(framelength)
			if len(frame) != framelength:
				raise ValueError('incomplete frame data')
			#print "frame length"
			#print len(frame)
			#if not (data.startswith(b'\xff\xd8') and data.endswith(b'\xff\xd9')):
			#	raise ValueError('invalid jpeg')

			self.frameNum += 1
			print ('-'*10 + "\nNext Frame (#" + str(self.frameNum) + ") length:" + str(framelength) + "\n" + '-'*10)

			return frame

	def getWholeVideo(self):
		"""Append to the list"""
		if self.filename:
            # Get the framelength from the first 5 bits
			data = self.file.read(5)
			if data:
				framelength = int(data)
				self.wholeVideo.append(framelength)
				data = self.file.read(framelength)
			return data

	def calNumFrames(self):
		"""Get total nimber of frame"""
		while self.getWholeVideo():
			pass
		self.numFrame = len(self.wholeVideo)
		self.file.close()
		self.file = open(self.filename, 'rb')

	def calFps(self):
		"""Get frame per second"""
		cap = cv2.VideoCapture("./{0}".format(self.filename))
		self.fps = int(cap.get(cv2.CAP_PROP_FPS))

	def calTotalTime(self):
		"""Get total time of video"""
		self.calNumFrames()
		self.calFps()
		self.totalTime= self.numFrame/ self.fps



	def frameNbr(self):
		"""Get frame number."""
		return self.frameNum

	def reset_frame(self):
		"""restart the video"""
		self.file.seek(0)
		self.frameNum = 0

