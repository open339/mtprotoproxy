import ssl
import random

class TLSFaker:
    def __init__(self, domain):
        self.domain = domain

    def fake_handshake(self, client_socket):
        try:
            client_socket.sendall(self._generate_fake_hello())
            response = client_socket.recv(4096)
            return b"ServerHello" in response
        except Exception as e:
            print("Fake TLS handshake error:", e)
            return False

    def _generate_fake_hello(self):
        # 简单的伪造 TLS 握手包
        random_bytes = bytes(random.randint(0, 255) for _ in range(32))
        return b"ClientHello" + random_bytes + self.domain.encode()
