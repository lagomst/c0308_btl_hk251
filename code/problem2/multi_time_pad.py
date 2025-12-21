import string

def process_hex_file(file_path):
    array_of_bytes = []
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                clean_line = line.strip()
                
                if clean_line:
                    byte_data = bytes.fromhex(clean_line)
                    
                    array_of_bytes.append(byte_data)
                    
        return array_of_bytes
    except FileNotFoundError:
        print("Không tìm thấy file!")
        return []
    except ValueError as e:
        print(f"Lỗi dữ liệu: {e}. Hãy kiểm tra xem chuỗi hex có ký tự lạ không.")
        return []


ciphertexts = process_hex_file('code/problem2/ciphertext2.txt')

max_len = max(len(c) for c in ciphertexts)
print(f"[*] Có {len(ciphertexts)} bản mã. Đang tấn công toàn bộ {max_len} bytes.")

# Hàm chấm điểm (Giữ nguyên hoặc tinh chỉnh nhẹ)
def score_byte(b):
    if b < 32 or b > 126: 
        return -100 
    c = chr(b) 
    if c == ' ': return 25 
    lower_c = c.lower()
    if lower_c in 'etaoinh': 
        return 20
    if lower_c in 'srdlu': 
        return 15
    if 'a' <= lower_c <= 'z':
        return 10
    if c in ".,'\"?!:;": return 8 
    if c in "0123456789": return 5 
    
    return 1

recovered_key = [] 

for i in range(max_len):
    best_key_byte = 0
    best_score = -float('inf')
    
    for k_guess in range(256):
        current_score = 0
        count = 0 # Đếm xem có bao nhiêu bản mã tham gia vào cột này
        
        for c in ciphertexts:
            if i < len(c):
                decrypted_byte = c[i] ^ k_guess
                current_score += score_byte(decrypted_byte)
                count += 1
        
        if count == 0: continue

        if current_score > best_score:
            best_score = current_score
            best_key_byte = k_guess
            
    recovered_key.append(best_key_byte)

# Hiển thị kết quả
key_bytes = bytes(recovered_key)
print(f"\n--- KEY (HEX): {key_bytes.hex()} ---")

print("\n--- PLAINTEXTS ---")
for idx, c in enumerate(ciphertexts):
    pt = []
    for i in range(len(c)):
        pt.append(c[i] ^ key_bytes[i])
    
    decrypted_text = bytes(pt).decode('utf-8', errors='replace')
    print(f"P[{idx:02d}]: {decrypted_text}")