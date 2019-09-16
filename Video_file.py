import cv2
import wx


class Video:
    def __init__(self, file_name):
        self._filename = file_name
        self._frame_number = -1
        self._cap = cv2.VideoCapture(self._filename)

        self._frameCount = int(self._cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self._frameWidth = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self._frameHeight = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self._frame_count = 0
        self._frame_grabbed = True

    def iter_frames(self):   # Frame Generator to yield next frame
        while self._frame_count < self._frameCount and self._frame_grabbed:
            self._frame_count += 1
            self._frame_grabbed, self.img = self._cap.read()
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            #print(self._cap.get(cv2.CAP_PROP_POS_FRAMES)) # Just for debugging
            yield self.img, wx.Bitmap.FromBuffer(640, 360, cv2.resize(self.img, (640, 360)))


    def get_org_frame_width(self):
        return self._cap.get(cv2.CAP_PROP_FRAME_WIDTH)


    def get_org_frame_height(self):
        return self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT)


    def get_frame_rate(self):
        return self._cap.get(cv2.CAP_PROP_FPS)

    def goto_frame(self, goto_frame):   # Both Prev and Goto_frame funtions will call this function (if On_Prev_Btn then goto_frame = -1 and if On_Text_Enter the goto_frame = frame number passed )
        self._goto_frame = self._cap.get(cv2.CAP_PROP_POS_FRAMES) - 2
        self._cap.set(cv2.CAP_PROP_POS_FRAMES, self._goto_frame)
        self._frame_grabbed, self.img = self._cap.read()
        print(self._cap.get(cv2.CAP_PROP_POS_FRAMES))
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        return self.img, wx.Bitmap.FromBuffer(640, 360, cv2.resize(self.img, (640, 360)))


    def got_frame(self, goto_frame):
        print("here")
        self._current_frame = self._cap.get(cv2.CAP_PROP_POS_FRAMES)
        print("current: ", self._current_frame)
        if goto_frame == -1:   ##### For Prev Button
            self._current_frame -= 1
            self._frame_count = 0
            self._cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            while self._frame_grabbed:
                self._frame_grabbed, self.img = self._cap.read()
                self._frame_count += 1
                if self._frame_count == self._current_frame:
                    self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
                    print("p: ", self._current_frame,self._frame_count)
                    return self.img, wx.Bitmap.FromBuffer(640, 360, cv2.resize(self.img, (640, 360)))

        elif goto_frame == self._cap.get(cv2.CAP_PROP_POS_FRAMES):
            self._current_frame = self._cap.get(cv2.CAP_PROP_POS_FRAMES)
            pass

        elif goto_frame > self._frameCount:
            self._cap.set(cv2.CAP_PROP_POS_FRAMES, (self._frameCount - 1))
            self._frame_grabbed, self.img = self._cap.read()
            print(self._cap.get(cv2.CAP_PROP_POS_FRAMES))
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            print("last")
            return self.img, wx.Bitmap.FromBuffer(640, 360, cv2.resize(self.img, (640, 360)))

        elif goto_frame > self._current_frame:
            while self._frame_grabbed:
                self._frame_grabbed, self.img = self._cap.read()
                self._frame_count += 1
                if self._frame_count == goto_frame:
                    self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
                    print("g: ", self._frame_count)
                    return self.img, wx.Bitmap.FromBuffer(640, 360, cv2.resize(self.img, (640, 360)))

        elif goto_frame < self._current_frame:
            self._frame_count = 0
            self._cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            while self._frame_grabbed:
                self._frame_count += 1
                self._frame_grabbed, self.img = self._cap.read()
                if self._frame_count == goto_frame:
                    self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
                    print("s: ", self._frame_count)
                    return self.img, wx.Bitmap.FromBuffer(640, 360, cv2.resize(self.img, (640, 360)))

    def __del__(self):
        self._cap.release()

# #print(hpy().heap())
# # if __name__ == '__main__':
# v =Video(r"C:\Users\qpjg1605\Documents\Python_proj\Auptimo\C2477.MP4")
# #  #print(v._frameCount)
# # #print(v.get_org_frame_height(),v.get_org_frame_width())
# v.iter_frames()
# #print(next)