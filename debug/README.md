# Cách debug trong môi trường ảo của python với visual studio code
### Lưu ý nên đặt thư mục ảo có dấu chấm phía trước, ví dụ: `.venv`, `.Camera_ven`  
## Cách 1
* Mở bảng điều khiển
Nhấn `Ctrl+Shift+P` và tìm kiếm `Python: Select interpreter` như ảnh dưới:
<img src="https://github.com/NguyenDucQuan12/get_rtsp_ipcamera/assets/68120446/613483fe-14b9-4440-b795-adc6a0d5718f">
Chọn thư mục chứa môi trường ảo và chọn phiên bản python phù hợp:
<img src="https://github.com/NguyenDucQuan12/get_rtsp_ipcamera/assets/68120446/72e84611-498d-44df-9875-c90a97dc83b2">
Xong nhấn `F5` để debug
## Cách 2
* Thêm file `launch.json`
Nhấn vào tab `debug` bên trái và chọn mũi tên xuống dưới để thêm file `launch.json`:
<img src="https://github.com/NguyenDucQuan12/get_rtsp_ipcamera/assets/68120446/b1729e14-5f8a-470b-913d-ad4f6e276335">
Chọn `add config (thư mục ảo cần debug)` và thêm dòng : `"justMyCode": false`.  
<img src="https://github.com/NguyenDucQuan12/get_rtsp_ipcamera/assets/68120446/209c40aa-44d2-4806-aafb-505c0d188056">
Lưu lại file và nhấn `F5` để debug
