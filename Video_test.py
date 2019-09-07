import cv2
import numpy as np
import wx
import imutils
from skimage.transform import resize


class Video:
    def __init__(self):
        # self._filename = file_name
        self._frame_number = -1
        self._cap = cv2.VideoCapture('C:\\Users\\qpjg1605\\Documents\\Python_proj\\Auptimo\\WIN_20190811_12_34_58_Pro.mp4')  ###self._filename
        self._frameCount = int(self._cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self._frameWidth = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self._frameHeight = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(self._frameCount)
        self._buf = np.empty((self._frameCount, self._frameHeight, self._frameWidth, 3),
                             np.dtype('uint8'))  # Empy numpy array of the shape and dtype(pixel from 0 to 255)
        self._frame_count = 0
        self._frame_grabbed = True
        print("here")
        while self._frame_count < self._frameCount and self._frame_grabbed:
            self._frame_grabbed, self._buf[self._frame_count] = self._cap.read()
            #self._buf[self._frame_count] = resize(img, (360, 640), anti_aliasing=False)
            #self._buf[self._frame_count] = img
            self._buf[self._frame_count] = self._buf[self._frame_count][..., ::-1]## Converting BGR to RBG(last dimension)
            #self._buf[self._frame_count] = imutils.resize(self._buf[self._frame_count], 640, 360)
            self._frame_count += 1
            #print(self._frame_count)

    def iter_frames(self):
        while self._frame_number < self._frameCount:
            self._frame_number = self._frame_number + 1
            # yield int(self._frame_number)
            # cur_bmp = wx.Bitmap.FromBuffer(self.get_org_frame_width(), self.get_org_frame_height(), )
            print(self._frame_number)
            yield self._buf[self._frame_number], wx.Bitmap.FromBuffer(self.get_org_frame_width(),
                                                                      self.get_org_frame_height(),
                                                                      self._buf[self._frame_number])  # Return NDArray and Bitmap Image

    def get_org_frame_width(self):
        return self._cap.get(cv2.CAP_PROP_FRAME_WIDTH)

    def get_org_frame_height(self):
        return self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame_rate(self):
        return self._cap.get(cv2.CAP_PROP_FPS)

    def goto_frame(self,target_frame_number):
        if target_frame_number <= self._frameCount:
            return self._buf[target_frame_number], wx.Bitmap.FromBuffer(self.get_org_frame_width(),
                                                                      self.get_org_frame_height(),
                                                                      self._buf[target_frame_number])
        else:
            return self._buf[0], wx.Bitmap.FromBuffer(self.get_org_frame_width(),
                                                                      self.get_org_frame_height(),
                                                                      self._buf[0])

    def __del__(self):  # Destructor
        self._cap.release()

#v = Video()
#print(next(v.iter_frames()))
