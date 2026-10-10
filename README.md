# CP-ABE Python Demo

基于 Python 和 PyCryptodome 实现的简化版 CP-ABE（密文策略属性基加密）核心流程模拟。

## 核心流程
- **Setup**: 生成主密钥与公钥
- **KeyGen**: 根据用户属性集合（如 {student, cs}）生成私钥
- **Encrypt**: 使用公钥加密数据
- **Decrypt**: 满足属性策略的用户解密成功，不满足则访问被拒绝

## 运行方式
```bash
pip install pycryptodome
python simple_cpabe.py

项目说明:
本仓库为学习 CP-ABE 工程化实现的第一步。由于纯 Python 无法直接进行双线性对运算，本项目使用 AES 模拟了访问控制加密中的“属性决定解密权限”的核心逻辑。后续计划替换为真实的密码学库。
