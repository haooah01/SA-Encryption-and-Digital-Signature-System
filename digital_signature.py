from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

class DigitalSignature:
    def __init__(self):
        self.key_pair = None
        self.public_key = None
        self.private_key = None

    def generate_key_pair(self):
        # Tạo cặp khóa mới
        self.key_pair = RSA.generate(2048)
        self.private_key = self.key_pair
        self.public_key = self.key_pair.publickey()
        
        # Lưu khóa
        with open("signature_private.pem", "wb") as f:
            f.write(self.private_key.export_key('PEM'))
        with open("signature_public.pem", "wb") as f:
            f.write(self.public_key.export_key('PEM'))

    def sign_message(self, message: str) -> bytes:
        # Tạo hash của message
        h = SHA256.new(message.encode('utf-8'))
        
        # Ký hash bằng private key
        signature = pkcs1_15.new(self.private_key).sign(h)
        return signature

    def verify_signature(self, message: str, signature: bytes) -> bool:
        # Tạo hash của message
        h = SHA256.new(message.encode('utf-8'))
        
        try:
            # Xác thực chữ ký bằng public key
            pkcs1_15.new(self.public_key).verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False

def main():
    try:
        # Khởi tạo đối tượng DigitalSignature
        ds = DigitalSignature()
        
        # Tạo cặp khóa
        print("Đang tạo cặp khóa cho chữ ký số...")
        ds.generate_key_pair()
        print("Đã tạo cặp khóa thành công!")

        # Tin nhắn cần ký
        message = "Đây là tin nhắn cần được ký số để đảm bảo tính xác thực."
        print(f"\nTin nhắn gốc: {message}")

        # Ký tin nhắn
        print("\nĐang ký tin nhắn...")
        signature = ds.sign_message(message)
        print("Đã ký tin nhắn thành công!")

        # Xác thực chữ ký
        print("\nĐang xác thực chữ ký...")
        if ds.verify_signature(message, signature):
            print("Xác thực chữ ký thành công!")
        else:
            print("Xác thực chữ ký thất bại!")

        # Thử nghiệm với tin nhắn bị thay đổi
        tampered_message = message + " [Đã bị thay đổi]"
        print(f"\nThử nghiệm với tin nhắn bị thay đổi: {tampered_message}")
        if ds.verify_signature(tampered_message, signature):
            print("CẢNH BÁO: Xác thực thành công với tin nhắn bị thay đổi!")
        else:
            print("Bảo mật hoạt động tốt: Phát hiện tin nhắn bị thay đổi!")

    except Exception as e:
        print(f"Có lỗi xảy ra: {str(e)}")

if __name__ == "__main__":
    main()
