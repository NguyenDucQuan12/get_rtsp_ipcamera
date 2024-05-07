import socket
import threading
import json
from concurrent.futures import ThreadPoolExecutor
from itertools import product
import tkinter as tk
from get_rtsp import Camera

# Đường dẫn đến file chứa thông tin đăng nhập về CSDL
json_filename = ".camera_app/ip_camera/storage_ip.json"

MY_HOSTNAME = socket.gethostname() # Tên laptop
MY_IP_ADDR = socket.gethostbyname(MY_HOSTNAME) # Địa chỉ IPV4

# Ví dụ ip là 169.254.184.0 thì sẽ loại 1 địa chỉ cuối và bắt đầu tìm kiếm từ 169.254.184.0 đến 169.254.184.254
BASE_ADDR1 = '.'.join(MY_IP_ADDR.split('.')[:-1])
# Ví dụ ip là 169.254.184.0 thì sẽ loại 2 địa chỉ cuối và bắt đầu tìm kiếm từ 169.254.0.0 đến 169.254.254.254
# Chỉ dùng trường hợp này khi có 2 camera mà cách phía trên chỉ tìm được 1 camera
BASE_ADDR2 = '.'.join(MY_IP_ADDR.split('.',2)[:-1])

RTSP_PORT = 554

SOCKET_TIMEOUT = 0.01

def check_rtsp(ip= None, ip_full = None):
    if ip:
        ipv4 = f'{BASE_ADDR2}.{ip[0]}.{ip[1]}'
    else:
        ipv4 = ip_full
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(SOCKET_TIMEOUT)
    exitcode = sock.connect_ex((ipv4, RTSP_PORT))
    sock.close()
    if not exitcode:
        print('📷 Found', ipv4)
        return ipv4, True
    return None, False
        
class Find_ip_camera(object):
    def __init__(self, window):
        
        self.window = tk.Tk()
        self.window.iconbitmap(".camera_app/image/app.ico")
        self.window.geometry("400x300")
        self.window.title("Tìm kiếm ip camera")
        self.object = window
        self.rtsp_ips = []
        self.sources =[]
        
        start_label = tk.Label(self.window, text="Phần mềm chỉ dò tìm được các camera có chuẩn ONVIF")
        start_label.pack()
        start_label = tk.Label(self.window, text="Để đảm bảo kết nối ổn định, chỉ kết nối cùng lúc tối đa 6 camera")
        start_label.pack()
        start_label = tk.Label(self.window, text="Quá trình tìm kiếm chưa đến 2 phút, vui lòng đợi")
        start_label.pack()
        
        self.show_ip_text = tk.StringVar()
        self.get_ip_button = tk.Button(self.window, textvariable= self.show_ip_text, background= "tomato", cursor="hand2", command= lambda: self.find_ip(reload=True))
        self.show_ip_text.set(" Camera không có sẵn. Đang dò ip ...")
        self.get_ip_button.pack()
        
        self.connect_camera = tk.Button(self.window, text= "Kết nối với các camera tìm được", cursor="hand2", command = self.connect_ip_camera)
        self.end_label = tk.Label(self.window, text="Không tìm thấy camera nào cả, kiểm tra lại kết nối ethernet")
        
        get_license_in_thread = threading.Thread(target=self.find_rtsp_ips)
        get_license_in_thread.daemon = True
        get_license_in_thread.start()
        
        self.window.mainloop()

    def find_rtsp_ips(self):
        # Lấy thông tin đăng nhập từ file json
        # self.get_ip_button["state"] = "disable"
        try:
            with open(json_filename, 'r') as inside:
                self.data = json.load(inside)
                for i in range(1, 7):
                    ip_key = f'IP_cam{i}'
                    ip = self.data['camera'].get(ip_key)
                    if ip:
                        _, result = check_rtsp(ip_full=ip)
                        if result:
                            self.rtsp_ips.append(ip)
                if not self.rtsp_ips:
                    self.find_rtsp_ips_2(self.rtsp_ips)
                else:
                    self.show_ip_text.set("Bấm để tìm kiếm thêm ip")
                    for ip in self.rtsp_ips:
                        self.show_result(ip)
                    self.connect_camera.pack()
        except Exception as e:
            print(f"Lỗi khi đọc tệp JSON: {e}")
        
    def find_ip(self, reload = False):
        if reload:
            self.show_ip_text.set("Đang dò ip ...")
            get_license_in_thread = threading.Thread(target=self.find_rtsp_ips_2, args=(self.rtsp_ips,))
            get_license_in_thread.start()
            
    def show_result(self, ip):
        ip_label = tk.Label(self.window, text=ip)
        ip_label.pack()
    
    def find_rtsp_ips_2(self,rtsp_ips):
        self.get_ip_button["state"] = "disable"
        self.connect_camera["state"] = "disable"
        print('🔎 Scanning...')
        num_threads = 10
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            # Tạo danh sách các cặp (ip_index, ip)
            ip_combinations = product(range(0, 255), repeat=2)
            # Thực hiện kiểm tra RTSP cho từng cặp IP trong danh sách bằng cách sử dụng executor map
            # results= executor.map(check_rtsp, ip_combinations) # Chỉ trả về 1 giá trị
            results = list(executor.map(check_rtsp, ip_combinations)) # Trả về nhiều giá trị
            i=1
            for ipv4, status in results:
                if status:
                    if i==7:
                        break
                    if ipv4 in rtsp_ips:
                        i+=1
                        continue
                    rtsp_ips.append(ipv4)
                    ip_key = f'IP_cam{i}'
                    self.data['camera'][ip_key] = ipv4
                    with open(json_filename, 'w') as outfile:
                        json.dump(self.data, outfile, indent=4)
        self.show_ip_text.set("Các camera có sẵn, bấm để tìm kiếm lại")
        self.get_ip_button["state"] = "normal"
        self.connect_camera["state"] = "normal"
    
    def connect_ip_camera(self):
        for ip in self.rtsp_ips:
            print(ip)
            camera = Camera(ip= ip, user= "", password="")
            rtsp = camera.get_rtsp_stream()
            self.sources.append((ip, rtsp, camera))
            print(self.sources)
        # Mở phần mềm
        self.window.destroy()
        self.object(tk.Tk(), "Dức Quân", self.sources)

    