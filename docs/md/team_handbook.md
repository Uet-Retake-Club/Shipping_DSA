# SỔ TAY NHÓM TRƯỞNG: SMART DELIVERY NETWORK (MST)
> **Dự án Môn học:** Cấu trúc Dữ liệu & Giải thuật (Data Structures & Algorithms)  
> **Quy mô nhóm:** 6 thành viên  
> **Chủ đề cốt lõi:** Thiết kế mạng lưới giao hàng thông minh bằng Cây bao trùm nhỏ nhất (Minimum Spanning Tree - Kruskal & Prim)

---

## 1. PHÂN CÔNG NHIỆM VỤ & MA TRẬN TRÁCH NHIỆM (RACIS MATRIX)

*Ký hiệu:*
- **R (Responsible):** Người trực tiếp thực hiện công việc chính.
- **A (Accountable):** Người chịu trách nhiệm cuối cùng về chất lượng/tiến độ.
- **C (Consulted):** Người được tham vấn ý kiến chuyên môn.
- **I (Informed):** Người được thông báo kết quả.
- **S (Support):** Người hỗ trợ kỹ thuật khi cần.

| Vai trò | Thành viên | Nhiệm vụ Cốt lõi (Core Tasks) | Sản phẩm Đầu ra (Deliverables) | Công cụ / Kỹ thuật | Tiêu chí Đánh giá |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Nhóm Trưởng / Điều Phối** | *TBD* | Tổ chức họp, quản lý Repo Git, lập tiến độ, làm việc với GV, tổng hợp slide & báo cáo. | Sổ tay tiến độ, Git Repo, Slide hoàn chỉnh, Kịch bản Demo. | GitHub, Trello/Jira, Notion, Google Docs | Đúng hạn, repo sạch, kết nối nhóm tốt. |
| **2. Nghiên Cứu Thuật Toán** | *TBD* | Nghiên cứu lý thuyết MST, chứng minh tính đúng đắn, so sánh Kruskal vs Prim, phân tích độ phức tạp, các trường hợp biên. | Chương Lý thuyết trong Báo cáo, bảng so sánh toán học, nội dung slide thuật toán. | LaTeX, Markdown, Tài liệu DSA | Hiểu sâu lý thuyết, giải thích rõ các case biên. |
| **3. Mô Hình Đồ Thị & Dữ Liệu** | *TBD* | Thiết kế Data Structure cho Graph (Adjacency List / Edge List), thu thập/tạo Dataset mẫu (thực tế & ngẫu nhiên). | Module `graph.py`, file dữ liệu JSON/CSV (mạng lưới kho hàng, chi phí/khoảng cách). | Python, Pandas, JSON, Random / Geo generator | Dữ liệu đa dạng (thưa/dày/không liên thông), cấu trúc linh hoạt. |
| **4. Lập Trình Backend (Kruskal)** | *TBD* | Tự cài đặt Union-Find (Disjoint Set Union - DSU) với Path Compression & Rank, cài đặt Kruskal, viết Unit Tests. | Module `kruskal.py`, `dsu.py`, file `test_kruskal.py`. | Python, PyTest | Tự cài đặt DSU (không dùng thư viện ngoài), chạy đúng, pass Unit tests. |
| **5. Lập Trình Backend (Prim)** | *TBD* | Tự cài đặt Priority Queue (Min-Heap), cài đặt thuật toán Prim, viết Unit Tests kiểm thử. | Module `prim.py`, `min_heap.py`, file `test_prim.py`. | Python, PyTest | Tự cài đặt Min-Heap, tối ưu $O(E \log V)$, pass Unit tests. |
| **6. Trực Quan Hóa & Báo Cáo** | *TBD* | Vẽ bản đồ/sơ đồ MST, đo đạc thời gian chạy (Benchmark), dựng biểu đồ hiệu năng, viết Báo cáo tổng kết. | Module `visualization.py`, Biểu đồ Benchmark, File Báo cáo cuối kỳ. | Matplotlib, NetworkX, Folium, Benchmark suite | Trực quan sinh động, biểu đồ so sánh rõ ràng, báo cáo chuẩn. |

---

## 2. KHUNG THEO DÕI TIẾN ĐỘ CHI TIẾT (6 TUẦN)

Nhóm trưởng sử dụng bảng Checkpoint dưới đây trong các buổi họp Weekly Sync (vào cuối mỗi tuần):

