# CƠ SỞ LÝ THUYẾT VỀ CÂY BAO TRÙM NHỎ NHẤT (MST) & BÀI TOÁN MẠNG LƯỚI GIAO VẬN
> **Dự án:** Smart Delivery Network Design Using MST  
> **Tài liệu phục vụ:** Báo cáo cuối kỳ, Slide thuyết trình và Phản biện kỹ thuật

---

## 1. ĐẶT VẤN ĐỀ LOGISTICS & TẠI SAO LẠI DÙNG MST?

Trong logistics và chuỗi cung ứng, các doanh nghiệp thường đối mặt với bài toán **Quy hoạch Hạ tầng Mạng lưới (Network Infrastructure Design)**:
- Làm thế nào để xây dựng hoặc ký hợp đồng duy trì một tập hợp các tuyến đường kết nối giữa tất cả các trung tâm điều phối (Hub), kho hàng (Warehouse) và bưu cục (Delivery Points) sao cho:
  1. Mọi điểm đều có thể vận chuyển hàng hóa tới nhau (mạng lưới hoàn toàn liên thông).
  2. Tổng chi phí đầu tư hoặc bảo trì hạ tầng là **nhỏ nhất**.
  3. Không có tuyến đường dư thừa tạo chu trình (tránh lãng phí ngân sách cố định).

### Phân biệt rõ MST với Dijkstra và TSP:
- **MST (Minimum Spanning Tree):** Tối ưu hóa **tổng chi phí toàn mạng lưới**. Giúp doanh nghiệp quyết định chọn tuyến đường nào để xây dựng/đầu tư.
- **Shortest Path (Dijkstra):** Tối ưu chi phí/thời gian giữa **2 điểm cụ thể**.
- **Traveling Salesman Problem (TSP):** Tìm hành trình đi tuần tự qua tất cả các điểm rồi quay về điểm xuất phát cho **1 xe chở hàng** (bài toán NP-hard).

Do đó, mô hình MST là giải pháp tối ưu toán học hoàn hảo cho bài toán thiết kế mạng lưới cốt lõi (backbone network).

---

## 2. ĐỊNH NGHĨA TOÁN HỌC & TÍNH CHẤT CẮT (CUT PROPERTY)

### 2.1. Định nghĩa Cây bao trùm nhỏ nhất
Cho đồ thị vô hướng, liên thông có trọng số $G = (V, E, w)$, trong đó $V$ là tập đỉnh, $E$ là tập cạnh, và $w: E \to \mathbb{R}^+$ là hàm trọng số.
Cây bao trùm nhỏ nhất (MST) là một đồ thị con $T = (V, E_T)$ thỏa mãn:
1. $T$ là một cây (liên thông, không có chu trình, gồm đúng $|V| - 1$ cạnh).
2. Tổng trọng số các cạnh là nhỏ nhất:
   $$w(T) = \sum_{e \in E_T} w(e) \quad \text{đạt giá trị nhỏ nhất}.$$

### 2.2. Tính chất cắt (Cut Property) và Chứng minh tính đúng đắn
- **Khái niệm Lát cắt (Cut):** Một lát cắt $(S, V \setminus S)$ là một phép phân chia tập đỉnh $V$ thành hai tập hợp con rời nhau.
- **Cạnh băng qua lát cắt (Crossing Edge):** Một cạnh $e = (u, v)$ được gọi là băng qua lát cắt $(S, V \setminus S)$ nếu $u \in S$ và $v \in V \setminus S$.
- **Định lý (Cut Property):**  
  > *Với bất kỳ lát cắt nào $(S, V \setminus S)$ trong đồ thị, cạnh băng qua lát cắt có trọng số nhỏ nhất (lightest crossing edge) luôn thuộc về ít nhất một cây bao trùm nhỏ nhất (MST).*

