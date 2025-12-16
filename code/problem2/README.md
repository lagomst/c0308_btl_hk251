# 🔓 Tấn công Mã hóa Many-Time Pad (MTP)

## 💡 Giới thiệu và Lỗ hổng (Vulnerability)

Bài toán này là một thử thách mật mã (CTF) khai thác lỗ hổng nghiêm trọng của mã hóa **XOR** (như One-Time Pad - OTP) khi **cùng một khóa ($K$) được sử dụng lại** để mã hóa nhiều thông điệp khác nhau.

* **Mã hóa:** $C_i = M_i \oplus K$
* **Lỗ hổng:** Việc sử dụng lại khóa phá vỡ tính bảo mật, cho phép chúng ta tìm khóa $K$ bằng **phân tích tần suất** (Frequency Analysis). 

---

## 🎯 Chiến lược Tấn công: Phân tích Tần suất trên từng Cột

Do độ dài khóa ($K$) được giới hạn bởi bản mã ngắn nhất ($\text{min\_len}$), ta có thể tấn công từng byte của khóa một cách độc lập.

### 1. Nguyên lý Cơ bản

Mục tiêu là tìm byte khóa $K[i]$ tại vị trí $i$ sao cho khi ta giải mã tất cả các byte $C_j[i]$ bằng $K[i]$, kết quả thu được là các ký tự văn bản gốc ($M_j[i]$) hợp lý nhất.

$$\text{Nếu } K[i] \text{ đúng } \rightarrow M_j[i] = C_j[i] \oplus K[i] \text{ sẽ là các ký tự văn bản thông thường (ASCII).}$$

### 2. Kỹ thuật Chấm điểm (Scoring)

Chúng ta thử 256 giá trị cho $K[i]$ và chấm điểm dựa trên tần suất xuất hiện của các ký tự sau khi giải mã:

| Ký tự | Điểm | Lý do |
| :--- | :--- | :--- |
| **Dấu cách** (`space`, ASCII 32) | Cao nhất | Ký tự **phổ biến nhất** trong văn bản tiếng Anh. |
| **Chữ cái thường** (`a-z`) | Cao | Rất phổ biến. |
| **Chữ cái hoa** (`A-Z`), số, dấu câu | Trung bình | Phổ biến nhưng ít hơn. |
| **Ký tự điều khiển** (ví dụ: ASCII 0-31) | **Phạt nặng** | Ký tự rác, gần như không bao giờ xuất hiện trong bản rõ. |

**Quá trình:**
1.  Lặp qua từng vị trí $i$ (từ 0 đến $\text{min\_len} - 1$).
2.  Với mỗi vị trí $i$, thử $K_{\text{guess}} \in [0, 255]$.
3.  Tính tổng điểm cho $K_{\text{guess}}$ khi áp dụng lên tất cả $C_j[i]$.
4.  Giá trị $K_{\text{guess}}$ nào cho **tổng điểm cao nhất** sẽ là byte khóa $K[i]$ chính xác.

---

## 🛠️ Các Bước Thực hiện Tổng quát

1.  **Chuẩn bị Dữ liệu:** Chuyển đổi tất cả các bản mã Hex sang định dạng Bytes.
2.  **Xác định Độ dài Khóa:** Lấy độ dài của bản mã ngắn nhất ($\text{min\_len}$).
3.  **Vòng lặp Tấn công Chính:** Dùng thuật toán chấm điểm để tìm từng byte $K[i]$.
4.  **Giải mã Cuối cùng:** Sử dụng khóa $K$ đã tìm được để giải mã tất cả các bản mã $C_i$.

## 📝 Tinh chỉnh Thủ công (Crib Dragging)

Thuật toán chấm điểm tự động thường chính xác khoảng **90-95%**. Nếu bản rõ giải mã được còn một vài ký tự lạ (ví dụ: `Th.s is the flag`), bạn cần tinh chỉnh thủ công:

1.  **Đoán:** Giả sử ký tự sai phải là 'i' (để thành `This`).
2.  **Tính lại Key:** Tính lại byte khóa đúng tại vị trí đó bằng công thức XOR ngược:
    $$K_{\text{đúng}}[i] = C_{\text{bản mã}}[i] \oplus M_{\text{đoán}}[i]$$
3.  **Cập nhật:** Thay thế byte khóa đã tìm được bằng tay và giải mã lại để xác nhận.