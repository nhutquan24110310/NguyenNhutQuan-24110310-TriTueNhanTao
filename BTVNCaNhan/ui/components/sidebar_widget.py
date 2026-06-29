# ui/components/sidebar_widget.py
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem

class SidebarWidget(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderLabel("Nhóm Thuật Toán AI")
        self.setStyleSheet("""
            QTreeWidget { background-color: #1e293b; border: none; padding: 5px; color: #f1f5f9; font-size: 13px; }
            QTreeWidget::item { height: 35px; border-bottom: 1px solid #334155; }
            QTreeWidget::item:hover { background-color: #334155; border-radius: 4px; }
            QTreeWidget::item:selected { background-color: #0ea5e9; color: white; border-radius: 4px; }
            QHeaderView::section { background-color: #334155; padding: 6px; font-weight: bold; color: #38bdf8; font-size: 14px; }
        """)
        self.populate_tree()

    def populate_tree(self):
        # Thiết lập đúng cấu trúc các nhóm thuật toán yêu cầu
        groups = {
            "1. Uninformed Search": ["BFS", "DFS", "IDS", "UCS (Theo bước đi)", "UCS (Theo lượng rác)"],
            "2. Informed Search": ["A*", "Greedy", "IDA*"],
            "3. Local Search": ["Simple Hill Climbing", "Stochastic Hill Climbing", "Random Restart Hill Climbing ", "Local Beam Search", "Simulated Annealing"],
            "4. Môi trường thiếu thông tin":["BFS (Không nhìn thấy)","BFS (Thấy 1 phần)"],
        }
        for g_name, algos in groups.items():
            parent_item = QTreeWidgetItem(self)
            parent_item.setText(0, g_name)
            for a in algos:
                child_item = QTreeWidgetItem(parent_item)
                child_item.setText(0, a)
        self.expandAll()