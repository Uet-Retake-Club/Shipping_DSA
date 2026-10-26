# 🚚 Smart Delivery Network Design Using Minimum Spanning Tree (MST)

> **Môn học:** Cấu trúc Dữ liệu & Giải thuật (Data Structures & Algorithms - DSA)  
> **Chủ đề:** Tối ưu hóa và quy hoạch mạng lưới giao nhận thông minh bằng Cây bao trùm nhỏ nhất (MST)  
> **Ngôn ngữ:** Python 3  
> **Bộ slide thuyết trình tương tác:** [`slides/index.html`](slides/index.html)  
> **Kịch bản thuyết trình & Vấn đáp phản biện:** [`docs/md/presentation_guide.md`](docs/md/presentation_guide.md)

---

## 📌 1. Giới Thiệu Dự Án

Dự án tập trung vào việc mô hình hóa hệ thống bưu chính và trung tâm phân loại giao vận (Logistics Network) thành bài toán đồ thị vô hướng có trọng số. Hệ thống áp dụng và so sánh ba thuật toán kinh điển tìm Cây bao trùm nhỏ nhất (**Borůvka**, **Kruskal**, **Prim**) nhằm tìm ra mạng lưới tuyến đường xương sống (Backbone Network) kết nối 100% các điểm nút bưu cục với tổng chi phí đầu tư và duy trì hạ tầng nhỏ nhất.

### 🌟 Điểm Nhấn Kỹ Thuật (Key Highlights)
1. **Tự cài đặt cấu trúc dữ liệu cốt lõi (Không dùng thư viện có sẵn cho DSA):**
   - **`DSU` (Disjoint Set Union):** Tối ưu hóa đồng thời bằng *Path Compression* và *Union by Rank*, đạt độ phức tạp $O(\alpha(V))$ cho mỗi thao tác.
   - **`MinHeap` & `IndexedMinHeap`:** Hàng đợi ưu tiên tự chế hỗ trợ cập nhật độ ưu tiên `decrease_key` cho thuật toán Eager Prim, giảm thiểu không gian bộ nhớ còn $O(V)$.
2. **So sánh đa thuật toán toàn diện:**
   - **Borůvka (1926):** Thuật toán MST đầu tiên trong lịch sử, hoạt động theo cơ chế co cụm song song từng vòng (Round-by-Round Component Merging).
   - **Kruskal (1956):** Chiến lược tham lam theo cạnh, tối ưu trên đồ thị thưa ($O(E \log E)$).
   - **Prim (1957):** Chiến lược tham lam theo đỉnh (Lazy & Eager), tối ưu trên đồ thị dày ($O(E \log V)$).
3. **Thực nghiệm trên mạng lưới thực tế:**
   - Tập dữ liệu **Hanoi Metropolitan Logistics Network** gồm 22 điểm nút (3 Mega Hubs, 9 Warehouses/DCs, 10 Delivery Points) với tọa độ GPS thực tế và công thức khoảng cách mặt cầu **Haversine Formula**.
   - Giúp cắt giảm hơn **35.6%** chi phí hạ tầng so với mạng lưới ban đầu.

---

## 🖥️ 2. Slide Thuyết Trình Tương Tác (HTML / CSS / JS)

Dự án đi kèm bộ Slide thuyết trình hiện đại, giao diện Dark Mode chuẩn công nghệ, mượt mà và tương tác trực tiếp tại:
👉 **[`slides/index.html`](slides/index.html)** *(Chỉ cần click đúp mở trực tiếp bằng bất kỳ trình duyệt nào: Chrome, Edge, Firefox, Brave,...)*

### 🎮 Các Tính Năng Của Slide:
- **Phím tắt điều hướng:**
  - `➔` / `Space` / `PageDown`: Chuyển sang slide kế tiếp.
  - `⬅` / `PageUp`: Quay lại slide trước.
  - `S`: Bật / Tắt cửa sổ **Ghi chú người thuyết trình (Speaker Notes)** có sẵn lời thoại kịch bản cho từng slide.
  - `O`: Mở bảng **Tổng quan tất cả các Slide (Slide Overview)** để nhảy nhanh.
  - `F`: Chế độ Toàn màn hình (Fullscreen).
