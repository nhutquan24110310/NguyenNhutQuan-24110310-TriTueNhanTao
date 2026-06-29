# ui/components/grid_widget.py
from PyQt5.QtWidgets import QWidget, QGridLayout, QFrame, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class TileWidget(QFrame):
    def __init__(self, index):
        super().__init__()
        self.index = index
        self.setFixedSize(110, 110)
        self.layout = QVBoxLayout(self)
        
        self.lbl_coord = QLabel(f"[{index//3},{index%3}]")
        self.lbl_coord.setAlignment(Qt.AlignRight | Qt.AlignTop)
        self.lbl_coord.setStyleSheet("color: #64748b; font-size: 10px; font-weight: bold;")
        
        self.lbl_icon = QLabel("")
        self.lbl_icon.setAlignment(Qt.AlignCenter)
        self.lbl_icon.setFont(QFont("Segoe UI Emoji", 24))
        
        self.layout.addWidget(self.lbl_coord)
        self.layout.addWidget(self.lbl_icon)
        self.set_state(0, False)

    def set_state(self, is_dirty, has_robot):
        if has_robot:
            self.lbl_icon.setText("🤖")
            self.setStyleSheet("background-color: #38bdf8; border: 2px solid #0ea5e9; border-radius: 8px;")
        elif is_dirty:
            self.lbl_icon.setText("🍂")
            self.setStyleSheet("background-color: #7c2d12; border: 1px solid #ea580c; border-radius: 8px;")
        else:
            self.lbl_icon.setText("")
            self.setStyleSheet("background-color: #1e293b; border: 1px solid #334155; border-radius: 8px;")

class GridWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)
        self.tiles = []
        for i in range(9):
            tile = TileWidget(i)
            self.tiles.append(tile)
            self.layout.addWidget(tile, i // 3, i % 3)

    def update_grid(self, grid_status, robot_pos):
        for i in range(9):
            is_dirty = grid_status[i] == 1
            has_robot = robot_pos == i
            self.tiles[i].set_state(is_dirty, has_robot)