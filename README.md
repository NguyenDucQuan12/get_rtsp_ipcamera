# get_rtsp_ipcamera
Tự động tìm  kiếm các ip của camera và kết nối camera (tối đa 6 thiết bị camera)
## Bắt đầu:
Bước 1: Tạo môi trường ảo  
`python -m venv .camera_app prompt="venv_camera"`  
Bước 2: Kích hoạt môi trường ảo  
`.camera_app\Scripts\activate`  
Nếu mà không kích hoạt được ở `terminal` thì cần chạy lệnh này trước khi chạy lại lệnh trên: `Set-ExcutionPolicy RemoteSigned-Scope CurrentUser`  
Bước 3: Chuyển tất cả các file trong thư mục `DucQuan` vào thư mục `.camera_app`  
Bước 4: Cài đặt các thư viện cần thiết  
`python -m pip install -r requirements.txt`  
Nếu có chỉnh sửa, thay đổi thư viện thì thêm vào file bằng câu lệnh sau: `python -m pip freeze > requirements.txt`  
Nếu xuất hiện lỗi: `pip: Fatal error in ...` thì chạy 2 lệnh sau để khắc phục lỗi:  
`python -m pip install --upgrade --force -reinstall pip`  
`python -m pip freeze`
