# HƯỚNG DẪN THUYẾT TRÌNH TOÀN DIỆN (PRESENTATION & DEFENSE MASTER GUIDE)
> **Đề tài:** Smart Delivery Network Design Using Minimum Spanning Tree (MST)  
> **Môn học:** Cấu trúc Dữ liệu & Giải thuật (Data Structures & Algorithms - DSA)  
> **Ngôn ngữ triển khai:** Python 3 (Tự cài đặt DSU, Min-Heap, IndexedMinHeap - Không dùng thư viện ngoài cho cấu trúc cốt lõi)  
> **Thời lượng đề xuất:** 12 - 15 phút Thuyết trình + 5 phút Vấn đáp Phản biện (Q&A)

---

## 1. TỔNG QUAN CHIẾN LƯỢC THUYẾT TRÌNH (STRATEGY & HOOK)

### 1.1. Thông điệp cốt lõi (Core Thesis)
> *"Trong bài toán logistics hiện đại, chi phí đầu tư và duy trì hạ tầng kết nối giữa các kho bãi chiếm hàng triệu USD. Bằng cách mô hình hóa hệ thống vận chuyển thành đồ thị có trọng số và áp dụng các biến thể tối ưu của Cây bao trùm nhỏ nhất (MST), chúng tôi chứng minh cách giảm thiểu tối đa chi phí hạ tầng mạng lưới nhưng vẫn đảm bảo 100% các điểm giao vận được liên thông hoàn hảo."*

### 1.2. Ba điểm "ăn điểm tuyệt đối" trước Giảng viên / Hội đồng
1. **Tự cài đặt thuật toán & Cấu trúc dữ liệu nâng cao:** Không chỉ gọi hàm có sẵn, nhóm tự cài đặt từ đầu:
   - `DSU` (Disjoint Set Union) với **Path Compression** và **Union by Rank** đạt độ phức tạp $O(\alpha(V))$.
   - `MinHeap` và `IndexedMinHeap` hỗ trợ thao tác cập nhật độ ưu tiên `decrease_key` cho thuật toán Eager Prim.
2. **So sánh đa thuật toán hoàn chỉnh:** Đối chiếu toàn diện giữa **Borůvka (1926)**, **Kruskal (1956)** và **Prim (1957)** trên cả 2 góc độ: lý thuyết toán học (Cut Property / Cycle Property) và thực nghiệm (đồ thị thưa vs dày).
3. **Bài toán thực tế (Real-world Case Study):** Ứng dụng trực tiếp trên tập dữ liệu mạng lưới giao vận thực tế tại Hà Nội (**Hanoi Metropolitan Logistics Network** - 22 nút: 3 Mega Hubs, 9 Warehouses, 10 Delivery Stations) với tọa độ GPS thực tế và công thức khoảng cách mặt cầu **Haversine**.

---

## 2. PHÂN BỔ THỜI LƯỢNG & KỊCH BẢN CHI TIẾT (12 - 15 PHÚT)

| Phần | Nội dung | Thời lượng | Người trình bày gợi ý |
| :--- | :--- | :---: | :--- |
| **Phần 1** | Giới thiệu & Đặt vấn đề Logistics (Problem Statement) | 2 phút | Thành viên 1 (Nhóm trưởng / Điều phối) |
| **Phần 2** | Mô hình hóa Đồ thị & Cơ sở Toán học (Cut/Cycle Property) | 2.5 phút | Thành viên 2 (Mô hình dữ liệu & NC Thuật toán) |
| **Phần 3** | Đi sâu 3 Thuật toán: Borůvka, Kruskal + DSU, Prim + Heap | 4.5 phút | Thành viên 3 & 4 (Backend Kruskal & Prim) |
| **Phần 4** | Đánh giá so sánh, Benchmark & Case Study Hà Nội | 3 phút | Thành viên 5 (Trực quan hóa & Benchmark) |
| **Phần 5** | Tổng kết, Giới hạn mô hình & Hướng phát triển | 1 phút | Toàn đội / Nhóm trưởng |
| **Phần 6** | Live Demo tương tác & Vấn đáp (Mock Defense Q&A) | 5 phút | Toàn đội |