| Tuần | Mục Tiêu Cốt Lõi | Hạng Mục Công Việc Cần Check (Checklist) | Phụ Trách Chính |
| :--- | :--- | :--- | :--- |
| **Tuần 1** | **Kickoff & Setup** | - [x] Khởi tạo GitHub Repo, cấu trúc thư mục, quy định quy trình Git.<br>- [x] Chốt ngôn ngữ lập trình (Python 3.14) & công nghệ.<br>- [x] Thống nhất chuẩn format dữ liệu đồ thị đầu vào (JSON/CSV). | Nhóm trưởng (Toàn đội) |
| **Tuần 2** | **Data & Theoretical Basis** | - [ ] Hoàn thành module cấu trúc dữ liệu Đồ thị (`Graph` class).<br>- [ ] Tạo 3 dataset: Nhỏ (manual 10 đỉnh), Trung bình (50 đỉnh), Lớn (500+ đỉnh).<br>- [ ] Hoàn thành bản thảo phần Lý thuyết MST & Phân tích độ phức tạp. | Mô hình dữ liệu & NC Thuật toán |
| **Tuần 3** | **Backend Kruskal + DSU** | - [ ] Cài đặt xong DSU (Tối ưu Path Compression & Union by Rank).<br>- [ ] Cài đặt xong Kruskal, xử lý trường hợp đồ thị không liên thông (MST Forest).<br>- [ ] Viết và pass toàn bộ Unit Tests cho Kruskal. | Backend Kruskal |
| **Tuần 4** | **Backend Prim + Heap** | - [ ] Cài đặt Min-Heap / Priority Queue tự chế.<br>- [ ] Cài đặt xong Prim, tối ưu với Min-Heap.<br>- [ ] Pass Unit Tests Prim; So sánh kết quả tổng chi phí MST giữa Kruskal & Prim (phải bằng nhau). | Backend Prim |
| **Tuần 5** | **Visualization & Benchmark** | - [ ] Xây dựng module vẽ đồ thị trước/sau khi chạy MST (Matplotlib/Folium).<br>- [ ] Thực hiện Benchmark so sánh thời gian chạy Kruskal vs Prim trên các dạng đồ thị (thưa/dày).<br>- [ ] Hoàn thành 80% Báo cáo cuối kỳ. | Trực quan hóa & NC Thuật toán |
| **Tuần 6** | **Final Polish & Review** | - [ ] Hoàn thiện Báo cáo chính thức + Bộ Slide thuyết trình.<br>- [ ] Chạy thử nghiệm Demo tương tác (Live Demo).<br>- [ ] Tổ chức 1 buổi Họp Phản Biện Giả Định (Mock Defense) cho 6 thành viên. | Toàn bộ thành viên |

---

## 3. BỘ CÂU HỎI PHẢN BIỆN MẪU (MOCK DEFENSE QUESTIONS)

### 3.1. Nhóm Trưởng / Điều Phối (Project Lead)
- **Q1: Tại sao bài toán thiết kế mạng lưới giao hàng lại chọn MST mà không chọn Đường đi ngắn nhất (Dijkstra) hay TSP?**  
  *Gợi ý trả lời:* MST giải quyết bài toán Xây dựng/Duy trì hạ tầng kết nối toàn bộ các kho với tổng chi phí nhỏ nhất. Dijkstra tìm đường đi ngắn nhất giữa 2 điểm cụ thể (không tối ưu tổng hạ tầng). TSP là tìm chu trình cho 1 xe đi qua tất cả các điểm rồi về chỗ cũ (bài toán NP-hard). Định hướng MST đúng cho việc quy hoạch mạng lưới giao hàng cố định.
- **Q2: Nếu đồ thị đầu vào không liên thông (có các kho bị cô lập), chương trình của nhóm xử lý như thế nào?**  
  *Gợi ý trả lời:* Thuật toán Kruskal sẽ trả về một Rừng cây bao trùm (MST Forest) gồm nhiều cây MST nhỏ tương ứng với từng thành phần liên thông. Prim nếu bắt đầu từ 1 đỉnh sẽ chỉ duyệt trong thành phần liên thông đó. Chương trình cần đếm số thành phần liên thông và đưa ra cảnh báo mạng lưới bị chia cắt.

