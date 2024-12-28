import socket
import threading
import json
import os
from encryption import MTProtoEncryptor
from tls_faker import TLSFaker

# 加载配置
with open("config.json", "r") as f:
    config = json.load(f)

# 用户输入
def get_user_input(prompt, default_value=None):
    user_input = input(f"{prompt} (默认: {default_value}): ").strip()
    return user_input if user_input else default_value

def generate_links(secret, port, domain, tag=None):
    base_url = f"tg://proxy?server={domain}&port={port}&secret={secret}"
    fake_tls_link = f"{base_url}&type=fake_tls"
    tls_link = f"{base_url}&type=tls"
    if tag:
        fake_tls_link += f"&tag={tag}"
        tls_link += f"&tag={tag}"
    return fake_tls_link, tls_link

# 提示输入
port = int(get_user_input("请输入代理端口", config["default_port"]))
aes_key = get_user_input("请输入 32 字节密钥", os.urandom(32).hex()[:32])
domain = get_user_input("请输入伪造的 TLS 域名", config["default_domain"])
tag = get_user_input("请输入广告标签 (可选)", config["tag"])

# 显示链接
fake_tls_link, tls_link = generate_links(aes_key, port, domain, tag)
print("\n以下是生成的链接:")
print(f"Fake TLS 链接: {fake_tls_link}")
print(f"TLS 链接: {tls_link}\n")

# 初始化加密模块和伪造 TLS 模块
encryptor = MTProtoEncryptor(aes_key)
tls_faker = TLSFaker(domain)

def handle_client(client_socket):
    try:
        # 处理伪造 TLS 握手
        fake_handshake = tls_faker.fake_handshake(client_socket)
        if not fake_handshake:
            print("TLS 握手失败")
            return

        # 接收并解密数据
        data = client_socket.recv(4096)
        decrypted_data = encryptor.decrypt(data)
        print("接收到消息:", decrypted_data)

        # 加密并发送响应
        response = "Hello from Fake TLS MTProto Proxy"
        encrypted_response = encryptor.encrypt(response.encode())
        client_socket.send(encrypted_response)

    except Exception as e:
        print("Error:", e)
    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)
    print(f"Fake TLS MTProto Proxy 正在运行，监听端口 {port}")

    while True:
        client_socket, addr = server.accept()
        print(f"接收到连接请求来自: {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
