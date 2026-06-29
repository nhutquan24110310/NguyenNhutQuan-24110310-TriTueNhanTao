# main.py
import sys
from PyQt5.QtWidgets import QApplication
from views.main_window import MainWindow
from controllers.main_controller import MainController

def main():
    # Tạo ứng dụng đồ họa QApplication
    app = QApplication(sys.argv)
    
    # Khởi tạo giao diện (View)
    window = MainWindow()
    
    # Khởi tạo bộ điều hướng điều khiển (Controller) và truyền giao diện vào
    controller = MainController(window)
    
    # Hiển thị giao diện lên màn hình máy tính
    window.show()
    
    # Giữ ứng dụng luôn chạy cho đến khi người dùng tắt cửa sổ
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()