### 3.2. Thành viên Nghiên Cứu Thuật Toán (Algorithm Researcher)
- **Q1: Hãy chứng minh tính đúng đắn của Thuật toán Kruskal/Prim dựa trên Cut Property (Tính chất cắt)?**  
  *Gợi ý trả lời:* Cut Property phát biểu rằng: Với bất kỳ lát cắt (Cut) nào chia đồ thị thành 2 tập hợp đỉnh $S$ và $V \setminus S$, cạnh có trọng số nhỏ nhất băng qua lát cắt đó (crossing edge) luôn thuộc về ít nhất một MST. Cả Prim và Kruskal đều liên tục chọn các cạnh nhẹ nhất băng qua các lát cắt hợp lệ (Prim cắt giữa tập đỉnh đã duyệt và chưa duyệt; Kruskal cắt giữa 2 thành phần liên thông khác nhau), do đó luôn đảm bảo tính tối ưu toàn cục (Greedy Choice Property).
- **Q2: Khi nào nên chọn Kruskal và khi nào nên chọn Prim? Khi các cạnh có trọng số bằng nhau thì cây MST có duy nhất không?**  
  *Gợi ý trả lời:* Kruskal ($O(E \log E) \approx O(E \log V)$) hiệu quả hơn trên đồ thị thưa ($E \ll V^2$). Prim với Min-Heap ($O(E \log V)$) hoặc Fibonacci Heap ($O(E + V \log V)$) tốt hơn trên đồ thị dày/dày đặc ($E \approx V^2$). Nếu tất cả trọng số cạnh là duy nhất, cây MST là duy nhất. Nếu có các cạnh bằng trọng số, có thể có nhiều cây MST khác nhau nhưng tổng chi phí luôn bằng nhau.

### 3.3. Thành viên Mô Hình Đồ Thị & Dữ Liệu (Graph & Data Modeler)
- **Q1: Em biểu diễn đồ thị trong mã nguồn bằng cấu trúc dữ liệu nào? Dữ liệu thực tế được chuyển đổi ra sao?**  
  *Gợi ý trả lời:* Sử dụng Danh sách cạnh (Edge List) cho Kruskal và Danh sách kề (Adjacency List) cho Prim. Dữ liệu tọa độ GPS thực tế (Latitude, Longitude) được chuyển đổi thành khoảng cách Haversine hoặc khoảng cách Euclid 2D, sau đó nhân với đơn vị chi phí xây dựng/bảo trì để làm trọng số cạnh.
- **Q2: Làm thế nào để sinh dữ liệu thử nghiệm ngẫu nhiên đảm bảo tính thực tế của mạng lưới logistics?**  
  *Gợi ý trả lời:* Sinh tọa độ theo dạng cụm (cluster): một cụm trung tâm nội thành (mật độ dày) và các điểm ngoại thành (thưa). Khoảng cách giữa các điểm tuân theo bất đẳng thức tam giác hình học, phản ánh đúng đặc thù logistics thay vì sinh đồ thị ngẫu nhiên tùy tiện (Erdős–Rényi).

### 3.4. Lập Trình Backend Kruskal (Kruskal Engineer)
- **Q1: Cấu trúc dữ liệu Disjoint Set (Union-Find) giúp ích gì cho Kruskal và hai kỹ thuật tối ưu hóa cốt lõi của nó là gì?**  
  *Gợi ý trả lời:* DSU giúp kiểm tra cực nhanh xem 2 đỉnh có thuộc cùng một thành phần liên thông hay không (để tránh tạo chu trình khi nạp cạnh). Hai kỹ thuật tối ưu:
  1. *Path Compression (Nén đường đi):* Gộp các nút trên đường đi trực tiếp vào nút gốc khi gọi `find()`.
  2. *Union by Rank/Size (Hợp nhất theo hạng):* Luôn gắn cây thấp hơn vào gốc của cây cao hơn.  
  Độ phức tạp gộp là $O(\alpha(V))$ (hàm nghịch đảo Ackermann) - gần như hằng số $O(1)$.
- **Q2: Nếu không dùng DSU mà dùng BFS/DFS để kiểm tra chu trình trong Kruskal thì độ phức tạp sẽ thay đổi thế nào?**  
  *Gợi ý trả lời:* Mỗi lần kiểm tra một cạnh mới sẽ mất $O(V + E)$ bằng BFS/DFS. Với $E$ cạnh, tổng thời gian kiểm tra chu trình là $O(E \cdot (V + E)) = O(E^2)$, chậm hơn rất nhiều so với $O(E \log E)$ khi dùng DSU.

### 3.5. Lập Trình Backend Prim (Prim Engineer)
- **Q1: Thuật toán Prim hoạt động như thế nào và tại sao Min-Heap lại cần thiết ở đây?**  
  *Gợi ý trả lời:* Prim bắt đầu từ 1 đỉnh tùy ý, duy trì tập đỉnh đã thuộc MST. Ở mỗi bước, chọn cạnh nhỏ nhất nối từ tập đỉnh trong MST ra đỉnh ngoài MST. Min-Heap cho phép lấy ra cạnh nhỏ nhất đó trong thời gian $O(\log V)$ thay vì phải duyệt tuyến tính qua tất cả các cạnh lân cận mất $O(V)$.
