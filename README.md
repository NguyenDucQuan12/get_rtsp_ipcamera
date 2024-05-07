# get_rtsp_ipcamera
Tự động tìm  kiếm các ip của camera và kết nối camera (tối đa 6 thiết bị camera)
## Bắt đầu:
1. Tải về thư mục `DucQuan` và giải nén ra
2. Tải python 3.11.8 từ https://www.python.org/downloads/
3. Tải Visual studio code 
Mở `Visual studio code` --> `Add folder to workspace` --> add DucQuan  
Bước 1: Tạo môi trường ảo `.camera_venv` bên trong thư mục `DucQuan`:  
`python -m venv .camera_app prompt="venv_camera"` hoặc `C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe -m venv .camera_app prompt="venv_camera` Cách sau là dành cho các trường hợp chỉ định phiên bản python cụ thể, khi mà môi trường của bạn có nhiều phiên bản python  
Bước 2: Kích hoạt môi trường ảo:  
`.camera_app\Scripts\activate`  
Nếu mà không kích hoạt được ở `terminal` thì cần chạy lệnh này trước khi chạy lại lệnh trên: `Set-ExcutionPolicy RemoteSigned-Scope CurrentUser`  
Bước 3: Chuyển tất cả các file trong thư mục `DucQuan` vào thư mục `.camera_app`, lưu ý để lại file `requirements.txt`  
Bước 4: Cài đặt các thư viện cần thiết:  
`python -m pip install -r requirements.txt`  
Nếu có chỉnh sửa, thay đổi thư viện thì thêm vào file bằng câu lệnh sau: `python -m pip freeze > requirements.txt`  
Nếu xuất hiện lỗi: `pip: Fatal error in ...` thì chạy 2 lệnh sau để khắc phục lỗi:  
`python -m pip install --upgrade --force -reinstall pip`  
`python -m pip freeze`  
Bước 5: Chạy phần mềm:  
`pyhon .camera_app\main.py`
