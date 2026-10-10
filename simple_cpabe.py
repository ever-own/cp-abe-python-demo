from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

class SimpleCPABE:
    def __init__(self):
        self.master_key = get_random_bytes(16) # 主密钥

    def setup(self):
        """生成公钥：将主密钥与访问策略绑定"""
        return self.master_key

    def keygen(self, public_key, user_attributes):
        """根据用户属性生成私钥"""
        required = {"student", "cs"}  # 策略：必须是学生且属于cs
        if required.issubset(set(user_attributes)):
            return self.master_key
        return None

    def encrypt(self, public_key, message):
        """用公钥加密消息"""
        cipher = AES.new(public_key, AES.MODE_CBC)
        ct = cipher.encrypt(pad(message.encode(), AES.block_size))
        return cipher.iv + ct  # 将IV和密文一起返回

    def decrypt(self, secret_key, ciphertext):
        """用私钥解密"""
        if secret_key is None:
            return "❌ 访问被拒绝：属性不满足策略"
        iv = ciphertext[:16]
        ct = ciphertext[16:]
        cipher = AES.new(secret_key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ct), AES.block_size).decode()

# --- 运行流程 ---
print("=== 初始化 CP-ABE ===")
abe = SimpleCPABE()
pk = abe.setup()
print("1. Setup完成，公钥已生成\n")

print("=== 加密数据 ===")
ct = abe.encrypt(pk, "这是我的论文数据")
print(f"2. 加密完成，密文长度: {len(ct)}字节\n")

print("=== 用户A：属性 = ['student', 'cs'] ===")
sk_a = abe.keygen(pk, ["student", "cs"])
print(f"3. 用户A解密: {abe.decrypt(sk_a, ct)}\n")

print("=== 用户B：属性 = ['student'] ===")
sk_b = abe.keygen(pk, ["student"])
print(f"4. 用户B解密: {abe.decrypt(sk_b, ct)}\n")