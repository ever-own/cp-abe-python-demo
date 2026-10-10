'''AES是一个对称加密算法，属于块加密算法。它可以使用不同的密钥长度（128位、192位或256位）来加密和解密数据。
本例以AES-128为例，演示了如何使用Python的Crypto库进行AES加密和解密操作。'''
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad#pad和unpad函数用于对数据进行填充和去填充，以确保数据长度是块大小的整数倍。
from Crypto.Random import get_random_bytes#get_random_bytes函数用于生成随机字节序列，通常用于生成密钥或初始化向量（IV）。

key = get_random_bytes(16)  # 生成128位密钥
data = "Hello, AES!".encode('utf-8')

# 加密
cipher = AES.new(key, AES.MODE_CBC)#它根据传入的密钥和加密模式配置一个 cipher（作为加密或解密对象）
ct = cipher.encrypt(pad(data, AES.block_size))#对加密对象cipher调用encrypt方法进行加密，传入的参数是经过pad函数填充后的数据。
#pad函数会根据AES的块大小对数据进行填充，以确保数据长度是块大小的整数倍。
print("加密后:", ct.hex())#密文ct是一个字节串，使用hex()方法将其转换为十六进制字符串进行打印输出。

# 解密
decipher = AES.new(key, AES.MODE_CBC, cipher.iv)#需要使用同一个密钥和 IV，才能还原明文;
#decipher是解密对象，使用与加密时相同的密钥和IV进行初始化。
pt = unpad(decipher.decrypt(ct), AES.block_size)#pt是解密后的明文，使用unpad函数去除填充，恢复原始数据。
print("解密后:", pt.decode('utf-8'))#打印解密后的明文