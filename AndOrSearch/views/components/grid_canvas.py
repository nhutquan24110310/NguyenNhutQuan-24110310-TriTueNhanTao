# views/components/grid_canvas.py
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtCore import Qt

class GridCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(8) # Khoảng cách giữa các ô
        self.cells = {}
        self.init_ui()

    def init_ui(self):
        # Tạo lưới ô vuông 3x3
        for r in range(3):
            for c in range(3):
                cell = QLabel(self)
                cell.setAlignment(Qt.AlignCenter)
                cell.setFixedSize(110, 110) # Kích thước mỗi ô vuông
                self.grid_layout.addWidget(cell, r, c)
                self.cells[(r, c)] = cell
        
        # Đặt trạng thái trống mặc định ban đầu
        self.update_grid((0, 0), set())

    def update_grid(self, robot_pos, dirty_cells):
        """Cập nhật lại giao diện khi trạng thái robot hoặc map thay đổi"""
        for (r, c), cell in self.cells.items():
            coord_text = f"[{r},{c}]"
            
            if (r, c) == robot_pos:
                # Ô có chứa Robot (Màu xanh neon / Sky blue giống mẫu)
                cell.setText(f"{coord_text}\n\n🤖")
                cell.setStyleSheet("""
                    background-color: #38B6FF; 
                    color: #000000; 
                    font-weight: bold; 
                    font-size: 14px; 
                    border-radius: 10px;
                    border: 2px solid #FFFFFF;
                """)
            elif (r, c) in dirty_cells:
                # Ô bẩn (Màu cam đỏ)
                cell.setText(f"{coord_text}\n\n🍂")
                cell.setStyleSheet("""
                    background-color: #A63A13; 
                    color: #FFFFFF; 
                    font-size: 14px; 
                    border-radius: 10px;
                """)
            else:
                # Ô sạch (Màu xám tối)
                cell.setText(f"{coord_text}")
                cell.setStyleSheet("""
                    background-color: #1F2633; 
                    color: #556080; 
                    font-size: 11px; 
                    border-radius: 10px;
                """)