- **Q2: Mảng visited hoặc in_mst đóng vai trò gì trong Prim? Nếu không có nó sẽ bị lỗi gì?**  
  *Gợi ý trả lời:* Mảng `visited` đánh dấu các đỉnh đã nạp vào cây bao trùm. Nếu không có mảng này, thuật toán sẽ liên tục lấy lại các cạnh nối giữa các đỉnh đã có trong MST, dẫn đến lặp vô tận hoặc tạo ra chu trình trong cây.

### 3.6. Trực Quan Hóa & Báo Cáo (Visualization & Report Lead)
- **Q1: Kết quả Benchmark so sánh Kruskal vs Prim của nhóm cho thấy điều gì trên các quy mô đồ thị khác nhau?**  
  *Gợi ý trả lời:* Trên đồ thị thưa ($E \approx V$), Kruskal thường chạy nhanh hơn hoặc tương đương Prim vì việc sắp xếp số lượng ít cạnh diễn ra rất nhanh. Trên đồ thị dày ($E \approx V^2$), Prim sử dụng Min-Heap thể hiện sự vượt trội rõ rệt vì chi phí sắp xếp $E$ cạnh trong Kruskal tăng vọt.
- **Q2: Hình ảnh trực quan hóa hỗ trợ gì cho việc nghiệm thu mô hình logistics thực tế?**  
  *Gợi ý trả lời:* Trực quan hóa giúp nhà quản trị nhìn rõ tuyến đường trục (backbone network) nào được chọn để đầu tư, loại bỏ các kết nối thừa thãi, và phát hiện trực quan các đoạn ngắt kết nối trong mạng lưới.

---

## 4. BÀI TẬP THỰC HÀNH TƯƠNG ỨNG TRÊN LEETCODE & HACKERRANK

| STT | Tên bài toán | Nền tảng & Độ khó | Vai trò phù hợp | Ý nghĩa rèn luyện & Áp dụng dự án |
| :---: | :--- | :--- | :--- | :--- |
| 1 | **Connecting Cities With Minimum Cost** | LeetCode 1135 / LintCode 3670 (Medium) | Backend Kruskal & Mô hình Đồ thị | Bài toán chuẩn mực cho Kruskal + DSU. Trả về `-1` khi đồ thị không liên thông. |
| 2 | **Min Cost to Connect All Points** | LeetCode 1584 (Medium) | Backend Prim & NC Thuật toán | Đồ thị đầy đủ 2D ($E = V(V-1)/2$). Prim với Priority Queue thể hiện ưu thế vượt trội. |
| 3 | **Prim's MST Special Subtree** | HackerRank (Medium) | Backend Prim | Cài đặt chuẩn thuật toán Prim từ 1 đỉnh xuất phát với Min-Heap. |
| 4 | **Kruskal (MST): Really Special Subtree** | HackerRank (Medium) | Backend Kruskal | Rèn luyện kỹ năng xử lý tie-breaking (các cạnh bằng trọng số) và tối ưu DSU. |
| 5 | **Redundant Connection** | LeetCode 684 (Medium) | Backend Kruskal & Nhóm trưởng | Phát hiện cạnh tạo chu trình đầu tiên bằng DSU. |
| 6 | **Optimize Water Distribution in a Village** | LeetCode 1168 (Hard) | NC Thuật toán & Trực quan hóa | Biến đổi bài toán MST bằng kỹ thuật "Đỉnh ảo" (Virtual Node 0) – Điểm cộng sáng tạo cho báo cáo! |

---

## 5. KỊCH BẢN MOCK DEFENSE (TUẦN 6)

1. **Bước 1 (5 phút): Chạy Live Demo:** Trực quan hóa nhập file CSV/JSON, chạy Kruskal/Prim và hiển thị bản đồ mạng lưới MST sinh ra.
2. **Bước 2 (10 phút): Thuyết trình Slide:** Trình bày từ Đặt vấn đề $\to$ Mô hình hóa $\to$ Thiết kế thuật toán $\to$ Kết quả Benchmark $\to$ Đánh giá.
3. **Bước 3 (10 phút): Vấn đáp phản biện:** Nhóm trưởng hỏi ngẫu nhiên câu hỏi trong Mục 3 cho từng thành viên, đảm bảo tất cả đều nắm chắc cơ chế hoạt động.
