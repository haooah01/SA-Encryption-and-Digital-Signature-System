from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
import base64

class KeyPairSource:
    def __init__(self):
        # Tạo cặp khóa RSA
        self.key = RSA.generate(2048)
        self.public_key = self.key.publickey()
        self.private_key = self.key

    def get_public_key(self):
        return self.public_key

    def get_private_key(self):
        return self.private_key

    def save_keys(self):
        # Lưu khóa private
        with open("private_key.pem", "wb") as f:
            f.write(self.private_key.export_key('PEM'))
        
        # Lưu khóa public
        with open("public_key.pem", "wb") as f:
            f.write(self.public_key.export_key('PEM'))

class MessageSource:
    @staticmethod
    def create_message(message: str) -> bytes:
        return message.encode('utf-8')

class EncryptionAlgorithm:
    def __init__(self, public_key):
        self.public_key = public_key
        self.cipher = PKCS1_OAEP.new(public_key)

    def encrypt(self, message: bytes) -> bytes:
        # Mã hóa message bằng public key
        return self.cipher.encrypt(message)

class DecryptionAlgorithm:
    def __init__(self, private_key):
        self.private_key = private_key
        self.cipher = PKCS1_OAEP.new(private_key)

    def decrypt(self, encrypted_message: bytes) -> bytes:
        # Giải mã message bằng private key
        return self.cipher.decrypt(encrypted_message)

def main():
    try:
        # Khởi tạo KeyPairSource
        print("Đang tạo cặp khóa RSA...")
        key_source = KeyPairSource()
        key_source.save_keys()
        print("Đã tạo và lưu cặp khóa thành công!")

        # Tạo message từ MessageSource
        message = "Xin chào! Đây là tin nhắn bí mật."
        print(f"\nTin nhắn gốc: {message}")
        message_bytes = MessageSource.create_message(message)

        # Mã hóa message
        print("\nĐang mã hóa tin nhắn...")
        encryptor = EncryptionAlgorithm(key_source.get_public_key())
        encrypted_message = encryptor.encrypt(message_bytes)
        encrypted_b64 = base64.b64encode(encrypted_message).decode('utf-8')
        print(f"Tin nhắn đã mã hóa (Base64): {encrypted_b64}")

        # Giải mã message
        print("\nĐang giải mã tin nhắn...")
        decryptor = DecryptionAlgorithm(key_source.get_private_key())
        decrypted_message = decryptor.decrypt(encrypted_message)
        print(f"Tin nhắn sau giải mã: {decrypted_message.decode('utf-8')}")

        # Thử nghiệm với tin nhắn bị thay đổi
        print("\nThử nghiệm bảo mật:")
        tampered_message = encrypted_message[:-1] + bytes([encrypted_message[-1] ^ 1])
        try:
            decryptor.decrypt(tampered_message)
            print("CẢNH BÁO: Tin nhắn bị thay đổi vẫn giải mã được!")
        except:
            print("Bảo mật hoạt động tốt: Phát hiện tin nhắn bị thay đổi!")

    except Exception as e:
        print(f"Có lỗi xảy ra: {str(e)}")

if __name__ == "__main__":
    main()
