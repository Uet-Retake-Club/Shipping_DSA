Listed directory Shipping_DSA
Viewed README.md:1-211
Viewed requirements.txt:1-13
Ran command: `Get-ChildItem -Recurse -File | Select-Object FullName`
Viewed main.py:1-114
Ran command: `python src/main.py`
Ran command: `python -m src.main`
Ran command: `pytest`
Ran command: `python -m unittest discover tests`
Ran command: `python -m src.main --data data/sample_medium_50_nodes.json`
Viewed dataset_generator.py:1-60
Viewed dataset_generator.py:190-244
Edited main.py
Edited dataset_generator.py
Ran command: `python src/main.py`
Ran command: `python src/generators/dataset_generator.py`

Dưới đây là hướng dẫn chi tiết cách chạy và kiểm thử project **Shipping_DSA** (Tối ưu mạng lưới giao hàng bằng Cây khung nhỏ nhất - MST: Kruskal & Prim).

---

### 1. Chuẩn bị môi trường & Thư viện

Mở terminal (PowerShell hoặc Command Prompt) tại thư mục gốc của project `c:\Dev_Uni\Shipping_DSA`.

*(Tùy chọn)* Cài đặt các thư viện bổ trợ từ [requirements.txt]():
```bash
pip install -r requirements.txt
```

---

### 2. Chạy chương trình chính ([src/main.py]())

Chương trình chính sẽ nạp đồ thị, thực thi cả 2 thuật toán **Kruskal (DSU)** và **Prim (Min-Heap)**, so sánh chi phí, số cạnh được chọn và thời gian thực thi.

#### 🔹 Chạy với mạng lưới mặc định (10 nút - Nội thành Hà Nội):
```bash
python src/main.py
```
*(hoặc dùng `python -m src.main`)*

#### 🔹 Chạy chi tiết (in danh sách các tuyến đường được chọn):
Thêm cờ `--verbose` hoặc `-v`:
```bash
python src/main.py -v
```

#### 🔹 Chạy với các bộ dữ liệu khác nhau:
Bạn có thể chỉ định file JSON trong thư mục `data/` qua cờ `--data` hoặc `-d`:

* **Mạng lưới trung bình (50 nút):**
  ```bash
  python src/main.py --data data/sample_medium_50_nodes.json
  ```

* **Mạng lưới lớn (500 nút):**
  ```bash
  python src/main.py --data data/sample_large_500_nodes.json
  ```

---

### 3. Sinh / Tái tạo dữ liệu mẫu ([dataset_generator.py]())

Nếu muốn tạo lại các file dữ liệu mạng lưới (JSON và CSV) trong thư mục `data/`:
```bash
python src/generators/dataset_generator.py
```
Lệnh này sẽ tự động tạo:
- `data/sample_small_10_nodes.json` & `data/small_nodes.csv`, `data/small_edges.csv`
- `data/sample_medium_50_nodes.json` & `data/medium_nodes.csv`, `data/medium_edges.csv`
- `data/sample_large_500_nodes.json` & `data/large_nodes.csv`, `data/large_edges.csv`

---

### 4. Chạy Unit Test kiểm tra tính đúng đắn

Project có sẵn bộ 19 bài kiểm thử bao phủ toàn bộ cấu trúc dữ liệu và thuật toán:
- [test_dsu.py](): Kiểm tra Disjoint Set Union (Union by rank, Path compression).
- [test_min_heap.py](): Kiểm tra Min-Heap.
- [test_graph.py](): Kiểm tra cấu trúc Graph, nạp/xuất JSON, CSV.
- [test_kruskal.py](): Kiểm tra thuật toán Kruskal.
- [test_prim.py](): Kiểm tra thuật toán Prim.

Chạy toàn bộ unit tests bằng lệnh:
```bash
python -m unittest discover tests
```
*(Nếu môi trường của bạn đã cài `pytest`, bạn cũng có thể gõ `pytest`)*