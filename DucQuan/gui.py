import PIL.ImageTk, PIL.Image
import cv2
import tkinter
from stream_camera import VideoCapture

class Camera_GUI (tkinter.Frame):
    def __init__(self, parent, text="", source=0, camera = None):

        super().__init__(parent)

        self.source = source
        self.camera = camera
        # Khởi tạo các giá trị ban đầu
        default_image_ = PIL.Image.open(".camera_app/image/default_image.png")
        self.default_image= PIL.ImageTk.PhotoImage(default_image_)

        self.vid = VideoCapture(self.source, text= text)
        
        self.make_gui_camera(text= text, window= self, width=500, height= 400)
        self.id_image = self.canvas.create_image(0, 0, image=self.default_image, anchor='nw')

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 25
        self.running = True
        self.update_frame()
        
    def make_gui_camera(self, text, window, width, height):
        
        # frame chứa camera 
        self.frame_toan_canh=tkinter.Frame(window, width=200, height=400, bg="#3cb371", border=5)
        self.frame_toan_canh.pack(fill=tkinter.BOTH, expand=True)   
        
        # Label hiển thị tên camera, ví dụ "Cam toàn cảnh"
        self.label = tkinter.Label(self.frame_toan_canh, text=text)  
        self.label.pack(side= tkinter.TOP,fill=tkinter.BOTH)

        # Canvas chứa hình ảnh lấy từ camera
        self.canvas = tkinter.Canvas(self.frame_toan_canh, width=width, height=height)
        self.canvas.pack(fill=tkinter.BOTH, expand=True)
        
        # Button that lets the user take a snapshot
        self.btn_recording = tkinter.Button(self.frame_toan_canh, text="Ghi hình", activebackground="tomato", cursor= "hand2", border = 5, command=self.start)
        self.btn_recording.pack(anchor='center', side='left', expand=True)

        self.btn_stop_recording = tkinter.Button(self.frame_toan_canh, text="Dừng ghi hình", cursor= "hand2", border = 5, command=self.stop)
        self.btn_stop_recording.pack(anchor='center', side='left', expand=True)
        self.btn_stop_recording["state"] = "disable"

        # Button that lets the user take a snapshot
        self.btn_snapshot = tkinter.Button(self.frame_toan_canh, text="Chụp ảnh", cursor= "hand2", border = 5, command=self.snapshot)
        self.btn_snapshot.pack(anchor='center', side='left', expand=True)

        # Button that lets the user take a snapshot
        self.btn_view = tkinter.Button(self.frame_toan_canh, text="Mở rộng", cursor= "hand2", border = 5, command=self.view)
        self.btn_view.pack(anchor='center', side='left', expand=True)
        
        # Button that lets the user take a snapshot
        self.btn_view = tkinter.Button(self.frame_toan_canh, text="Thông tin", cursor= "hand2", border = 5, command=self.setting_camera)
        self.btn_view.pack(anchor='center', side='left', expand=True)
    
    def update_frame(self):
        # Lấy từng khung hình từ camera
        ret, frame = self.vid.get_frame()
        
        # Lấy chiều cao, chiều rộng của canvas chứa camera
        self.canvas.update()
        width = self.canvas.winfo_width()
        height= self.canvas.winfo_height()
        
        if ret:
            # Xóa hình ảnh cũ
            self.canvas.delete(self.id_image)
            # Thay đổi kích thước khung hình cho vừa với kích thước canvas
            resized_image = cv2.resize(frame,(width, height))
            self.frame = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
            self.frame = PIL.Image.fromarray(self.frame)
            self.photo = PIL.ImageTk.PhotoImage(image=self.frame)
            # Ve khung hình mới lên canvas
            self.id_image = self.canvas.create_image(0, 0, image=self.photo, anchor='nw')
        else:
            self.canvas.delete(self.id_image)
            self.id_image = self.canvas.create_image(0, 0, image=self.default_image, anchor='nw')  
        # Sau khoảng thời gian delay thì tiếp tục lặp lại cập nhật khung hình
        if self.running:
            self.after(self.delay, self.update_frame)
            
    def start (self):
        self.btn_recording.config(bg="tomato", activebackground="tomato")
        self.vid.start_recording()
        self.btn_recording["state"] = "disable"
        self.btn_stop_recording["state"] = "normal"
    
    def stop(self):
        self.vid.stop_recording()
        self.btn_recording.config(bg="white", activebackground="white")
        self.btn_recording["state"] = "normal"
        self.btn_stop_recording["state"] = "disable"
    
    def view(self):
        another_window(self.vid, True, "me")
    
    def snapshot(self):
        self.vid.snapshot()
        
    def setting_camera(self):
        self.camera.setting_now()
        self.camera.media_profile_configuration()
            
class another_window():

    def __init__(self, source, quickview, text =""):
        
        self.vid = source
        # Đặt cờ để xác nhận cửa sổ mới đã được bật hay chưa
        self.quickview = quickview
        
        self.window = tkinter.Toplevel()
        self.window.title("sys_quickview")
        self.window.iconbitmap(".camera_app/image/app.ico")
        self.window.geometry("1000x800")
        
        default_image_ = PIL.Image.open(".camera_app/image/default_image.png")
        default_image= PIL.ImageTk.PhotoImage(default_image_)
        
        # Tạo GUI cho cửa sổ này
        self.make_gui_camera(text= text, window= self.window, width=600, height= 700)
        self.id_image = self.canvas.create_image(0, 0, image=default_image, anchor='nw') 
        self.running = True
        self.delay =10

        self.update_frame()
        # Hàm hủy này sẽ được chạy mỗi khi đóng cửa sổ này
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_frame(self):
        # Lấy từng khung hình từ camera
        ret, frame = self.vid.get_frame()
        
        # Lấy chiều cao, chiều rộng của canvas chứa camera
        self.canvas.update()
        width = self.canvas.winfo_width()
        height= self.canvas.winfo_height()
        
        if ret:
            # Xóa hình ảnh cũ
            self.canvas.delete(self.id_image)
            # Thay đổi kích thước khung hình cho vừa với kích thước canvas
            resized_image = cv2.resize(frame,(width, height))
            self.frame = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
            self.frame = PIL.Image.fromarray(self.frame)
            self.photo = PIL.ImageTk.PhotoImage(image=self.frame)
            # Ve khung hình mới lên canvas
            self.id_image = self.canvas.create_image(0, 0, image=self.photo, anchor='nw')
        else:
            self.canvas.delete(self.id_image)
            self.id_image = self.canvas.create_image(0, 0, image=self.default_image, anchor='nw')  
        # Sau khoảng thời gian delay thì tiếp tục lặp lại cập nhật khung hình
        if self.running:
            self.window.after(self.delay, self.update_frame)



        
    def make_gui_camera(self, text, window, width, height):
        
        # frame chứa camera 
        self.frame_toan_canh=tkinter.Frame(window, width=200, height=400, bg="#3cb371", border=5)
        self.frame_toan_canh.pack(fill=tkinter.BOTH, expand=True)   
        
        # Label hiển thị tên camera, ví dụ "Cam toàn cảnh"
        self.label = tkinter.Label(self.frame_toan_canh, text=text)  
        self.label.pack(side= tkinter.TOP,fill=tkinter.BOTH)

        # Canvas chứa hình ảnh lấy từ camera
        self.canvas = tkinter.Canvas(self.frame_toan_canh, width=width, height=height)
        self.canvas.pack(fill=tkinter.BOTH, expand=True)
    
    def on_close(self):  
        self.window.destroy()
