import threading
import cv2
import time
import os

# Đọc từng frame từ camera
class VideoCapture:
    def __init__(self, video_source, text):

        # Khởi tạo các giá trị mặc định
        self.video_source = video_source
        self.vid = None
        self.text = text
        
        self.ret = False
        self.frame = None
        self.running = True
        self.camera_connected = True
        
        # default values for recording
        
        self.recording = False
        self.recording_filename = 'output.mp4'
        self.recording_writer = None
        
        self.open_camera()
        
        # Khởi tạo thread, tham số daemon có nghĩa là khi chương trình tắt thì thread cũng tự động đóng
        self.thread = threading.Thread(target=self.process)
        self.thread.daemon = True
        self.thread.start()

    def open_camera(self):
        self.vid = cv2.VideoCapture(self.video_source)
        self.vid.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        
        self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))    # convert float to int
        self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))  # convert float to int
        self.fps = int(self.vid.get(cv2.CAP_PROP_FPS))
        self.fps_record = 25
        # print(self.fps)
    
        if not self.vid.isOpened():
            # print(cannot_connect_camera)
            self.camera_connected = False
            return
    
    def start_recording(self, filename=None):

        if self.recording:
            print('Đang quay video với tên:', self.recording_filename)
        else:
            folder = "video/" + time.strftime("%Y-%m-%d", time.localtime()) 
            if filename:
                self.recording_filename = filename
            else:
                os.makedirs(folder, exist_ok=True)
                self.recording_filename = folder + "/"+ self.text + time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + ".avi"
            fourcc = cv2.VideoWriter_fourcc(*'MP42') # .avi
        
            self.recording_writer = cv2.VideoWriter(self.recording_filename, fourcc, self.fps_record, (self.width, self.height))
            self.recording = True
            print('[MyVideoCapture]  Bắt đầu ghi hình:', self.recording_filename)

    def stop_recording(self):

        if not self.recording:
            print('[MyVideoCapture] not recording')
        else:
            self.recording = False
            self.recording_writer.release()
            print('[MyVideoCapture] stop recording:', self.recording_filename)

    def record(self, frame):

        # write frame to file
        if self.recording_writer and self.recording_writer.isOpened():
            self.recording_writer.write(frame)
    
    def snapshot(self, filename=None):
        """TODO: add docstring"""

        if not self.ret:
            print('[MyVideoCapture] no frame for snapshot')
        else:
            folder = "image/" + self.text+ time.strftime("%Y-%m-%d", time.localtime())
            os.makedirs(folder, exist_ok=True)
            if not filename:
                filename =folder + "/" + time.strftime("frame-%d-%m-%Y-%H-%M-%S.jpg")
                cv2.imwrite(filename, self.frame)
                print('[MyVideoCapture] snapshot (using cv2):', filename)

        
    # Thực hiện luồng stream
    def process(self):
        while self.running:
            if not self.camera_connected:
                self.release_function()
                return
         
            self.ret, self.frame = self.vid.read()
            
            if self.ret:
                if self.recording:
                    self.record(self.frame)
            else:
                self.running = False
                if self.recording:
                    self.stop_recording()
                break
                
    # Trả về frame hiện tại
    def get_frame(self):
        return self.ret, self.frame

    # Giải phóng tài nguyên khi kết thúc ghi hình, hàm hủy sẽ được gọi trước khi đóng cửa sổ
    def release_function(self):
        if self.running:
            self.running = False
            self.thread.join()
        if self.vid.isOpened():
            self.vid.release()
            