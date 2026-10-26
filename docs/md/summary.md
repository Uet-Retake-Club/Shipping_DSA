# Abstraction

Trong bài thuyết trình này ta sẽ tìm hiểu về ứng dụng của MST, các thuật toán tiền nhiệm của nó cũng như hai thuật toán phổ biến nhất hiện nay được sử dụng để xây dựng MST.

# Introduction

### Định nghĩa

(Wiki) Với một [đồ thị liên thông](https://vi.wikipedia.org/wiki/%C4%90%E1%BB%93_th%E1%BB%8B_li%C3%AAn_th%C3%B4ng "Đồ thị liên thông"), [vô hướng](https://vi.wikipedia.org/wiki/%C4%90%E1%BB%93_th%E1%BB%8B_v%C3%B4_h%C6%B0%E1%BB%9Bng "Đồ thị vô hướng") cho trước, [cây bao trùm](https://vi.wikipedia.org/wiki/C%C3%A2y_bao_tr%C3%B9m "Cây bao trùm") của nó là một [đồ thị con](https://vi.wikipedia.org/wiki/Thu%E1%BA%ADt_ng%E1%BB%AF_l%C3%BD_thuy%E1%BA%BFt_%C4%91%E1%BB%93_th%E1%BB%8B#%C4%90%E1%BB%93_th%E1%BB%8B_con "Thuật ngữ lý thuyết đồ thị") có dạng cây và có tất cả các [đỉnh](https://vi.wikipedia.org/wiki/%C4%90%E1%BB%93_th%E1%BB%8B_\(l%C3%BD_thuy%E1%BA%BFt_%C4%91%E1%BB%93_th%E1%BB%8B\) "Đồ thị (lý thuyết đồ thị)") liên thông với nhau. Một đồ thị có thể có nhiều cây bao phủ khác nhau. Chúng ta cũng có thể gán một _trọng số_ cho mỗi cạnh, là con số biểu thị sự "không ưa thích" và dùng nó để tính trọng số của một cây bao trùm bằng cách cộng tất cả trọng số của các cạnh trong cây bao trùm đó. Khi đó, một **cây bao trùm nhỏ nhất** là một cây bao trùm có trọng số bé hơn hoặc bằng trọng số của tất cả các cây bao trùm khác. Tổng quát hơn, bất kỳ một đồ thị vô hướng (không nhất thiết liên thông) đều có một **rừng bao phủ nhỏ nhất**, là hợp của các cây bao trùm nhỏ nhất của các [thành phần liên thông](https://vi.wikipedia.org/wiki/Th%C3%A0nh_ph%E1%BA%A7n_li%C3%AAn_th%C3%B4ng "Thành phần liên thông") của nó.

(VNOI) Theo lý thuyết đồ thị, một đồ thị được biểu diễn bằng công thức $G=(V,E)$, trong đó $V$ là tập các đỉnh và $E$ là tập các cạnh.

- **Cây bao phủ (_spanning tree_)** của đồ thị là một tập hợp các cạnh của đồ thị thỏa mãn tập cạnh này **không chứa chu trình** và **liên thông** (từ một đỉnh bất kì có thể đi tới bất kỳ đỉnh nào khác mà chỉ dùng các cạnh trên **cây khung**).
- Trong đồ thị **có trọng số**, **cây bao phủ nhỏ nhất (_minimum spanning tree_)** là **cây khung** có tổng trọng số các cạnh trong cây **nhỏ nhất**.

# Các thuật toán tiền nhiệm

**Thuật toán Borůvka**: Ban đầu thuật toán khởi tạo cây bao trùm cần tìm là một tập rỗng và dần dần từng bước thêm các cạnh vào tập hợp đó. Trong mỗi bước, với mỗi thành phần liên thông hiện tại, thuật toán chọn cạnh nhỏ nhất nối thành phần đó với một đỉnh nằm ngoài nó, thêm cạnh này vào cây bao trùm và hợp các thành phần ở hai đầu cạnh lại làm một. Lặp lại cho tới khi đồ thị chỉ còn đúng một thành phần liên thông.

```
1  Khởi tạo một tập rỗng T
2  Chừng nào các đỉnh của G vẫn chưa liên thông bởi tập cạnh trong T:
3      Khởi tạo một tập rỗng E
4      Với mỗi thành phần liên thông S:
5          Thêm cạnh nhỏ nhất nối S với một đỉnh không thuộc S vào E
6      Thêm tập hợp E vào T
7  Tập hợp T là một cây bao trùm nhỏ nhất của G
```

Độ phức tạp: $O(|E| \log |V|)$

# Các thuật toán hiện tại

### Các tính chất hữu dụng

Mỗi tính chất dưới đây được phát biểu kèm chứng minh.

#### 1. Tính chất chu trình

**Phát biểu:** Trong một chu trình $C$ bất kỳ, nếu $e$ là cạnh có trọng số lớn nhất **tuyệt đối** (không có cạnh nào khác có trọng số bằng $e$) thì $e$ không thể nằm trên bất kỳ cây khung nhỏ nhất nào.

**Chứng minh:** Giả sử $e$ thuộc một cây khung $T$ của đồ thị, ta sẽ chứng minh luôn tồn tại một cây khung khác có trọng số nhỏ hơn $T$.

- Xóa cạnh $e$ khỏi $T$. Lúc này $T$ bị chia làm 2 thành phần liên thông và tổng trọng số giảm đi $w_e$.
- Giả sử sau khi xóa $e$, các đỉnh trong chu trình $C$ vẫn liên thông với nhau. Khi thêm $e$ trở lại, $e$ sẽ nối 2 đỉnh đã liên thông ⇒ tồn tại chu trình trong cây khung ⇒ trái với giả thiết $T$ là cây khung. Vậy khi xóa $e$ khỏi $T$, các đỉnh của $C$ bị tách làm 2 thành phần liên thông.
- Do đó ta có thể chọn một cạnh $e'$ khác $e$ thuộc chu trình $C$ để nối 2 thành phần này, biến $T$ trở lại thành một cây khung. Vì $e$ có trọng số lớn nhất tuyệt đối trên $C$, nên khi thay $e$ bằng $e'$, trọng số của $T$ giảm đi $w_e - w_{e'} > 0$.

**Kết luận:** $T$ không phải là cây khung nhỏ nhất của đồ thị.

#### 2. Đường đi hẹp nhất

**Phát biểu:** Xét 2 đỉnh $u, v$ bất kỳ trong đồ thị. Nếu $w$ là trọng số của cạnh lớn nhất trên đường đi từ $u$ đến $v$ trên cây khung nhỏ nhất của đồ thị thì không thể tìm được đường đi nào từ $u$ đến $v$ trên đồ thị ban đầu chỉ đi qua những cạnh có trọng số nhỏ hơn $w$.

**Chứng minh:**

- Xét cây khung $T$ bất kỳ của đồ thị $G$ mà tồn tại đường đi $u \to v$ trên $G$ có cạnh lớn nhất **nhỏ hơn** cạnh lớn nhất của đường đi $u \to v$ trên $T$. Gọi đường đi trên $G$ là $path$, cạnh lớn nhất của đường đi $u \to v$ trên $T$ là $e$.
- Nếu xóa $e$ khỏi $T$, cây khung bị chia thành 2 thành phần liên thông rời nhau, một chứa $u$ và một chứa $v$.
- Do $path$ là đường đi $u \to v$ trên $G$ nên trên $path$ tồn tại cạnh $e'$ nối 2 thành phần này. Mọi cạnh trên $path$ đều có trọng số nhỏ hơn $e$ (theo giả thiết) ⇒ khi xóa $e$ và thay bằng $e'$, ta thu được cây khung $T'$ có trọng số nhỏ hơn $T$.

**Kết luận:** $T$ không phải cây khung nhỏ nhất của đồ thị.

#### 3. Tính duy nhất

**Phát biểu:** Nếu tất cả các cạnh đều có trọng số khác nhau thì chỉ có duy nhất một cây khung nhỏ nhất. Ngược lại, nếu một vài cạnh có trọng số giống nhau thì có thể có nhiều hơn một cây khung nhỏ nhất.

**Chứng minh (cho trường hợp trọng số đôi một khác nhau):**

- Giả sử tồn tại 2 cây khung nhỏ nhất $T$ và $T'$. Xét cạnh $u-v$ nằm trong $T$ nhưng không nằm trong $T'$.
- Gọi đường đi $u \to v$ trên $T$ là $path$, trên $T'$ là $path'$. Hiển nhiên $path'$ không chứa cạnh $u-v$.
- Vì trọng số các cạnh đều khác nhau ⇒ cạnh lớn nhất của $path$ có trọng số lớn hơn cạnh lớn nhất của $path'$, hoặc ngược lại.
- Theo tính chất đường đi hẹp nhất, $T$ hoặc $T'$ không phải là cây khung nhỏ nhất. Mâu thuẫn.

#### 4. Tính chất cạnh nhỏ nhất

**Phát biểu:** Nếu $e$ là cạnh có trọng số nhỏ nhất của đồ thị, và không có cạnh nào khác có trọng số bằng $e$ thì $e$ nằm trong mọi cây khung nhỏ nhất của đồ thị.

**Chứng minh:** Ta chứng minh mọi cây khung không chứa $e$ đều không phải là cây khung nhỏ nhất.

- Giả sử $e$ nối 2 đỉnh $u$, $v$. Gọi $T$ là một cây khung không chứa $e$.
- Xét cạnh $e'$ bất kỳ thuộc đường đi từ $u \to v$ trên $T$. Khi xóa $e'$ khỏi $T$, $T$ tách làm 2 thành phần liên thông, một chứa $u$, một chứa $v$. Do đó ta có thể thêm cạnh $e$ (nối $u-v$) để nối 2 thành phần này, $T$ trở lại thành một cây khung.
- Vì $e$ có trọng số nhỏ nhất tuyệt đối của đồ thị, nên khi thay $e'$ bằng $e$, trọng số của $T$ giảm đi một lượng dương.

**Kết luận:** $T$ ban đầu không phải là cây khung nhỏ nhất của đồ thị.

---

### 1. Thuật toán Kruskal

**Ý tưởng thuật toán**: Ban đầu mỗi đỉnh là một cây riêng biệt, ta tìm cây khung nhỏ nhất bằng cách duyệt các cạnh theo trọng số từ nhỏ đến lớn, rồi hợp nhất các cây lại với nhau.

Cụ thể hơn, giả sử cạnh đang xét nối 2 đỉnh $u$ và $v$, nếu 2 đỉnh này nằm ở 2 cây khác nhau thì ta thêm cạnh này vào cây khung, đồng thời hợp nhất 2 cây chứa $u$ và $v$.

Giả sử ta cần tìm cây khung nhỏ nhất của đồ thị $G$. Thuật toán gồm các bước sau:

- Khởi tạo rừng $F$ (tập hợp các cây), trong đó mỗi đỉnh của $G$ tạo thành một cây riêng biệt.
- Khởi tạo tập $S$ chứa tất cả các cạnh của $G$.
- Chừng nào $S$ còn **khác rỗng** và $F$ gồm **hơn một cây**:
    - Xóa cạnh nhỏ nhất trong $S$.
    - Nếu cạnh đó nối hai cây khác nhau trong $F$, thì thêm nó vào $F$ và hợp hai cây kề với nó làm một.
    - Nếu không thì loại bỏ cạnh đó.

Khi thuật toán kết thúc, rừng chỉ gồm đúng một cây và đó là một cây khung nhỏ nhất của đồ thị $G$.

### Chứng minh

Cần chứng minh hai điều:

1. Đầu ra của thuật toán là một cây khung.
2. Cây đó có trọng số nhỏ nhất trong số tất cả các cây khung của đồ thị.

**Chứng minh (1)**

- Mỗi cạnh $(u,v)$ được xét chỉ được kết nạp vào cây khung nếu $u, v$ thuộc 2 thành phần liên thông khác nhau $T_u, T_v$ ⇒ các cạnh được thêm không tạo thành chu trình.
- Do $T$ không có chu trình ⇒ số cạnh được thêm $\le n-1$. Ta sẽ chứng minh $T$ có đúng $n-1$ cạnh:
    - Giả sử số cạnh được thêm $< n-1$ ⇒ $T$ gồm hai hay nhiều thành phần liên thông.
    - Mặt khác, do $G$ liên thông ⇒ tồn tại các cạnh của $G$ nối các thành phần liên thông đó mà không thuộc $T$. Cạnh nhỏ nhất trong số các cạnh này sẽ được đưa vào vì không tạo chu trình, mâu thuẫn với giả thiết ⇒ giả sử sai.
    - Vậy số cạnh được thêm vào bằng đúng $n-1$.

**Chứng minh (2)**

Gọi $T$ là cây khung đầu ra của thuật toán Kruskal và $T^{\ast}$ là một cây khung nhỏ nhất. Ta sẽ chứng minh $c(T) = c(T^{\ast})$.

- Nếu $T = T^{\ast}$ thì hiển nhiên đúng.
    
- Nếu $T \ne T^{\ast}$, gọi $(u,v)$ là cạnh thuộc $T - T^{\ast}$, và $S$ là thành phần liên thông chứa $u$ tại thời điểm $(u,v)$ được thêm vào $T$.
    
    **Nhận xét:** Nếu xóa cạnh $(u,v)$ trên $T$ thì $T$ tách thành 2 thành phần liên thông $S$ và $G-S$. Đây là một **lát cắt**; ta có thể thêm bất cứ cạnh nào nối giữa 2 thành phần này để tạo thành một cây mới ⇒ $(u,v) \in$ lát cắt $(S, G-S)$.
    
- Ta chứng minh $(u,v)$ có trọng số nhỏ nhất trong lát cắt $(S, G-S)$:
    
    - Nếu tồn tại cạnh $e$ từ $S$ đến $G-S$ có trọng số nhỏ hơn $(u,v)$, thuật toán Kruskal sẽ chọn $e$ thay vì $(u,v)$ ⇒ vô lý. Vậy $(u,v)$ có **trọng số nhỏ nhất** trong các cạnh từ $S$ đến $G-S$. **(†)**
    - Mặt khác, vì $T^{\ast}$ là cây khung nên có một đường từ $S$ tới $G-S$ trên $T^{\ast}$; gọi $(x,y)$ là cạnh thuộc đường này và cắt lát cắt. Xét cây khung $T^{\ast\prime} = T^{\ast} \cup {(u,v)} - {(x,y)}$, suy ra $c(T^{\ast\prime}) = c(T^{\ast}) + c(u,v) - c(x,y)$.
    - Theo **(†)** có $c(u,v) \le c(x,y)$ nên $c(T^{\ast\prime}) \le c(T^{\ast})$. Mà $T^{\ast}$ là cây khung nhỏ nhất ⇒ $c(T^{\ast\prime}) = c(T^{\ast})$ và $T^{\ast\prime}$ cũng là **cây khung nhỏ nhất**, đồng thời $|T - T^{\ast\prime}| = |T - T^{\ast}| - 1$.
    
    _**Ý nghĩa:** Ta đã biến đổi cây khung nhỏ nhất $T^{\ast}$ thành cây khung nhỏ nhất $T^{\ast\prime}$ làm giảm số cạnh khác nhau giữa nó và $T$ đi 1 cạnh._
    
- Lặp lại cách chứng minh với mỗi cạnh thuộc $T - T^{\ast\prime}$, ta biến đổi được cây khung nhỏ nhất ban đầu thành $T$, hay nói cách khác $c(T) = c(T^{\ast})$.
    

**Đánh giá độ phức tạp thuật toán:**

Gọi $n$ là số đỉnh, $m$ là số cạnh của đồ thị. Thuật toán gồm 2 phần:

- Sắp xếp $m$ cạnh theo trọng số tăng dần mất $O(m \log m)$.
- Duyệt $m$ cạnh, mỗi cạnh dùng Disjoint Set mất $O(\log n)$, tổng cộng $O(m \log n)$.

⇒ Độ phức tạp của thuật toán Kruskal là $O(m \log m + m \log n)$, tương đương $O(m \log n)$ vì $\log m \le 2\log n$.

### 2. Thuật toán Prim

**Ý tưởng thuật toán**: Ý tưởng của thuật toán Prim rất giống với thuật toán Dijkstra (tìm đường đi ngắn nhất trên đồ thị). Nếu như thuật toán **Kruskal** xây dựng cây khung nhỏ nhất bằng cách kết nạp từng **cạnh** thì thuật toán **Prim** kết nạp từng **đỉnh** theo tiêu chí: đỉnh được nạp vào tiếp theo phải **chưa được nạp** và **gần nhất** với các đỉnh đã được nạp.

Thuật toán bao gồm các bước sau:

- Khởi tạo tập $S$ là cây khung hiện tại, ban đầu $S$ chưa có đỉnh nào.
- Khởi tạo mảng $D$ trong đó $D_i$ là khoảng cách ngắn nhất từ đỉnh $i$ đến một đỉnh đã được kết nạp vào $S$, ban đầu $D[i] = +\infty$ (đỉnh xuất phát có $D = 0$).
- Lặp lại các thao tác sau $n$ lần ($n$ là số đỉnh của đồ thị):
    - Tìm đỉnh $u$ không thuộc $S$ có $D_u$ nhỏ nhất, thêm $u$ vào tập $S$.
    - Xét tất cả các đỉnh $v$ kề $u$, cập nhật $D_v = \min(D_v, w_{u,v})$ với $w_{u,v}$ là trọng số cạnh $u-v$. Nếu $D_v$ được cập nhật theo $w_{u,v}$ thì đánh dấu $trace_v = u$.
    - Thêm cạnh $u - trace[u]$ vào tập cạnh thuộc cây khung nhỏ nhất (trừ đỉnh xuất phát, vốn chưa có $trace$).

**Đánh giá độ phức tạp thuật toán:**

- Duyệt tổng cộng $n$ lần, mỗi lần lấy 1 đỉnh ra khỏi heap mất $O(\log n)$; cập nhật trọng số của tất cả các đỉnh kề, tổng số lần cập nhật là $m$, mỗi lần mất $O(\log n)$.
- Như vậy, độ phức tạp của thuật toán Prim là $O((m+n)\log n)$ với $n$ là số đỉnh và $m$ là số cạnh của đồ thị.

**Bonus:** Có thể sử dụng [Visualgo](https://visualgo.net/en/mst) để mô phỏng thuật toán Kruskal và Prim thông qua hoạt ảnh, qua đó hiểu thêm về các thuật toán trên.

# Đánh giá và so sánh các thuật toán

Cả ba thuật toán Borůvka, Kruskal và Prim đều là thuật toán **tham lam (greedy)**: ở mỗi bước chọn một cạnh "có lợi nhất" mà vẫn đảm bảo không tạo chu trình. Tính đúng đắn của chúng đều dựa trên các tính chất đã chứng minh ở trên (tính chất chu trình, tính chất cạnh nhỏ nhất, và dạng tổng quát của nó là tính chất lát cắt: cạnh nhỏ nhất đi qua một lát cắt luôn thuộc một cây khung nhỏ nhất). Điểm khác nhau nằm ở **cách chọn cạnh** và **cấu trúc dữ liệu** đi kèm.

Trong phần này, $n$ là số đỉnh và $m$ là số cạnh của đồ thị.

### So sánh tổng quan

|Tiêu chí|Borůvka|Kruskal|Prim|
|---|---|---|---|
|Hướng tiếp cận|Mỗi thành phần liên thông chọn cạnh nhỏ nhất đi ra khỏi nó|Duyệt toàn bộ cạnh theo thứ tự trọng số tăng dần|Lớn dần một cây duy nhất từ một đỉnh xuất phát|
|Đơn vị được kết nạp|Cạnh (nhiều cạnh cùng lúc ở mỗi vòng)|Cạnh|Đỉnh|
|Trạng thái trung gian|Rừng các cây|Rừng các cây|Một cây duy nhất|
|Cấu trúc dữ liệu chính|Disjoint Set (hoặc gộp đỉnh)|Sắp xếp cạnh và Disjoint Set|Heap hoặc mảng|
|Độ phức tạp|$O(m \log n)$|$O(m \log n)$|$O((n+m)\log n)$ với binary heap|
|Biểu diễn đồ thị phù hợp|Danh sách cạnh|Danh sách cạnh|Danh sách kề hoặc ma trận kề|
|Đồ thị không liên thông|Cho ra rừng bao phủ nhỏ nhất|Cho ra rừng bao phủ nhỏ nhất|Phải chạy lại từ mỗi thành phần liên thông|
|Khả năng song song hóa|Tốt|Hạn chế|Hạn chế|

### Đánh giá từng thuật toán

**Borůvka**

- Mỗi vòng lặp, số thành phần liên thông giảm ít nhất một nửa, nên chỉ cần $O(\log n)$ vòng, mỗi vòng duyệt $O(m)$ cạnh, tổng cộng $O(m \log n)$.
- Ưu điểm: các thành phần được xử lý độc lập trong cùng một vòng, nên rất phù hợp để chạy song song hoặc phân tán. Đây cũng là lý do thuật toán này vẫn được dùng làm bước khởi đầu trong nhiều thuật toán MST hiện đại.
- Nhược điểm: khi có nhiều cạnh trùng trọng số, cần một quy tắc phá hòa nhất quán (ví dụ so sánh thêm chỉ số cạnh), nếu không các thành phần có thể chọn các cạnh tạo thành chu trình. Cài đặt cũng phức tạp hơn Kruskal.

**Kruskal**

- Chi phí chủ yếu nằm ở bước sắp xếp $O(m \log m)$. Vì $m \le n^2$ nên $\log m \le 2 \log n$, do đó $O(m \log m) = O(m \log n)$. Phần Disjoint Set (có nén đường đi và hợp theo hạng) chỉ tốn khoảng $O(m\,\alpha(n))$, gần như hằng số.
- Ưu điểm: dễ cài đặt, chỉ cần danh sách cạnh. Nếu các cạnh đã được sắp xếp sẵn hoặc trọng số là số nguyên nhỏ (dùng counting sort), thuật toán chạy gần tuyến tính. Thuật toán có thể dừng sớm khi đã chọn đủ $n-1$ cạnh.
- Nhược điểm: phải sắp xếp toàn bộ cạnh, nên kém hiệu quả trên đồ thị dày ($m \approx n^2$). Thuật toán cũng cần lưu toàn bộ danh sách cạnh, không hợp với đồ thị cho ngầm (cạnh chỉ được tính khi cần).

**Prim**

- Với binary heap, mỗi đỉnh được lấy ra một lần và mỗi cạnh gây ra tối đa một lần cập nhật, tổng cộng $O((n+m)\log n)$. Với Fibonacci heap, độ phức tạp giảm còn $O(m + n \log n)$. Nếu dùng mảng thay cho heap, độ phức tạp là $O(n^2)$ và không cần cấu trúc dữ liệu phức tạp.
- Ưu điểm: hiệu quả trên đồ thị dày, đặc biệt bản $O(n^2)$ dùng mảng. Thuật toán không cần sắp xếp toàn bộ cạnh nên phù hợp với đồ thị cho ngầm, ví dụ bài toán nối $n$ điểm trên mặt phẳng với khoảng cách là trọng số. Cây luôn liên thông ở mọi bước.
- Nhược điểm: chỉ xử lý được một thành phần liên thông mỗi lần chạy, và khó song song hóa vì mỗi bước phụ thuộc vào bước trước.

### Khi nào nên dùng thuật toán nào?

|Tình huống|Lựa chọn gợi ý|Lý do|
|---|---|---|
|Đồ thị thưa ($m$ cỡ $n$), đầu vào là danh sách cạnh|Kruskal|Ngắn gọn, dễ cài, chi phí chủ yếu là sắp xếp|
|Đồ thị dày ($m$ cỡ $n^2$)|Prim (bản mảng $O(n^2)$ hoặc Fibonacci heap)|Tránh phải sắp xếp $O(n^2)$ cạnh|
|Cạnh đã sắp xếp sẵn hoặc trọng số nguyên nhỏ|Kruskal|Gần tuyến tính theo $m$|
|Đồ thị cho ngầm (ví dụ các điểm trên mặt phẳng)|Prim|Không cần liệt kê trước mọi cạnh|
|Xử lý song song hoặc phân tán|Borůvka|Mỗi thành phần chọn cạnh độc lập|
|Đồ thị không liên thông, cần rừng bao phủ nhỏ nhất|Kruskal hoặc Borůvka|Cho ra rừng một cách tự nhiên|

### Một số lưu ý chung

- **Khác với Dijkstra:** Prim có ý tưởng gần giống Dijkstra nhưng cập nhật $D_v = \min(D_v, w_{u,v})$ chứ không phải $D_u + w_{u,v}$. Vì vậy cả Prim và Kruskal vẫn đúng khi đồ thị có cạnh trọng số âm, trong khi Dijkstra thì không.
- **Tính duy nhất:** nếu các trọng số đôi một khác nhau thì MST là duy nhất, nên cả ba thuật toán cho cùng một kết quả. Nếu có trọng số trùng nhau, các thuật toán có thể cho ra các cây khác nhau nhưng tổng trọng số luôn bằng nhau.
- **Trong thực tế:** Kruskal và Prim (cài đặt bằng heap) là hai lựa chọn phổ biến nhất vì đơn giản và đủ nhanh. Việc chọn giữa hai thuật toán này chủ yếu phụ thuộc vào mật độ cạnh của đồ thị và dạng dữ liệu đầu vào.