- **Interactive Graph Simulator (Slide 9):**
  - Mô phỏng trực quan thuật toán Kruskal & Prim từng bước một (Step-by-Step).
  - Đổi màu cạnh, hiển thị kiểm tra chu trình DSU và tính tổng trọng số trực tiếp theo thời gian thực.
- **Presentation Timer (Đồng hồ thuyết trình):**
  - Tự động đếm giờ, cảnh báo màu vàng khi qua 10 phút và màu đỏ khi qua 13 phút.
- **Bộ câu hỏi Mock Defense tương tác (Slide 12):**
  - Click vào từng câu hỏi hóc búa của Hội đồng để lật mở đáp án chuẩn mực.

---

## 📖 3. Hướng Dẫn Thuyết Trình & Kịch Bản Phản Biện

Tài liệu chi tiết hướng dẫn từng bước chuẩn bị thuyết trình:
👉 **[`docs/md/presentation_guide.md`](docs/md/presentation_guide.md)**
- **Kịch bản lời dẫn (Speaker Script):** Lời thoại chi tiết từ phần mở đầu, phân tích thuật toán đến kết luận.
- **Phân bổ thời lượng:** Chuẩn 12 - 15 phút thuyết trình + 5 phút phản biện.
- **Bộ câu hỏi vấn đáp chuyên sâu (Mock Defense Q&A):**
  1. *Tại sao chọn MST mà không dùng Dijkstra hay TSP?*
  2. *Thuật toán có đúng khi trọng số cạnh âm không?*
  3. *Xử lý đồ thị không liên thông (Rừng bao trùm MSF) như thế nào?*
  4. *Tính duy nhất của cây MST khi có cạnh trùng trọng số?*
  5. *Hàm Ackermann nghịch đảo $\alpha(V)$ và ý nghĩa trong DSU?*

---

## 📂 4. Cấu Trúc Thư Mục Dự Án

```
Shipping_DSA/
├── README.md                      # Giới thiệu & Hướng dẫn tổng quan
├── requirements.txt               # Thư viện phụ trợ (pytest, pandas, networkx, folium)
├── slides/                        # Bộ Slide thuyết trình tương tác
│   ├── index.html                 # Slide HTML chính (12 slide chuẩn mực)
│   ├── style.css                  # Giao diện Dark mode, Glassmorphism, animations
│   └── script.js                  # Engine điều khiển, Timer, Speaker Notes, Simulator
├── src/
│   ├── algorithms/
│   │   ├── boruvka.py             # Thuật toán Boruvka & Round-by-round merging
│   │   ├── kruskal.py             # Thuật toán Kruskal
│   │   ├── prim.py                # Thuật toán Prim (Lazy & Eager)
│   │   ├── dsu.py                 # Disjoint Set Union (Path Compression + Rank)
│   │   ├── min_heap.py            # Min-Heap tự cài đặt
│   │   └── indexed_min_heap.py    # Indexed Min-Heap (hỗ trợ decrease_key)
│   └── generators/
│       └── dataset_generator.py   # Bộ sinh dữ liệu & khoảng cách Haversine / Euclid
├── data/
│   ├── reallife_data/
│   │   ├── hanoi_network.json     # Mạng lưới logistics 22 điểm tại Hà Nội
│   │   ├── hanoi_nodes.csv
│   │   └── hanoi_edges.csv
│   └── sample_small_10_nodes.json
├── docs/
│   └── md/
│       ├── presentation_guide.md  # Kịch bản thuyết trình & Mock Defense
│       ├── summary.md             # Tóm tắt lý thuyết toàn diện
│       ├── boruvka_algorithm.md   # Chuyên đề thuật toán Boruvka
│       ├── team_handbook.md       # Sổ tay phân công nhóm & RACIS matrix
│       └── data_format_spec.md    # Đặc tả định dạng dữ liệu JSON / CSV
└── tests/                         # Bộ Unit Test kiểm thử giải thuật
```

---

## 🚀 5. Khởi Chạy Nhanh

### Mở Slide Thuyết Trình:
Chỉ cần mở tệp `slides/index.html` trong trình duyệt web của bạn, hoặc chạy lệnh:
```powershell
start slides/index.html
```

### Chạy Kiểm Thử (Unit Tests):
```powershell
pip install -r requirements.txt
pytest
```