---

## 3. LỜI THOẠI CHI TIẾT TỪNG SLIDE (SPEAKER NOTES & SCRIPT)

### Slide 1: Trang bìa (Title & Team Intro)
- **Lời dẫn:**  
  *"Kính chào Thầy/Cô và các bạn. Hôm nay, nhóm chúng em xin được đại diện trình bày đề tài môn Cấu trúc dữ liệu & Giải thuật với chủ đề: **Thiết kế mạng lưới giao vận thông minh sử dụng Cây bao trùm nhỏ nhất (Smart Delivery Network Design Using MST)**. Dự án tập trung vào việc mô hình hóa bài toán tối ưu chi phí hạ tầng giao vận, tự thiết kế các cấu trúc dữ liệu cốt lõi và kiểm chứng trên dữ liệu mạng lưới bưu chính thực tế tại Hà Nội."*

---

### Slide 2: Đặt vấn đề thực tế (Problem Statement & Motivation)
- **Điểm nhấn:** Phân biệt rõ bài toán **Hạ tầng kết nối (Backbone Network)** khác với bài toán **Định tuyến xe (Vehicle Routing / TSP)**.
- **Lời dẫn:**  
  *"Trong ngành vận chuyển và chuỗi cung ứng, một doanh nghiệp sở hữu hàng chục kho tổng, kho trung chuyển và hàng trăm bưu cục. Để kết nối các điểm này, họ có thể thuê hoặc xây dựng các tuyến đường vận tải độc quyền, hạ tầng cáp quang quản lý nội bộ.  
  Nếu nối tất cả các cặp kho lại với nhau (Full Mesh), chi phí sẽ bùng nổ theo cấp số nhân $O(V^2)$. Ngược lại, nếu chọn sai các tuyến nối, mạng lưới có thể bị chia cắt hoặc chi phí vận hành bị đội lên quá cao.  
  Câu hỏi đặt ra là: **Làm thế nào để chọn ra một tập hợp các tuyến đường tối thiểu, sao cho từ bất kỳ kho nào cũng có thể gửi hàng tới các kho khác, mà tổng chi phí xây dựng là NHỎ NHẤT?** Đây chính là định nghĩa chuẩn mực của bài toán **Minimum Spanning Tree (MST)**."*

---

### Slide 3: Mô hình hóa Đồ thị & Xử lý Dữ liệu Thực tế (Graph Modeling & Data)
- **Điểm nhấn:** Đồ thị vô hướng có trọng số $G = (V, E)$, tính toán khoảng cách Haversine.
- **Lời dẫn:**  
  *"Chúng em mô hình hóa mạng lưới thành đồ thị vô hướng có trọng số $G = (V, E)$:  
  - **Tập đỉnh $V$:** Đại diện cho 3 cấp độ bưu cục: Mega Hub (Kho tổng), Regional Warehouse (Kho trung chuyển) và Delivery Point (Bưu cục phát).  
  - **Tập cạnh $E$:** Tuyến đường giao thông khả dĩ giữa hai nút.  
  - **Trọng số cạnh $w(u, v)$:** Kết hợp giữa khoảng cách địa lý và hệ số cấp đường (đường cao tốc, quốc lộ, đường nội đô).  
  Đặc biệt, để xử lý tọa độ GPS thực tế (Latitude, Longitude), nhóm đã cài đặt công thức mặt cầu **Haversine** nhằm tính toán chính xác độ cong Trái Đất, loại bỏ sai số lớn của khoảng cách Euclid phẳng khi áp dụng trên quy mô liên tỉnh."*

---

