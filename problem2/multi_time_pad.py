import string

# BƯỚC 1: CHUẨN BỊ DỮ LIỆU
# Đây là toàn bộ ciphertext của bạn
hex_ciphertexts = [
    "030d091e0052020f0d32451b0d16520c411d3f0c1c4c111a0c154e2710184c111d4d120b36",
    "030d094c0b1300044e38034c180d174d12063e154c1b04014d150632452e05091e1441217045380904",
    "030d094c121b03051d770700091252181142770d091e451002164e330c1c1c00164d0501200b",
    "18450e000a054141032e450e19091e14410c381c1f404510010e19",
    "040a0302451f0c184e230d094c3217010d0b25080d024511020c0b",
    "030a4c0e171b03064e22164c1f10150c134e360b084c11170c410f39014c1e101f",
    "180b094c0113144d4e200d0902450605044e230a020b101b03464e3e164c080a1c08",
    "00004b00095219000532450319175201040f21004c0d0b164d0601",
    "040d094c0d1309410038114c0e001703411a200a4c1b001706124e311703014501050e1c32",
    "000d09024516021600770a024c0d171f410f7717050b0d064d16063609094c071d1f04",
    "030d094c06131d150f3e0b4c0f041e01040a77040000451a0c0f0a24450d0201521e16012500",
    "1f004b0845060c0a0b7711040d11521a090f3b004c050b52190e19",
    "15000a0317174d150632450e0304064d090f33450405115219090b77120d180000",
    "030d094c121a0c0d0b70164c18041b01410d3608094c10024d000033450f0d101505154e3f001e",
    "1609004c0d1303051d7711034c111a08411d3e010940451a0c131e380a020901520c0f0a77030319021a1941063217",
    "000d0902450105044e330c1a090152090e1939450e09091d1a",
    "190a4c000c1c08411936164c0f100641410038451b04041e08411936164c0a17170805",
    "030d094c26131d150f3e0b4b1f451f040f0a77120d1f451c02154e38034c0b17170805",
    "1510184c0d174d030b3b0a020b00164d150177110409450505000232080d0242014d021c320008",
    "040d094c111d020a4e230d094c161a04114e3e0b4c180a05",
    "110a1e4c031d1f151777010d15165e4d0e1c77001a090b52000e1c32",
    "030d094c091b03044e20000218450101000d3c494c180d1703411a3e020418451d03020b7708031e00",
    "1609004c071d0c151d7712091e0052010e1d23494c180d171f044e20001e09451d030d177703031917",
    "1510184c1606040d027711040d11521a090f3b004c080c164d0601",
    "16164c0a04004d001d772c4b1a005205040f2501404c111a0841083e02041842014d121a3e09004c0a1c",
    "030d094c091b0304492445020311520e141a77040208450605044e200d0d0000551e410038114c0b0a1c08",
    "030d094c3217010d0b25080d02451f0c0a0b2445040516521f040922090d1e45110c0d02",
    "030a4c090b1102141c3602094c111a08412d3615180d0c1c41410d25001b40451303054e360900",
]

# Chuyển đổi hex sang bytes
ciphertexts = [bytes.fromhex(c) for c in hex_ciphertexts]

# Tìm độ dài ngắn nhất, vì ta chỉ có thể tấn công các cột mà mọi C đều có
min_len = min(len(c) for c in ciphertexts)
print(f"[*] Có {len(ciphertexts)} bản mã. Tấn công trên {min_len} bytes đầu tiên.")

# ----------------------------------------------------

# BƯỚC 2: HÀM CHẤM ĐIỂM
# Hàm này chấm điểm "độ hợp lý" của một byte
# Điểm cao cho ký tự phổ biến, điểm âm nặng cho ký tự "rác"
def score_byte(b):
    b = int(b)
    # Giả sử văn bản là tiếng Anh (hoặc ASCII)
    
    # Dấu cách (space) là phổ biến nhất
    if b == 32:
        return 20
    # Ký tự chữ cái thường (rất phổ biến)
    if b >= 97 and b <= 122: # a-z
        return 15
    # Ký tự chữ hoa (phổ biến)
    if b >= 65 and b <= 90: # A-Z
        return 10
    # Dấu câu và số (khá phổ biến)
    if b in b".,'\"?!:;()[]{}0123456789":
        return 5
    # Ký tự điều khiển (control chars) và ký tự rác
    # Đây là những ký tự gần như KHÔNG BAO GIỜ xuất hiện
    if b < 32 or b > 126:
        return -50 # Phạt rất nặng
    
    # Các trường hợp khác (ví dụ: #, $, %, ^, &)
    return 1

# ----------------------------------------------------

# BƯỚC 3: VÒNG LẶP TẤN CÔNG CHÍNH

recovered_key = [] # Key sẽ được lưu ở đây

# Lặp qua từng cột (từng byte)
for i in range(min_len):
    best_key_byte = 0
    best_score = -float('inf') # Điểm thấp vô cùng
    
    # Thử 256 giá trị có thể có cho key_byte (0-255)
    for k_guess in range(256):
        current_score = 0
        
        # Thử giải mã CỘT THỨ i của TẤT CẢ các bản mã
        for c in ciphertexts:
            # c[i] là byte thứ i của bản mã c
            decrypted_byte = c[i] ^ k_guess
            current_score += score_byte(decrypted_byte)
            
        # So sánh điểm
        if current_score > best_score:
            best_score = current_score
            best_key_byte = k_guess
            
    # Sau khi thử hết 256 giá trị, `best_key_byte` là byte key tốt nhất
    recovered_key.append(best_key_byte)

# ----------------------------------------------------

# BƯỚC 4: HIỂN THỊ KẾT QUẢ

print("\n--- KHÓA (KEY) ĐÃ ĐƯỢC PHỤC HỒI (dạng bytes) ---")
# Chuyển danh sách số int sang đối tượng bytes
key_bytes = bytes(recovered_key)
print(key_bytes.hex()) # In key ở dạng hex

print("\n--- CÁC BẢN RÕ (PLAINTEXT) ĐÃ ĐƯỢC GIẢI MÃ (THỬ) ---")

# Hàm XOR 2 mảng bytes
def xor_bytes(a, b):
    # Lấy độ dài ngắn hơn để xor
    length = min(len(a), len(b))
    return bytes([a[i] ^ b[i] for i in range(length)])

# In kết quả giải mã
for i, c in enumerate(ciphertexts):
    decrypted_text = xor_bytes(c, key_bytes)
    
    # Chúng ta chỉ có thể giải mã an toàn đến min_len
    # Phần còn lại của bản mã (nếu dài hơn) sẽ bị xor với key_bytes lặp lại
    # nhưng vì key của chúng ta chỉ dài min_len, chúng ta chỉ nên in phần đó
    
    # Thử in ra dạng 'utf-8', bỏ qua các lỗi
    print(f"P[{i:02d}]: {decrypted_text.decode('utf-8', errors='ignore')}")