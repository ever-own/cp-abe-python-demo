from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
#程序中所有的密钥生成过程均为简化示例（即调用get_random_bytes生成随机字符串），实际应用中应使用更复杂的密钥生成和管理机制。
class SimpleCPABE:
    def __init__(self):
        self.master_key = get_random_bytes(16) # 主密钥

    def setup(self):
        """生成公钥：将主密钥与访问策略绑定"""
        return self.master_key

    def keygen(self, public_key, user_attributes):
        """根据用户属性生成私钥"""
        #满足访问策略的条件：用户是advisor，或者是student且属于cs专业
        attrs = set(user_attributes)
        if "advisor" in attrs or ("student" in attrs and "cs" in attrs) or ("department chair" in attrs and "cs" in attrs):
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
        iv = ciphertext[:16]#取出前16字节作为IV
        ct = ciphertext[16:]#取出剩余部分作为密文
        cipher = AES.new(secret_key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ct), AES.block_size).decode()
'''self是类的实例对象，一个具体创建出来的 ABE 方案框架实例
    self.master_key是主密钥，self.setup()生成公钥，self.keygen()根据用户属性生成私钥，self.encrypt()用公钥加密消息，self.decrypt()用私钥解密消息'''
# --- 运行流程 ---
print("=== 初始化 CP-ABE ===")
abe = SimpleCPABE()
pk = abe.setup()
print("1. Setup完成，公钥已生成\n")

print("=== 加密数据 ===")
ct = abe.encrypt(pk, "这是我的论文数据")
print(f"2. 加密完成，密文长度: {len(ct)}字节,密文为: {ct.hex()}\n")

#以下为测试用例
print("=== 用户A：属性 = ['student', 'cs'] ===")
sk_a = abe.keygen(pk, ["student", "cs"])
print(f"3. 用户A解密: {abe.decrypt(sk_a, ct)}\n")

print("=== 用户B：属性 = ['student'] ===")
sk_b = abe.keygen(pk, ["student"])
print(f"4. 用户B解密: {abe.decrypt(sk_b, ct)}\n")

print("=== 用户C：属性 = ['advisor'] ===")
sk_c = abe.keygen(pk, ["advisor"])
print(f"5. 用户C解密: {abe.decrypt(sk_c, ct)}\n")

print("=== 用户D：属性 = ['department chair', 'cs'] ===")
sk_d = abe.keygen(pk, ["department chair", "cs"])
print(f"6. 用户D解密: {abe.decrypt(sk_d, ct)}\n")

print("=== 用户E：属性 = ['department chair', 'ee'] ===")
sk_e = abe.keygen(pk, ["department chair", "ee"])
print(f"7. 用户E解密: {abe.decrypt(sk_e, ct)}\n")
