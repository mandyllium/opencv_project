import os
import subprocess

import wx

import numpy

LOG_LEVEL       = "error"
VIDEO_CODEC     = "rawvideo"
PIXEL_FORMAT    = "rgb24"
VIDEO_SYNC_MODE = "drop"

class Video():
    def __init__(self, file_name, out_frame_width, out_frame_height):
        self._file_name       = file_name
        self._duration        = 0.0
        self._frame_rate      = 0.0
        self._last_frame      = 0
        self._frame_width     = 0
        self._frame_height    = 0
        self.out_frame_width  = out_frame_width
        self.out_frame_height = out_frame_height

        self._get_video_info()

        self._process = subprocess.Popen(["ffmpeg",
                                          "-loglevel", LOG_LEVEL,
                                          "-i", f"{file_name}",
                                          "-f", "image2pipe",
                                          "-s", f"{self.out_frame_width}x{self.out_frame_height}",
                                          "-vsync", VIDEO_SYNC_MODE,
                                          "-pix_fmt", PIXEL_FORMAT,
                                          "-vcodec", VIDEO_CODEC,
                                          "-"],
                                         stdin = subprocess.PIPE,
                                         stdout = subprocess.PIPE,
                                         stderr = subprocess.PIPE,
                                         bufsize = 3 * self._frame_width *self._frame_height
                                         )
        #print(self._process.stderr.readline(), self._process.stderr.readline())

    def iter_frames(self):
        raw_image = self._process.stdout.read(self.out_frame_width * self.out_frame_height * 3)
        if not raw_image:
            return None, None
        cur_frame = numpy.frombuffer(raw_image, dtype='uint8')
        cur_bmp = wx.Bitmap.FromBuffer(self.out_frame_width, self.out_frame_height, cur_frame)
        return cur_frame, cur_bmp

    def goto_frame(self, target_frame_num, next_frame = False):
        print(f"{(1 / self._frame_rate) * target_frame_num}", target_frame_num)
        if next_frame:
            return self.iter_frames()
        else:
            return self._get_arbitrary_frame(target_frame_num)

    def get_org_frame_width(self):
        return self._frame_width

    def get_org_frame_height(self):
        return self._frame_height

    def get_frame_rate(self):
        return self._frame_rate

    def get_last_frame(self):
        return self._last_frame


    def _get_arbitrary_frame(self, target_frame_num):
        #Here we are using total number seconds with miliseconds as the arg for -ss
        self._process = subprocess.Popen(['ffmpeg',
                                          "-loglevel", LOG_LEVEL,
                                          "-ss", f"{(1 / self._frame_rate) * target_frame_num}",
                                          "-i", f"{self._file_name}",
                                          "-f", "image2pipe",
                                          "-s", f"{self.out_frame_width}x{self.out_frame_height}",
                                          "-vsync", VIDEO_SYNC_MODE,
                                          "-pix_fmt", PIXEL_FORMAT,
                                          "-vcodec", VIDEO_CODEC,
                                          "-"],
                                         stdin = subprocess.PIPE,
                                         stdout = subprocess.PIPE,
                                         stderr = subprocess.PIPE
                                         )
        return self.iter_frames()

    def _get_video_info(self):
        try:
            #Here output values order are not dependent on the stream args order
            out = subprocess.check_output(["ffprobe",
                                           "-loglevel", LOG_LEVEL,
                                           "-select_streams", "v:0",
                                           "-show_entries", "stream=avg_frame_rate,width,height,duration",
                                           "-of", "default=nw=1:nk=1",
                                           f"{self._file_name}"]).decode().split("\r\n")[:-1]
            self._frame_width = int(out[0])
            self._frame_height = int(out[1])
            self._frame_rate = next(map((lambda x: int(x[0]) / int(x[1])), [out[2].split("/")]))
            self._duration = float(out[3]) if not out[3] == "N/A" else 0
            self._last_frame = round((self._duration - (1 / self._frame_rate)) * self._frame_rate)
        except subprocess.CalledProcessError:
            print("Error while getting width, height etc. from process")

    def __del__(self): pass
        #self._process.terminate()
        # self._process.stdout.close()
        # self._process.stderr.close()
        # self._process.wait()
        # self._process = None

