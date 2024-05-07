import sys
log_file_path = ".camera_app/log/log.txt"
log_error_file_path = ".camera_app/log/error_log.txt"
# Ghi tất cả các thông báo bằng phương thức print vào file long, các lỗi xuất hiện vào file error_log
# Bởi vì khi đóng gói ứng dụng thì sẽ không có terminal hiển thị các thông tin này, vì vậy cần lưu vào file
sys.stdout = open(log_file_path, encoding="utf-8", mode="a")
sys.stderr = open(log_error_file_path, encoding="utf-8", mode="a")