import os
import sys

# Đảm bảo root thư mục dự án luôn nằm trong sys.path khi chạy tests
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
