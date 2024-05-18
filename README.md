# get_rtsp_ipcamera
Tự động tìm  kiếm các ip của camera và kết nối camera (tối đa 6 thiết bị camera), lượng CPU tiêu thụ nếu không sử dụng chức năng theo dõi là 5% một camera, nếu ghi hình lị là 9-10% CPU cho một camera  
Vì vậy số lượng 6 camera là điều kiện lý tưởng cho việc hoạt động của máy tính để có thể xem được phần mềm  
Phần mềm không cần kết nối mạng, nên đảm bảo không thể phát tán, leak hình ảnh từ camera cho người khác  
## Sơ đồ kết nối camera với máy tính  

## Bắt đầu:
1. Tải về thư mục `DucQuan` và giải nén ra
2. Tải python 3.11.8 từ https://www.python.org/downloads/
3. Tải Visual studio code 
Mở `Visual studio code` --> `Add folder to workspace` --> add DucQuan  
Bước 1: Tạo môi trường ảo `.camera_venv` bên trong thư mục `DucQuan`:  
`python -m venv .camera_app prompt="venv_camera"` hoặc `C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe -m venv .camera_app prompt="venv_camera` Cách sau là dành cho các trường hợp chỉ định phiên bản python cụ thể, khi mà môi trường của bạn có nhiều phiên bản python  
Bước 2: Kích hoạt môi trường ảo:  
`.camera_app\Scripts\activate`  
Nếu mà không kích hoạt được ở `terminal` thì cần chạy lệnh này trước khi chạy lại lệnh trên: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`  
Bước 3: Chuyển tất cả các file trong thư mục `DucQuan` vào thư mục `.camera_app`, lưu ý để lại file `requirements.txt`  
Bước 4: Cài đặt các thư viện cần thiết:  
`python -m pip install -r requirements.txt`  
Nếu có chỉnh sửa, thay đổi thư viện thì thêm vào file bằng câu lệnh sau: `python -m pip freeze > requirements.txt`  
Nếu xuất hiện lỗi: `pip: Fatal error in ...` thì chạy 2 lệnh sau để khắc phục lỗi:  
`python -m pip install --upgrade --force -reinstall pip`  
`python -m pip freeze`  
Bước 5: Chạy phần mềm:  
`pyhon .camera_app\main.py`  lần đầu sẽ tìm kiếm các ip, từ lần sau sẽ tự động hiển thị các ip đã có
## Hình ảnh phần mềm  
![image](https://github.com/NguyenDucQuan12/get_rtsp_ipcamera/assets/68120446/122f2c81-7c38-48c8-a0fc-07a209fd27bc)

![image](https://github.com/NguyenDucQuan12/get_rtsp_ipcamera/assets/68120446/39b22eb6-b92b-4af1-a773-947caf1f6446)

![image](https://github.com/NguyenDucQuan12/get_rtsp_ipcamera/assets/68120446/3254b7fd-804d-4431-b1ae-0303ecca56f3)

## Các camera đã thử nghiệm  
### Dmax : Dmax DMC 2036BZW, Dmax DMC 2054 BZW
