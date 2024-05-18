import threading
import cv2
import PIL.Image, PIL.ImageTk
import socket
import time
import os
from queue import Queue

class VideoCapture:
    def __init__(self, video_source, text):
        self.video_source = video_source
        self.vid = None
        self.text = text
        self.ipv4 = text
        self.ret = False
        self.frame = None
        self.running = True

        self.recording = False
        self.recording_filename = 'output.mp4'
        self.recording_writer = None
        self.max_queue_size = 50
        self.frame_queue = Queue(maxsize=self.max_queue_size)  # Queue để lưu trữ các frame
        
        self.open_camera()
        disconnect_camera = PIL.Image.open(".camera_app/image/disconnect.png")
        self.default_image= PIL.ImageTk.PhotoImage(disconnect_camera)
        
        self.load_frame_from_camera_thread = threading.Thread(target=self.process)
        self.load_frame_from_camera_thread.daemon = True
        self.load_frame_from_camera_thread.start()

    def open_camera(self):
        self.vid = cv2.VideoCapture(self.video_source)
        self.vid.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.vid.get(cv2.CAP_PROP_FPS))
        self.fps_record = 25
    
    def check_connect_camera (self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # socket.AF_INET là tham số truyền vào IP phiên bản 4 IPv4
        # socket.SOCK_STREAM là tham số chỉ loại kết nối TCP IP
        sock.settimeout(0.01)
        exitcode = sock.connect_ex((self.ipv4, 554))
        sock.close()
        return True if not exitcode else False      

    def start_recording(self, filename=None):
        if self.recording:
            print('Đang quay video với tên:', self.recording_filename)
        else:
            folder = "video/" + time.strftime("%Y-%m-%d", time.localtime()) 
            if filename:
                self.recording_filename = filename
            else:
                os.makedirs(folder, exist_ok=True)
                self.recording_filename = folder + "/" + self.text + time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + ".avi"
            fourcc = cv2.VideoWriter_fourcc(*'MP42')
            self.recording_writer = cv2.VideoWriter(self.recording_filename, fourcc, self.fps_record, (self.width, self.height))
            self.recording = True
            self.write_video_thread = threading.Thread(target=self.write_frames)
            self.write_video_thread.start()
            print('[MyVideoCapture]  Bắt đầu ghi hình:', self.recording_filename)

    def stop_recording(self):
        if not self.recording:
            print('[MyVideoCapture] not recording')
        else:
            self.recording = False
            self.recording_writer.release()
            print('[MyVideoCapture] stop recording:', self.recording_filename)

    def put_frame_to_queue(self, frame):
        # Ghi frame vào queue
        self.frame_queue.put(frame)
        if self.frame_queue.qsize() > self.max_queue_size:
            self.frame_queue.get()
    
    def write_frames(self):
        while self.recording:
            # Nếu có frame trong queue thì ghi chúng xuống video
            if not self.frame_queue.empty():
                frame = self.frame_queue.get()
                if self.recording_writer and self.recording_writer.isOpened():
                    self.recording_writer.write(frame)
            else:
                time.sleep(0.01)  # Nếu không có frame nào, tạm dừng 10ms
                
    def snapshot(self, filename=None):
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
            # if not self.check_connect_camera():
            #     self.ret = None
            #     # self.frame = self.default_image
            #     # self.release_function() 
         
            self.ret, self.frame = self.vid.read()
            
            if not self.ret:
                self.running = False
                if self.recording:
                    self.stop_recording()
                break
            else:
                if self.recording:
                    self.put_frame_to_queue(self.frame)
                    
    def get_frame(self):
        return self.ret, self.frame
    
    def release_function(self):
        if self.running:
            self.running = False
            self.load_frame_from_camera_thread.join()
            if self.recording:
                self.stop_recording()
            if self.vid.isOpened():
                self.vid.release()