**Chứng minh bằng phản chứng (Exchange Argument):**
1. Giả sử tồn tại một MST $T$ không chứa cạnh nhẹ nhất $e = (u, v)$ băng qua lát cắt $(S, V \setminus S)$.
2. Vì $T$ là cây bao trùm nối toàn bộ các đỉnh, tồn tại một đường đi duy nhất trong $T$ nối $u$ và $v$. Đường đi này bắt đầu tại $u \in S$ và kết thúc tại $v \in V \setminus S$, do đó chắc chắn phải chứa ít nhất một cạnh khác $e' = (u', v')$ cũng băng qua lát cắt $(S, V \setminus S)$.
3. Nếu ta thêm cạnh $e$ vào $T$, ta tạo thành một chu trình đơn. Nếu ta loại bỏ cạnh $e'$ khỏi chu trình đó, ta thu được một cây bao trùm mới $T' = T \cup \{e\} \setminus \{e'\}$.
4. Tổng trọng số của cây mới:
   $$w(T') = w(T) - w(e') + w(e)$$
5. Do $e$ là cạnh nhẹ nhất băng qua lát cắt nên $w(e) \le w(e')$. Từ đó suy ra $w(T') \le w(T)$.
6. Vì $T$ đã là MST (tổng trọng số tối thiểu), ta bắt buộc phải có $w(T') = w(T)$, chứng tỏ $T'$ cũng là một MST chứa cạnh $e$. Như vậy cạnh $e$ luôn an toàn để chọn vào MST. $\blacksquare$

---

## 3. SO SÁNH THUẬT TOÁN: KRUSKAL VS PRIM

| Tiêu chí | Thuật toán Kruskal | Thuật toán Prim |
| :--- | :--- | :--- |
| **Triết lý thiết kế** | Tham lam theo **Cạnh** (Edge-based Greedy) | Tham lam theo **Đỉnh** (Vertex-based Greedy) |
| **Cấu trúc dữ liệu chính** | Mảng cạnh sắp xếp + **Disjoint Set Union (DSU)** | Danh sách kề + **Min-Heap (Priority Queue)** |
| **Độ phức tạp thời gian** | $O(E \log E) = O(E \log V)$ | $O(E \log V)$ (với Min-Heap) hoặc $O(E + V \log V)$ (Fibonacci Heap) |
| **Độ phức tạp không gian** | $O(V + E)$ (để lưu mảng DSU và danh sách cạnh) | $O(V + E)$ (để lưu đồ thị kề, visited array, và Heap) |
| **Hiệu năng trên Đồ thị thưa** ($E \ll V^2$) | **Cực nhanh và tối ưu**. Sắp xếp số lượng ít cạnh tốn rất ít thời gian. | Tương đương, nhưng có phụ phí quản lý Heap. |
| **Hiệu năng trên Đồ thị dày** ($E \approx V^2$) | Kém hơn do chi phí sắp xếp $O(V^2 \log(V^2)) = O(V^2 \log V)$ rất lớn. | **Rất vượt trội**, đặc biệt khi tối ưu bằng Decrease-Key hoặc mảng trực tiếp. |
| **Trạng thái trung gian** | Một **Rừng cây (Forest)** gồm các cụm rời nhau được ghép dần. | Một **Cây con duy nhất liên tục mở rộng** từ đỉnh ban đầu. |

---

## 4. CÁC TRƯỜNG HỢP BIÊN QUAN TRỌNG (EDGE CASES)

### 4.1. Đồ thị không liên thông (Disconnected Graph)
- Nếu mạng lưới bị ngắt thành nhiều cụm tách biệt (ví dụ: các kho hàng ở hải đảo hoặc vùng chia cắt không có đường nối):
  - **Kruskal:** Tự nhiên tìm ra một **Rừng cây bao trùm (MST Forest)** với $k$ cây con tương ứng với $k$ thành phần liên thông, tổng số cạnh nạp vào là $|V| - k$.
  - **Prim:** Nếu chỉ bắt đầu từ 1 đỉnh, Prim chỉ duyệt được các đỉnh trong thành phần liên thông chứa đỉnh đó. Cần lặp Prim qua các đỉnh chưa duyệt để tìm đủ rừng cây bao trùm.
  - **Quy chuẩn của dự án:** Module phải đếm số thành phần liên thông và đưa ra thông báo cảnh báo rõ ràng.

### 4.2. Cạnh có trọng số bằng nhau (Ties in Weight)
- Nếu đồ thị có nhiều cạnh cùng chi phí:
  - Có thể tồn tại **nhiều cây MST khác nhau** về mặt hình học/danh sách cạnh.
  - **Tuy nhiên, tổng chi phí nhỏ nhất luôn luôn bằng nhau và duy nhất.**
  - Dự án thiết lập cơ chế tie-breaking nhất quán (ưu tiên theo ID đỉnh) để đảm bảo tính tái lập (deterministic).

### 4.3. Kỹ thuật "Đỉnh ảo" (Virtual Node 0)
- Một bài toán nâng cao kinh điển trong logistics (tương tự bài LeetCode 1168):
  - Một kho hàng có thể được cấp phát độc lập bằng cách xây trạm phát điện/nước tại chỗ (chi phí $C_i$) hoặc nối đường dây từ trạm khác (chi phí $R_{ij}$).
  - Ta có thể mô hình hóa bằng cách thêm một **Đỉnh nguồn ảo (Virtual Node 0)**, với cạnh nối từ $0$ tới kho $i$ có trọng số $C_i$. Chạy MST trên đồ thị mở rộng này sẽ giải quyết đồng thời bài toán "tự xây tại chỗ" hay "kết nối chia sẻ".
