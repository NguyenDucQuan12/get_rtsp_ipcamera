import tkinter as tk                # python 3
from tkinter import font as tkfont  # python 3
from tkinter import ttk

# Chuyển đổi frame giữa màn hình : https://stackoverflow.com/questions/67992255/switch-between-two-frames-in-tkinter-in-separates-files

class Setting(tk.Toplevel):

    def __init__(self, master=None, onvif_camera = None, *args, **kwargs):
        tk.Toplevel.__init__(self, master, *args, **kwargs)
        self.onvif_camera = onvif_camera
        self.title("Cài đặt")
        self.iconbitmap(".camera_app/image/app.ico")
        self.geometry("700x700")
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, Information_Device, Track_with_yolo):
            page_name = F.__name__
            frame = F(parent=container, controller=self, camera = self.onvif_camera)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller, camera):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Xem thông tin thiết bị",
                            command=lambda: controller.show_frame("Information_Device"))
        button2 = tk.Button(self, text="Cài đặt theo dõi",
                            command=lambda: controller.show_frame("Track_with_yolo"))
        button1.pack()
        button2.pack()


class Information_Device(tk.Frame):

    def __init__(self, parent, controller, camera):
        tk.Frame.__init__(self, parent)
        self.camera = camera
        self.columnconfigure((0,1,2,3,4,5,6,7), weight =1, uniform="a")
        # self.columnconfigure(1, weight =6, uniform="a")
        self.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20), weight =1, uniform="a")
        
        self.controller = controller
        label = tk.Label(self, text="Vui lòng khởi động lại phần mềm sau khi thay đổi cài đặt", font=controller.title_font)
        label.grid(row=0, column=0, columnspan=8)
        self.make_gui_info_device()
        self.get_info_device()
        self.get_info_current()
        self.set_profile()
        self.set_value_can_change()
        button = tk.Button(self, text="Quay lại", border= 2, cursor="hand2",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row=20, column= 0)
        
    def make_gui_info_device(self):
        label = tk.Label(self, text= "Tên thiết bị: " )
        label.grid(row=1, column=0)
        label = tk.Label(self, text= "Thương hiệu: " )
        label.grid(row=2, column=0)
        label = tk.Label(self, text= "Tên cấu hình: " )
        label.grid(row=3, column=0)
        label = tk.Label(self, text= "Encoding: " )
        label.grid(row=4, column=0)
        label = tk.Label(self, text= "Độ phân giải: " )
        label.grid(row=5, column=0)
        label = tk.Label(self, text= "FPS: " )
        label.grid(row=6, column=0)
        label = tk.Label(self, text= "Chất lượng: " )
        label.grid(row=7, column=0)
        label = tk.Label(self, text= "Cấu hình H264: " )
        label.grid(row=8, column=0)
        label = tk.Label(self, text= "GOV Length: " )
        label.grid(row=9, column=0)
        label = tk.Label(self, text= "Tên người dùng: " )
        label.grid(row=1, column=3)
        label = tk.Label(self, text= "Mật khẩu: " )
        label.grid(row=2, column=3)
        label = tk.Label(self, text= "Quyền hạn: " )
        label.grid(row=3, column=3)
        
        self.max_setting_button = tk.Button(self, text="Cấu hình tối đa", border= 2, cursor="hand2", command=self.max_setting_camera)
        self.max_setting_button.grid(row=18 , column= 2)
        self.max_setting_button = tk.Button(self, text="Mặc định", border= 2, cursor="hand2", command=self.max_setting_camera)
        self.max_setting_button.grid(row=18 , column= 3)
        self.max_setting_button = tk.Button(self, text="Áp dụng", border= 2, cursor="hand2", command=self.apply_new_setting)
        self.max_setting_button.grid(row=20 , column= 4)
        
    
    def get_info_device(self):
        self.model = self.camera.model() # return DMC-2036BZW
        self.manufacturer = self.camera.manufacturer() # return D-max
        self.resolutions_available = self.camera.resolutions_available() # Return [(1920, 1080), (1600, 900), (1280, 720), (960, 540), (640, 360), (320, 180)]
        self.qualitiRangge = self.camera.qualityRange() # return (1,100)
        self.fps_min_max = self.camera.frame_rate_range() # return (1, 25)
        self.gov_length_min_max = self.camera.gov_length_range() # return (1, 255)
        self.H264_support = self.camera.H264_profile_support() # return 'Baseline','Main','High
        self.user_info = self.camera.GetUser() # return user, password, role
        
    def get_info_current(self):
        self.name_profile, self.encoding, self.width, self.heighth, self.quality_current, self.fps_current, self.bitrate_current, self.GOV_length_current, self.encoding_profile = self.camera.detail_video()
  
    def set_profile(self):
        label = tk.Label(self, text=self.model )
        label.grid(row=1, column=1, sticky=tk.W)
        label = tk.Label(self, text= self.manufacturer)
        label.grid(row=2, column=1, sticky=tk.W)
        label = tk.Label(self, text= self.name_profile )
        label.grid(row=3, column=1, sticky=tk.W)
        label = tk.Label(self, text=self.encoding)
        label.grid(row=4,column=1, sticky=tk.W)
        label = tk.Label(self, text=self.user_info[0] )
        label.grid(row=1,column=4, sticky=tk.W)
        label = tk.Label(self, text=self.user_info[1] )
        label.grid(row=2,column=4, sticky=tk.W)
        label = tk.Label(self, text=self.user_info[2] )
        label.grid(row=3,column=4, sticky=tk.W)
        
    def set_value_can_change(self):
        self.resolution_combobox = ttk.Combobox(self,
            state="readonly",
            values=[],
            # postcommand=dropdown_opened # Khi mở danh sách thì sẽ chạy lệnh
        )
        self.resolution_combobox.set((self.width, self.heighth))
        # Thêm 1 giá trị vào list cũ, không làm mất các giá trị trước
        values = list(self.resolution_combobox["values"])
        self.resolution_combobox["values"] = values + self.resolutions_available
        self.resolution_combobox.grid(row= 5, column= 1, sticky=tk.W)
        
        self.fps_combobox = ttk.Combobox(self,
                                state="readonly",
                                values=[])
        self.fps_combobox.set(self.fps_current)
        list_fps_avalable = list(range(self.fps_min_max[0], self.fps_min_max[1]+1)) # (1 , 10)retun [1,2,3,4,5,6,7,8,9]
        self.fps_combobox["values"] = list_fps_avalable
        self.fps_combobox.grid(row= 6, column= 1, sticky=tk.W)
        
        self.quality_combobox = ttk.Combobox(self,
                                             state="readonly",
                                             values=[])
        self.quality_combobox.set(self.quality_current)
        list_quality_avalable = list(range(self.qualitiRangge[0], self.qualitiRangge[1]+1)) # (1 , 10)retun [1,2,3,4,5,6,7,8,9]
        self.quality_combobox["values"] = list_quality_avalable
        self.quality_combobox.grid(row= 7, column= 1, sticky=tk.W)
        
        self.H264_support_combobox = ttk.Combobox(self,
                                                state="readonly",
                                                values=[])
        self.H264_support_combobox.set(self.encoding_profile)
        self.H264_support_combobox["values"] = self.H264_support
        self.H264_support_combobox.grid(row= 8, column= 1, sticky=tk.W)
        
        self.GOV_length_combobox = ttk.Combobox(self,
                                                state="readonly",
                                                values=[])
        self.GOV_length_combobox.set(self.GOV_length_current)
        list_GOV_length_avalable = list(range(self.gov_length_min_max[0], self.gov_length_min_max[1]+1)) # (1 , 10)retun [1,2,3,4,5,6,7,8,9]
        self.GOV_length_combobox["values"] = list_GOV_length_avalable
        self.GOV_length_combobox.grid(row= 9, column= 1, sticky=tk.W)

    def max_setting_camera(self):
        self.camera.set_max_setting_camera()

    def apply_new_setting(self):
        new_resolutions = self.resolution_combobox.current()
        new_fps = self.fps_combobox.get()
        new_fps = int(new_fps)
        new_quality = self.quality_combobox.get()
        new_profile_H264 = self.H264_support_combobox.get()
        new_GOV_length = self.GOV_length_combobox.get()
        new_width = self.resolutions_available[new_resolutions][0]
        new_width = int(new_width)
        new_height = self.resolutions_available[new_resolutions][1]
        new_height = int(new_height)
        self.camera.apply_new_setting(width =new_width , height=new_height , fps= new_fps , quality= new_quality, H264_profile=new_profile_H264 , GOV_length= new_GOV_length)

class Track_with_yolo(tk.Frame):

    def __init__(self, parent, controller, camera):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ẩn cửa sổ gốc

    app = Setting(master=root)
    app.mainloop()
