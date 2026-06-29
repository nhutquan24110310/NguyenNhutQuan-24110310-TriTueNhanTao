# ui/components/result_widget.py
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLabel

class ResultWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("KẾT QUẢ THỰC THI THUẬT TOÁN", parent)
        self.setStyleSheet("""
            QGroupBox { font-weight: bold; color: #38bdf8; border: 1px solid #334155; margin-top: 10px; padding: 10px; border-radius: 6px;} 
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }
        """)
        self.setFixedHeight(85)
        
        layout = QHBoxLayout(self)
        self.lbl_algo = QLabel("Thuật toán: Chưa chọn")
        self.lbl_steps = QLabel("Số bước di chuyển: 0")
        self.lbl_nodes = QLabel("Số Node đã duyệt: 0")
        self.lbl_time = QLabel("Thời gian tính toán: 0.00 ms")
        
        for lbl in [self.lbl_algo, self.lbl_steps, self.lbl_nodes, self.lbl_time]:
            lbl.setStyleSheet("color: #f1f5f9; font-size: 13px;")
            layout.addWidget(lbl)

    def update_results(self, algo_name, steps, nodes, exec_time):
        self.lbl_algo.setText(f"Thuật toán: {algo_name}")
        self.lbl_steps.setText(f"Số bước di chuyển: {steps}")
        self.lbl_nodes.setText(f"Số Node đã duyệt: {nodes}")
        self.lbl_time.setText(f"Thời gian tính toán: {exec_time:.2f} ms")