### Slide 4: Cơ sở Toán học & Tính chất Cắt (Theoretical Basis & Cut Property)
- **Điểm nhấn:** Tính chất Cắt (Cut Property) và Tính chất Chu trình (Cycle Property).
- **Lời dẫn:**  
  *"Cả ba thuật toán tìm MST mà nhóm nghiên cứu đều hoạt động theo chiến lược **Tham lam (Greedy Strategy)**. Tính đúng đắn của chúng được bảo đảm bởi hai định lý nền tảng:  
  1. **Tính chất lát cắt (Cut Property):** Với bất kỳ một lát cắt $(S, V \setminus S)$ nào chia đồ thị thành 2 phần rời rạc, cạnh có trọng số nhỏ nhất băng qua lát cắt đó luôn thuộc về mọi cây bao trùm nhỏ nhất.  
  2. **Tính chất chu trình (Cycle Property):** Trong một chu trình bất kỳ, cạnh có trọng số lớn nhất tuyệt đối sẽ không bao giờ xuất hiện trong bất kỳ cây MST nào.  
  Các thuật toán Kruskal, Prim và Borůvka thực chất chỉ là những cách thức khác nhau để tận dụng hai tính chất này nhằm liên tục đưa các cạnh tối ưu vào cây khung."*

---

### Slide 5: Thuật toán Tiền nhiệm Borůvka (1926) & Sức mạnh Song song hóa
- **Điểm nhấn:** Thuật toán MST đầu tiên trong lịch sử, co cụm song song từng vòng.
- **Lời dẫn:**  
  *"Thuật toán tìm MST đầu tiên trong lịch sử không phải là Kruskal hay Prim, mà là **Borůvka (1926)**, ra đời để thiết kế lưới điện vùng Moravia.  
  Ý tưởng của Borůvka rất độc đáo: Thuật toán hoạt động theo từng vòng (Round). Ban đầu mỗi đỉnh là 1 thành phần riêng biệt. Ở mỗi vòng, **đồng thời tất cả các thành phần** đều tìm cạnh nhẹ nhất nối ra ngoài và gộp lại.  
  Sau mỗi vòng, số lượng thành phần giảm ít nhất 50%, nên thuật toán chỉ cần tối đa $\lceil \log_2 V \rceil$ vòng lặp. Điểm đặc sắc nhất của Borůvka là tính chất **song song hóa tự nhiên**, mỗi cụm có thể tính toán độc lập mà không cần đồng bộ tuần tự như Prim hay Kruskal."*

---

### Slide 6: Thuật toán Kruskal & Tối ưu hóa DSU (Path Compression + Union by Rank)
- **Điểm nhấn:** Tự cài đặt DSU từ đầu, giải thích hàm Ackermann nghịch đảo $\alpha(V)$.
- **Lời dẫn:**  
  *"Thuật toán Kruskal tiếp cận theo hướng tiếp cận từng cạnh: Sắp xếp toàn bộ $E$ cạnh theo trọng số tăng dần, sau đó lần lượt xét từng cạnh và kết nạp nếu nó không tạo chu trình.  
  Thách thức lớn nhất của Kruskal là: **Làm sao kiểm tra 2 đỉnh có thuộc cùng chu trình hay không trong thời gian nhanh nhất?**  
  Nếu dùng BFS/DFS, ta mất $O(V)$, khiến Kruskal chậm tới $O(E \cdot V)$. Để giải quyết triệt để, nhóm đã **tự cài đặt cấu trúc Disjoint Set Union (DSU)** với 2 kỹ thuật tối ưu hóa kinh điển:  
  1. **Path Compression (Nén đường đi):** Nối thẳng các đỉnh trên đường đi về nút gốc.  
  2. **Union by Rank (Gộp theo hạng):** Luôn gắn cây có độ cao nhỏ hơn vào cây có độ cao lớn hơn.  
  Nhờ đó, mỗi thao tác kiểm tra chu trình chỉ tốn $O(\alpha(V))$ - hàm Ackermann nghịch đảo, với mọi đồ thị thực tế $\alpha(V) \le 4$, tương đương thời gian thực thi hằng số $O(1)$. Tổng độ phức tạp của Kruskal chỉ còn $O(E \log E)$ cho bước sắp xếp."*

