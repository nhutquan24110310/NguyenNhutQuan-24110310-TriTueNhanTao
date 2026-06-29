import math
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QPen, QFont, QPainterPath # Thêm QPainterPath ở đây

class MapWidget(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.nodes = {}
        self.setStyleSheet("background-color: #21222c; border: none;")

    def init_map(self, variables, positions, constraints):
        self.scene.clear()
        self.nodes = {}
        
        # 1. Vẽ các đường nối ràng buộc giữa các đơn vị kề nhau
        pen_line = QPen(QColor("#44475a"), 2, Qt.DashLine)
        drawn_edges = set()
        for u, neighbors in constraints.items():
            for v in neighbors:
                edge = tuple(sorted((u, v)))
                if edge not in drawn_edges and u in positions and v in positions:
                    drawn_edges.add(edge)
                    p1 = positions[u]
                    p2 = positions[v]
                    # Nối từ tâm hình khối chữ nhật (115x60)
                    self.scene.addLine(p1[0] + 57, p1[1] + 30, p2[0] + 57, p2[1] + 30, pen_line)

        # 2. Vẽ các khối tên đơn vị hành chính bo góc bằng QPainterPath
        for var in variables:
            if var in positions:
                x, y = positions[var]
                
                # Tạo đường path hình chữ nhật bo góc
                path = QPainterPath()
                # Tham số: x, y, width, height, xRadius (độ bo x), yRadius (độ bo y)
                path.addRoundedRect(x, y, 115, 60, 10, 10)
                
                # Thêm path vào scene
                rect = self.scene.addPath(
                    path, 
                    QPen(QColor("#f8f8f2"), 1.5), 
                    QBrush(QColor("#6272a4"))
                )
                
                # Ghi tên Huyện/Thành phố
                text = self.scene.addText(var)
                text.setDefaultTextColor(QColor("#f8f8f2"))
                text.setFont(QFont("Segoe UI", 9, QFont.Bold))
                text.setPos(x + 10, y + 16)
                
                self.nodes[var] = rect

    def update_color(self, var, color_name):
        colors = {
            "Vàng": QColor("#ffb86c"),
            "Hồng": QColor("#ff79c6"),
            "Tím": QColor("#bd93f9"),
            "Xanh Lá": QColor("#50fa7b"),
            "Xóa": QColor("#6272a4")
        }
        if var in self.nodes:
            self.nodes[var].setBrush(QBrush(colors.get(color_name, QColor("#6272a4"))))

    def update_all_colors(self, assignment):
        for var, color in assignment.items():
            self.update_color(var, color)