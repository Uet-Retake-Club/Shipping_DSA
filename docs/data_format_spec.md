# ĐẶC TẢ CHUẨN ĐỊNH DẠNG DỮ LIỆU ĐỒ THỊ (DATA FORMAT SPECIFICATION)
> **Dự án:** Smart Delivery Network Design Using MST  
> **Áp dụng cho:** Tất cả các dataset thử nghiệm và mô hình đồ thị (`src/core/graph.py`)

---

## 1. MỤC TIÊU & NGUYÊN TẮC
Để toàn bộ các module (Graph Model, Kruskal, Prim, Visualization, Benchmark) tương thích hoàn hảo, cấu trúc dữ liệu đồ thị logistics được chuẩn hóa theo hai định dạng: **JSON** (khuyên dùng cho dữ liệu có metadata phong phú) và **CSV** (cho dữ liệu bảng đơn giản).

Mỗi mạng lưới gồm 2 thành phần chính:
1. **Nodes (Các điểm nút giao vận):** Đại diện cho Kho tổng (Hub), Kho trung chuyển khu vực (Warehouse), hoặc Điểm bưu cục / giao nhận (Delivery Point).
2. **Edges (Các tuyến đường kết nối khả dĩ):** Đại diện cho các tuyến đường tiềm năng có thể đầu tư/xây dựng, đi kèm chi phí hoặc độ dài kết nối.

---

## 2. ĐỊNH DẠNG JSON CHUẨN (`.json`)

File JSON bao gồm thông tin metadata của mạng lưới, danh sách đỉnh và danh sách cạnh.

```json
{
  "network_name": "HaNoi_Logistics_Cluster_Small",
  "description": "Mạng lưới logistics khu vực thử nghiệm 10 điểm",
  "coordinate_system": "2D_Cartesian", 
  "nodes": [
    {
      "id": "H1",
      "name": "Central Hub Long Bien",
      "type": "hub",
      "x": 50.0,
      "y": 50.0,
      "lat": 21.037,
      "lon": 105.890
    },
    {
      "id": "W1",
      "name": "Warehouse Cau Giay",
      "type": "warehouse",
      "x": 20.0,
      "y": 60.0,
      "lat": 21.033,
      "lon": 105.795
    },
    {
      "id": "D1",
      "name": "Delivery Point My Dinh",
      "type": "delivery_point",
      "x": 10.0,
      "y": 55.0,
      "lat": 21.028,
      "lon": 105.772
    }
  ],
  "edges": [
    {
      "u": "H1",
      "v": "W1",
      "weight": 31.62,
      "road_type": "highway",
      "status": "candidate"
    },
    {
      "u": "W1",
      "v": "D1",
      "weight": 11.18,
      "road_type": "urban",
      "status": "candidate"
    }
  ]
}
```

### Chi tiết các trường dữ liệu:
- **`nodes`**:
  - `id` *(string / int)*: Mã định danh duy nhất của điểm nút (bắt buộc).
  - `name` *(string)*: Tên hiển thị địa điểm.
  - `type` *(string)*: Loại nút (`hub`, `warehouse`, `delivery_point`).
  - `x`, `y` *(float)*: Tọa độ phẳng 2D (cho đồ thị hình học, tính khoảng cách Euclid).
  - `lat`, `lon` *(float, optional)*: Tọa độ GPS địa lý thực tế (cho tính khoảng cách Haversine và vẽ bản đồ Folium).
- **`edges`**:
  - `u`, `v` *(string / int)*: ID của 2 đỉnh đầu mút của tuyến đường (bắt buộc). Đồ thị là vô hướng nên `(u, v)` tương đương `(v, u)`.
  - `weight` *(float)*: Trọng số tuyến đường (chi phí xây dựng / bảo trì hoặc độ dài km) (bắt buộc, $> 0$).
  - `road_type` *(string, optional)*: Loại đường (`highway`, `arterial`, `urban`).

---

## 3. ĐỊNH DẠNG CSV CHUẨN (`.csv`)

Nếu dùng định dạng CSV, dữ liệu được phân tách làm 2 file tương ứng:

### `nodes.csv`
```csv
id,name,type,x,y,lat,lon
H1,Central Hub Long Bien,hub,50.0,50.0,21.037,105.890
W1,Warehouse Cau Giay,warehouse,20.0,60.0,21.033,105.795
D1,Delivery Point My Dinh,delivery_point,10.0,55.0,21.028,105.772
```

### `edges.csv`
```csv
u,v,weight,road_type
H1,W1,31.62,highway
W1,D1,11.18,urban
```

---

## 4. QUY ĐỊNH VỀ TÍNH TOÁN KHOẢNG CÁCH / TRỌNG SỐ TỰ ĐỘNG
Khi sinh đồ thị ngẫu nhiên hoặc khi file dữ liệu chỉ có danh sách tọa độ các đỉnh mà chưa có cạnh cụ thể:
1. **Khoảng cách Euclid 2D (Euclidean Distance):**
   $$d(A, B) = \sqrt{(x_B - x_A)^2 + (y_B - y_A)^2}$$
2. **Khoảng cách Haversine (tính độ cong bề mặt Trái Đất):**
   Dùng khi dữ liệu có `lat`, `lon` để tính khoảng cách thực tế tính bằng kilômét:
   $$a = \sin^2\left(\frac{\Delta \varphi}{2}\right) + \cos(\varphi_1)\cos(\varphi_2)\sin^2\left(\frac{\Delta \lambda}{2}\right)$$
   $$d = 2 R \cdot \arcsin(\sqrt{a}) \quad (R \approx 6371 \text{ km})$$
3. **Trọng số chi phí hạ tầng:**
   $$\text{Weight} = d(A, B) \times \text{Cost Factor}(\text{Road Type})$$