---

### Slide 7: Thuật toán Prim & Min-Heap (Lazy vs Eager Prim)
- **Điểm nhấn:** Phát triển cây liên tục từ 1 đỉnh, tối ưu từ $O(V^2)$ xuống $O(E \log V)$ bằng IndexedMinHeap.
- **Lời dẫn:**  
  *"Khác với Kruskal chọn cạnh rải rác, thuật toán **Prim** bắt đầu từ một đỉnh gốc và nuôi lớn một cây liên thông duy nhất. Ở mỗi bước, Prim chọn đỉnh gần nhất bên ngoài để kéo vào cây.  
  Nhóm chúng em đã triển khai cả hai phiên bản:  
  1. **Lazy Prim:** Sử dụng `MinHeap` tự cài đặt để lưu toàn bộ các cạnh kề. Cạnh cũ không hợp lệ sẽ bị bỏ qua khi lấy ra. Bộ nhớ là $O(E)$.  
  2. **Eager Prim:** Sử dụng cấu trúc **IndexedMinHeap** (Heap có chỉ mục hỗ trợ `decrease_key`). Ta chỉ lưu đúng khoảng cách ngắn nhất của mỗi đỉnh tới cây MST, giúp giảm thiểu không gian bộ nhớ chỉ còn đúng $O(V)$ và thời gian $O(E \log V)$.  
  Đặc điểm của Prim là đồ thị luôn liên thông tại mọi bước trung gian, rất thuận lợi cho việc thi công hạ tầng cuốn chiếu."*

---

### Slide 8: Bảng Ma trận So sánh Toàn diện (Comparison Matrix)
- **Điểm nhấn:** Hướng dẫn khi nào chọn thuật toán nào.
- **Lời dẫn:**  
  *"Dựa trên phân tích toán học và thực nghiệm, nhóm tổng kết bảng tiêu chí lựa chọn:  
  - Trên **Đồ thị thưa ($E \approx V$):** Kruskal là sự lựa chọn vượt trội vì số lượng cạnh ít, bước sắp xếp chạy cực nhanh và cấu trúc DSU rất nhẹ.  
  - Trên **Đồ thị dày ($E \approx V^2$):** Eager Prim thể hiện ưu thế áp đảo vì không phải tốn chi phí sắp xếp $O(V^2)$ cạnh.  
  - Khi cần **Tính toán phân tán / GPU:** Borůvka là ứng cử viên hàng đầu nhờ khả năng gộp song song giữa các cụm độc lập."*

---

### Slide 9: Demo Trực quan hóa Tương tác (Interactive Live Simulation)
- **Điểm nhấn:** Minh họa trực tiếp trên Slide các bước kết nạp cạnh của Kruskal và Prim.
- **Lời dẫn:**  
  *(Người thuyết trình bấm nút Next Step trên widget mô phỏng):*  
  *"Tại đây, Thầy/Cô có thể thấy trực quan cách thuật toán Kruskal duyệt danh sách cạnh: Cạnh nhẹ nhất nối Cầu Giấy và Đống Đa được chọn đầu tiên. Khi duyệt đến cạnh tạo thành chu trình tam giác giữa 3 nút đã liên thông, DSU phát hiện cùng gốc `find(u) == find(v)` và lập tức loại bỏ. Tổng trọng số và số cạnh $V-1$ được cập nhật thời gian thực."*

---

### Slide 10: Thực nghiệm trên Mạng lưới Hà Nội (Hanoi Case Study)
- **Điểm nhấn:** 22 nút, so sánh mạng lưới ban đầu vs mạng lưới sau khi tối ưu MST.
- **Lời dẫn:**  
  *"Áp dụng vào thực tế mạng lưới bưu chính Hà Nội gồm 22 điểm nút (3 Hub lớn: Long Biên, Bắc Từ Liêm, Quang Minh):  
  - Ban đầu, mạng lưới dự thảo gồm 30 tuyến liên kết có tổng chi phí xây dựng và bảo trì định kỳ là **184.2 đơn vị chi phí**.  
  - Sau khi áp dụng thuật toán MST, hệ thống đã loại bỏ 9 tuyến đường dư thừa, chỉ giữ lại đúng 21 tuyến trục huyết mạch kết nối toàn diện 22 nút với tổng chi phí giảm xuống chỉ còn **118.6 đơn vị chi phí** (tiết kiệm hơn 35.6% ngân sách đầu tư ban đầu mà vẫn đảm bảo hàng hóa luân chuyển được tới mọi trạm)."*

