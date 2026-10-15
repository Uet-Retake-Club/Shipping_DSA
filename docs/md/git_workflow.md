# QUY CHUẨN LÀM VIỆC VỚI GIT & QUY TRÌNH PHỐI HỢP NHÓM (GITFLOW)
> **Dự án:** Smart Delivery Network Design Using MST  
> **Áp dụng cho:** Toàn bộ 6 thành viên trong nhóm

---

## 1. CẤU TRÚC NHÁNH (BRANCHING MODEL)

Mọi thành viên tuân thủ mô hình nhánh chuẩn sau:

- **`main`**: Nhánh chính thức, chứa mã nguồn đã kiểm thử và ổn định 100%. Không bao giờ commit trực tiếp lên `main`.
- **`dev`**: Nhánh tích hợp cho toàn đội. Mọi tính năng sau khi hoàn thành sẽ tạo Pull Request (PR) vào `dev`.
- **`feature/<role-or-feature-name>`**: Nhánh làm việc độc lập của từng thành viên.
  - Ví dụ:
    - `feature/graph-model`: Mô hình đồ thị & đọc ghi JSON/CSV (Graph & Data Modeler)
    - `feature/kruskal-dsu`: Cài đặt DSU & Thuật toán Kruskal (Backend Kruskal)
    - `feature/prim-heap`: Cài đặt Min-Heap & Thuật toán Prim (Backend Prim)
    - `feature/visualization`: Trực quan hóa bản đồ và đồ thị (Visualization Lead)
    - `feature/benchmark`: Benchmark đo đạc thời gian chạy (Visualization & Algo Lead)

---

## 2. QUY TRÌNH PHỐI HỢP LÀM TÍNH NĂNG (FEATURE WORKFLOW)

Mỗi khi bắt đầu một tính năng mới:

### Bước 1: Đồng bộ mã nguồn mới nhất từ `dev`
```bash
git checkout dev
git pull origin dev
```

### Bước 2: Tạo nhánh tính năng mới
```bash
git checkout -b feature/tên-tính-năng
```

### Bước 3: Viết mã nguồn & Unit Tests
Thường xuyên chạy kiểm thử cục bộ:
```bash
python -m pytest tests/
```

### Bước 4: Commit theo chuẩn Conventional Commits
Định dạng commit message:
`<loại>(<phạm vi>): <mô tả ngắn gọn>`

Các loại commit chuẩn:
- `feat`: Tính năng mới (ví dụ: `feat(kruskal): implement dsu with path compression and rank`)
- `fix`: Sửa lỗi (ví dụ: `fix(prim): handle disconnected graph components`)
- `test`: Thêm hoặc sửa unit test (ví dụ: `test(dsu): add cycle detection test cases`)
- `docs`: Thêm hoặc sửa tài liệu (ví dụ: `docs(spec): update node metadata format`)
- `refactor`: Tái cấu trúc code mà không đổi hành vi (ví dụ: `refactor(graph): simplify adjacency list indexing`)
- `perf`: Tối ưu hiệu năng (ví dụ: `perf(heap): optimize bubble-up operation in MinHeap`)

### Bước 5: Đẩy lên remote repository
```bash
git push -u origin feature/tên-tính-năng
```

### Bước 6: Tạo Pull Request (PR)
- Tạo PR trên GitHub từ `feature/tên-tính-năng` vào `dev`.
- Gắn tag người phụ trách liên quan (Reviewer) xem xét.
- Đảm bảo toàn bộ Unit Tests pass trước khi Merge.
- Nhóm trưởng hoặc thành viên phụ trách mảng sẽ phê duyệt và thực hiện **Squash and Merge** hoặc **Rebase and Merge**.

---

## 3. BẢO VỆ NHÁNH & NGUYÊN TẮC AN TOÀN
1. Không commit các file tạm, file rác, file nhị phân lớn hoặc thư mục môi trường ảo `.venv/`. Luôn kiểm tra `git status` trước khi `git add .`.
2. Giữ lịch sử commit sạch, thông điệp rõ ràng để phục vụ việc chấm điểm báo cáo của Giảng viên.
