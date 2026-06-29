import random

class MapGenerator:
    @staticmethod
    def get_dong_thap_map():
        # 12 Đơn vị hành chính tỉnh Đồng Tháp
        variables = [
            'Hồng Ngự H.', 'Hồng Ngự TP.', 'Tân Hồng', 'Tam Nông', 
            'Thanh Bình', 'Tháp Mười', 'Cao Lãnh H.', 'Cao Lãnh TP.', 
            'Lấp Vò', 'Lai Vung', 'Sa Đéc', 'Châu Thành'
        ]
        
        # Miền giá trị màu sắc lấy cảm hứng từ ảnh bản đồ thực tế
        domains = {var: ['Vàng', 'Hồng', 'Tím', 'Xanh Lá'] for var in variables}
        
        # Ràng buộc giáp ranh địa lý thực tế giữa các huyện/thành phố
        constraints = {
            'Hồng Ngự H.': ['Hồng Ngự TP.', 'Tân Hồng', 'Tam Nông', 'Thanh Bình'],
            'Hồng Ngự TP.': ['Hồng Ngự H.', 'Tân Hồng', 'Tam Nông'],
            'Tân Hồng': ['Hồng Ngự H.', 'Hồng Ngự TP.', 'Tam Nông', 'Tháp Mười'],
            'Tam Nông': ['Hồng Ngự H.', 'Hồng Ngự TP.', 'Tân Hồng', 'Thanh Bình', 'Cao Lãnh H.', 'Tháp Mười'],
            'Thanh Bình': ['Hồng Ngự H.', 'Tam Nông', 'Cao Lãnh H.', 'Lấp Vò'],
            'Tháp Mười': ['Tân Hồng', 'Tam Nông', 'Cao Lãnh H.'],
            'Cao Lãnh H.': ['Tam Nông', 'Thanh Bình', 'Tháp Mười', 'Cao Lãnh TP.', 'Lấp Vò', 'Sa Đéc', 'Châu Thành'],
            'Cao Lãnh TP.': ['Cao Lãnh H.', 'Lấp Vò'],
            'Lấp Vò': ['Thanh Bình', 'Cao Lãnh H.', 'Cao Lãnh TP.', 'Lai Vung', 'Sa Đéc'],
            'Lai Vung': ['Lấp Vò', 'Sa Đéc', 'Châu Thành'],
            'Sa Đéc': ['Cao Lãnh H.', 'Lấp Vò', 'Lai Vung', 'Châu Thành'],
            'Châu Thành': ['Cao Lãnh H.', 'Sa Đéc', 'Lai Vung']
        }
        
        # Tọa độ địa lý tương đối mô phỏng dáng bản đồ Đồng Tháp thực tế
        positions = {
            'Hồng Ngự H.': (40, 30),
            'Hồng Ngự TP.': (160, 65),
            'Tân Hồng': (290, 30),
            'Tam Nông': (210, 150),
            'Thanh Bình': (70, 240),
            'Tháp Mười': (410, 210),
            'Cao Lãnh H.': (285, 300),
            'Cao Lãnh TP.': (215, 390),
            'Lấp Vò': (80, 440),
            'Lai Vung': (150, 540),
            'Sa Đéc': (260, 490),
            'Châu Thành': (380, 550)
        }
        
        return variables, domains, constraints, positions

    @staticmethod
    def get_random_map(num_nodes=5):
        variables = [f'Node_{i}' for i in range(num_nodes)]
        domains = {var: ['Đỏ', 'Xanh', 'Vàng'] for var in variables}
        constraints = {var: [] for var in variables}
        
        # Tạo ràng buộc ngẫu nhiên
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                if random.random() > 0.5:
                    constraints[variables[i]].append(variables[j])
                    constraints[variables[j]].append(variables[i])
        return variables, domains, constraints