---

### Slide 11: Đánh giá Giới hạn & Ứng dụng Thực tế Mở rộng
- **Điểm nhấn:** Tư duy phản biện kỹ thuật: MST có rủi ro gì?
- **Lời dẫn:**  
  *"Để có cái nhìn đa chiều, nhóm cũng đã phân tích các hạn chế của cây khung MST trong thực tế:  
  1. **Điểm lỗi đơn lẻ (Single Point of Failure):** Vì là cây, nên nếu một tuyến đường trục bị sạt lở hoặc tắc nghẽn, mạng lưới sẽ bị đứt gãy làm 2 nửa. Giải pháp thực tế là bổ sung thêm một số cạnh dự phòng (2-Edge Connected Network / Ring Topology).  
  2. **Đường đi giữa 2 nút có thể bị dài (Hop count):** MST tối ưu tổng chi phí toàn mạng lưới, nhưng đường đi giữa hai điểm cụ thể có thể phải đi vòng qua nhiều trạm trung gian.  
  Do đó, trong kiến trúc hạ tầng logistics hoàn chỉnh, MST đóng vai trò làm **Mạng lưới kết nối xương sống (Backbone Network)**, sau đó kết hợp thêm các tuyến đường tắt trọng điểm."*

---

### Slide 12: Tổng kết & Hỏi đáp (Conclusion & Mock Defense Ready)
- **Lời dẫn:**  
  *"Tóm lại, dự án đã hoàn thành trọn vẹn mục tiêu: từ nghiên cứu lý thuyết, tự cài đặt cấu trúc dữ liệu nâng cao DSU & Min-Heap, cho tới kiểm thử và ứng dụng thực tiễn trên mạng lưới giao vận. Nhóm chúng em xin chân thành cảm ơn Thầy/Cô đã lắng nghe và rất mong nhận được câu hỏi góp ý!"*

---

## 4. BỘ CÂU HỎI VẤN ĐÁP PHẢN BIỆN CHUYÊN SÂU (MOCK DEFENSE Q&A)

### Câu 1 (Rất hay hỏi): Tại sao chọn bài toán MST cho giao vận mà không chọn Dijkstra hay TSP?
- **Trả lời ngắn gọn & chuẩn xác:**  
  - **MST:** Tối ưu hóa chi phí **XÂY DỰNG / DUY TRÌ HẠ TẦNG** cố định kết nối toàn bộ hệ thống các trạm với nhau (Tổng chi phí toàn bộ các cạnh nhỏ nhất).  
  - **Dijkstra:** Tối ưu hóa hành trình **ĐI TỪ ĐIỂM A ĐẾN ĐIỂM B** cho một bưu phẩm cụ thể (Đường đi ngắn nhất giữa 2 đỉnh).  
  - **TSP (Travelling Salesperson Problem):** Tối ưu hóa **LỘ TRÌNH CHO 1 XE ĐI GIAO HÀNG** qua tất cả các điểm rồi quay về điểm xuất phát (Tìm chu trình Hamilton có trọng số nhỏ nhất - bài toán NP-hard).  
  $\Rightarrow$ MST giải quyết bài toán quy hoạch mạng lưới cấp độ hạ tầng, là tiền đề để chạy Dijkstra và gom đơn giao hàng.

---

