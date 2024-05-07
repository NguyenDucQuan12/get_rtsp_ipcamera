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
https://cxsmz04.na1.hubspotlinks.com/Ctc/LW+113/cxSmZ04/VVYFCk3rhGMSW21GdbD7n3WsgW6WXg815dMGnbN1n_9Y67T5yYW69tBBd6lZ3l2W329lL-4vklzvW3Pfc7f1RXC34N4XvFX_Fcl4cW1yDcCT2jPt49W7k3ydd4RvMKjW5K6XRB7CH1SlW1mjTmK5mQhzCW2VFNzx7SWLH9W633kYt5pJTyJN89LfR_1gv4qW2Pr_Dl8KVx-6W4Bgg-k7RwfQnW6xf3J35Q2twvW2rNxSh68_fWxW3mvL-240dlXnW1Xl22K5w17CnW42_mw559lHwyW94vRrd6ghfLCW3WXGW26XJpyTW3wqZ_y8Md47kW6HVJhw3zTkRZW79872C1YdVBjN3yWvpRjcdmrW8HZJCX7Mpnr3W8wpbwt6CSdr0W1PDXNx3JLM3YN8_kB3HVQSHjW1R7SYw1BPycrW7df4bG1jvdDMW4hcTzS535NK0N7vNVxQlXWG1W1x_vdp2J56LcW6r9ZY58hzKz0W7q5D3677S7dxW1Qsv552CsF1GW2qpN698MVw3mVTCZmg4HXm3FW3M598W196Q1sW3BcDT96wQkLlW3FyZ1_8b4qnbW1QVw6P5_f74rW8mzX005VjhSLVLq9bG78C2F-W4VYl3T98-_tCW8GwZVf18psyhW3Xf_9P528ZlnW4hZqlh80WKvmW3ZsNk65WL6qjW55YYLy5-m670W5YZ-GB5hblxkW4qd9Rn99ddZHW2tB-2k2pxmtXf25Y1Cx04
