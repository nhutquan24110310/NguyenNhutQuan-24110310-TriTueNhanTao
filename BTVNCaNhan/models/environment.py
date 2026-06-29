# models/environment.py
import random

class VacuumEnvironment:
    def __init__(self):
        self.grid = [0] * 9  # Mảng 9 phần tử đại diện lưới 3x3. 0: Sạch, 1: Có rác
        self.robot_pos = 0   # Vị trí Robot từ 0 đến 8 (Ví dụ: ô góc trái trên là 0, góc phải dưới là 8)
        self.reset()

    def reset(self):
        """Khởi tạo ngẫu nhiên ma trận rác và vị trí của robot"""
        # Ngẫu nhiên mỗi ô có 50% tỷ lệ có rác
        self.grid = [random.choice([0, 1]) for _ in range(9)]
        # Ngẫu nhiên vị trí xuất phát của robot
        self.robot_pos = random.randint(0, 8)
        
    def get_coordinates(self, pos):
        """Chuyển đổi chỉ số phẳng (0-8) thành tọa độ dòng và cột (hàng, cột)"""
        return pos // 3, pos % 3