### Câu 2: Thuật toán có chạy đúng nếu trọng số cạnh có giá trị âm không?
- **Trả lời:**  
  **Có, cả Kruskal, Prim và Borůvka đều chạy HOÀN TOÀN ĐÚNG với cạnh có trọng số âm!**  
  *Giải thích toán học:* Tính chất lát cắt (Cut Property) và tính chất chu trình (Cycle Property) không hề phụ thuộc vào dấu của trọng số cạnh. Chúng chỉ so sánh thứ tự hơn kém giữa các trọng số ($w_e < w_{e'}$). Khác với Dijkstra (sẽ sai khi có cạnh âm do cập nhật tích lũy đường đi $D_u + w$), các thuật toán MST chỉ xét trọng số trực tiếp của cạnh kết nạp, do đó cạnh âm càng được ưu tiên chọn trước vì nó làm giảm tổng trọng số của cây.

---

### Câu 3: Nếu đồ thị đầu vào không liên thông thì thuật toán xử lý thế nào?
- **Trả lời:**  
  - **Kruskal:** Vẫn duyệt hết các cạnh và tự động trả về một **Rừng cây bao trùm nhỏ nhất (Minimum Spanning Forest - MSF)**. Số cạnh thu được sẽ là $V - C$ (với $C$ là số thành phần liên thông).  
  - **Prim:** Nếu chỉ chạy từ một đỉnh `start`, Prim chỉ thăm được thành phần liên thông chứa đỉnh đó. Để xử lý đồ thị không liên thông, chương trình của nhóm bọc một vòng lặp ngoài: quét qua các đỉnh chưa được `visited` và khởi động lại Prim, từ đó thu được toàn bộ rừng MSF.

---

### Câu 4: Khi nào cây MST là duy nhất? Nếu có các cạnh bằng trọng số thì sao?
- **Trả lời:**  
  - **Tính duy nhất:** Nếu tất cả các cạnh trong đồ thị có trọng số đôi một khác nhau, thì cây MST chắc chắn là **DUY NHẤT**.  
  - **Khi có cạnh trùng trọng số:** Có thể tồn tại nhiều cây MST khác nhau (tùy thuộc vào thứ tự sắp xếp tie-breaking của Kruskal hoặc thứ tự nạp vào Heap của Prim). Tuy nhiên, **TỔNG TRỌNG SỐ CỦA CÂY KHUNG NHỎ NHẤT LUÔN LUÔN BẰNG NHAU** và đều đạt giá trị tối ưu toàn cục.

---

### Câu 5: Tại sao độ phức tạp của DSU lại là $\alpha(V)$ và $\alpha$ là hàm gì?
- **Trả lời:**  
  $\alpha(n)$ là **hàm nghịch đảo của hàm Ackermann** ($A(n, n)$) - một hàm tăng trưởng cực kỳ khủng khiếp trong toán học. Trong khi $A(4, 4)$ lớn hơn cả số nguyên tử trong vũ trụ quan sát được, thì hàm nghịch đảo $\alpha(n) \le 4$ với mọi giá trị $n$ trong vũ trụ thực tế ($n < 10^{80}$).  
  Khi kết hợp đồng thời cả **Path Compression** và **Union by Rank**, chiều cao cây luôn được giữ ở mức gần như phẳng, giúp mỗi thao tác `find` và `union` đạt thời gian khấu hao (amortized time) xấp xỉ hằng số $O(1)$.

---

## 5. CHECKLIST CHUẨN BỊ TRƯỚC GIỜ THUYẾT TRÌNH
- [ ] Mở sẵn bộ Slide mẫu trong trình duyệt (Chrome / Edge / Firefox).
- [ ] Thử nghiệm các phím tắt: `Left`/`Right` (đổi slide), `O` (xem danh sách tổng quan slide), `S` (mở kịch bản ghi chú), `F` (bật Fullscreen).
- [ ] Thử chạy widget mô phỏng tương tác ở Slide 9 để quen tay bấm từng bước.
- [ ] Chuẩn bị sẵn sơ đồ so sánh hoặc file `hanoi_network.json` để mở nếu Giảng viên hỏi sâu về dữ liệu.
