import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64

class ModernButton(ttk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(style='Modern.TButton')

class RSAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng Mã hóa RSA & Chữ ký số")
        self.root.geometry("900x700")
        
        # Tạo style cho giao diện
        self.create_styles()
        
        # Khởi tạo các biến
        self.private_key = None
        self.public_key = None
        
        # Tạo frame chính
        main_frame = ttk.Frame(root, style='Main.TFrame')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill='x', pady=10)
        ttk.Label(header_frame, text="HỆ THỐNG MÃ HÓA VÀ CHỮ KÝ SỐ RSA",
                 style='Header.TLabel').pack()
        
        # Tạo notebook để chứa các tab
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True, pady=10)
        
        # Tab quản lý khóa
        self.create_key_management_tab()
        
        # Tab mã hóa/giải mã
        self.create_encryption_tab()
        
        # Tab chữ ký số
        self.create_signature_tab()

    def create_styles(self):
        style = ttk.Style()
        style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'),
                      foreground='#2c3e50', padding=10)
        
        style.configure('Main.TFrame', background='#f5f6fa')
        
        style.configure('Tab.TFrame', padding=10)
        
        style.configure('Modern.TButton', font=('Helvetica', 10),
                      padding=10, background='#3498db')
        
        style.configure('Status.TLabel', font=('Helvetica', 9),
                      foreground='#7f8c8d', padding=5)
        
        style.configure('Section.TLabelframe', padding=10)
        style.configure('Section.TLabelframe.Label', font=('Helvetica', 11, 'bold'))

    def create_key_management_tab(self):
        key_frame = ttk.Frame(self.notebook, style='Tab.TFrame')
        self.notebook.add(key_frame, text='Quản lý khóa')
        
        # Frame cho các nút điều khiển
        control_frame = ttk.LabelFrame(key_frame, text="Thao tác",
                                     style='Section.TLabelframe')
        control_frame.pack(fill='x', padx=5, pady=5)
        
        # Nút tạo khóa với style mới
        ModernButton(control_frame, text="Tạo cặp khóa mới",
                    command=self.generate_keys).pack(pady=10)
        
        # Frame hiển thị khóa
        key_display_frame = ttk.LabelFrame(key_frame, text="Thông tin khóa",
                                         style='Section.TLabelframe')
        key_display_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Hiển thị khóa công khai
        ttk.Label(key_display_frame, text="Khóa công khai (Public Key):",
                 font=('Helvetica', 10, 'bold')).pack(pady=5)
        self.public_key_text = scrolledtext.ScrolledText(key_display_frame,
                                                       height=8, font=('Consolas', 10))
        self.public_key_text.pack(fill='x', padx=5, pady=5)
        
        # Hiển thị khóa riêng tư
        ttk.Label(key_display_frame, text="Khóa riêng tư (Private Key):",
                 font=('Helvetica', 10, 'bold')).pack(pady=5)
        self.private_key_text = scrolledtext.ScrolledText(key_display_frame,
                                                        height=8, font=('Consolas', 10))
        self.private_key_text.pack(fill='x', padx=5, pady=5)

    def create_encryption_tab(self):
        encrypt_frame = ttk.Frame(self.notebook)
        self.notebook.add(encrypt_frame, text='Mã hóa/Giải mã')
        
        # Vùng nhập tin nhắn
        ttk.Label(encrypt_frame, text="Tin nhắn:").pack(pady=5)
        self.message_text = scrolledtext.ScrolledText(encrypt_frame, height=5)
        self.message_text.pack(fill='x', padx=5)
        
        # Nút mã hóa/giải mã
        btn_frame = ttk.Frame(encrypt_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Mã hóa", 
                  command=self.encrypt_message).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Giải mã", 
                  command=self.decrypt_message).pack(side='left', padx=5)
        
        # Vùng kết quả
        ttk.Label(encrypt_frame, text="Kết quả:").pack(pady=5)
        self.result_text = scrolledtext.ScrolledText(encrypt_frame, height=5)
        self.result_text.pack(fill='x', padx=5)

    def create_signature_tab(self):
        sign_frame = ttk.Frame(self.notebook)
        self.notebook.add(sign_frame, text='Chữ ký số')
        
        # Vùng nhập tin nhắn
        ttk.Label(sign_frame, text="Tin nhắn cần ký:").pack(pady=5)
        self.sign_message_text = scrolledtext.ScrolledText(sign_frame, height=5)
        self.sign_message_text.pack(fill='x', padx=5)
        
        # Nút ký và xác thực
        btn_frame = ttk.Frame(sign_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Ký tin nhắn", 
                  command=self.sign_message).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Xác thực chữ ký", 
                  command=self.verify_signature).pack(side='left', padx=5)
        
        # Vùng chữ ký
        ttk.Label(sign_frame, text="Chữ ký:").pack(pady=5)
        self.signature_text = scrolledtext.ScrolledText(sign_frame, height=5)
        self.signature_text.pack(fill='x', padx=5)

    def generate_keys(self):
        try:
            # Tạo cặp khóa mới
            key = RSA.generate(2048)
            self.private_key = key
            self.public_key = key.publickey()
            
            # Hiển thị khóa
            self.public_key_text.delete(1.0, tk.END)
            self.public_key_text.insert(tk.END, self.public_key.export_key().decode())
            
            self.private_key_text.delete(1.0, tk.END)
            self.private_key_text.insert(tk.END, self.private_key.export_key().decode())
            
            messagebox.showinfo("Thành công", "Đã tạo cặp khóa mới!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tạo khóa: {str(e)}")

    def encrypt_message(self):
        if not self.public_key:
            messagebox.showerror("Lỗi", "Vui lòng tạo cặp khóa trước!")
            return
            
        try:
            message = self.message_text.get(1.0, tk.END).strip()
            cipher = PKCS1_OAEP.new(self.public_key)
            encrypted = cipher.encrypt(message.encode())
            
            # Chuyển sang base64 để hiển thị
            encrypted_b64 = base64.b64encode(encrypted).decode()
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, encrypted_b64)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mã hóa: {str(e)}")

    def decrypt_message(self):
        if not self.private_key:
            messagebox.showerror("Lỗi", "Vui lòng tạo cặp khóa trước!")
            return
            
        try:
            encrypted_b64 = self.result_text.get(1.0, tk.END).strip()
            encrypted = base64.b64decode(encrypted_b64)
            
            cipher = PKCS1_OAEP.new(self.private_key)
            decrypted = cipher.decrypt(encrypted)
            
            self.message_text.delete(1.0, tk.END)
            self.message_text.insert(tk.END, decrypted.decode())
            messagebox.showinfo("Thành công", "Đã giải mã tin nhắn!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể giải mã: {str(e)}")

    def sign_message(self):
        if not self.private_key:
            messagebox.showerror("Lỗi", "Vui lòng tạo cặp khóa trước!")
            return
            
        try:
            message = self.sign_message_text.get(1.0, tk.END).strip()
            h = SHA256.new(message.encode())
            signature = pkcs1_15.new(self.private_key).sign(h)
            
            # Chuyển sang base64 để hiển thị
            signature_b64 = base64.b64encode(signature).decode()
            
            self.signature_text.delete(1.0, tk.END)
            self.signature_text.insert(tk.END, signature_b64)
            messagebox.showinfo("Thành công", "Đã ký tin nhắn!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể ký: {str(e)}")

    def verify_signature(self):
        if not self.public_key:
            messagebox.showerror("Lỗi", "Vui lòng tạo cặp khóa trước!")
            return
            
        try:
            message = self.sign_message_text.get(1.0, tk.END).strip()
            signature_b64 = self.signature_text.get(1.0, tk.END).strip()
            signature = base64.b64decode(signature_b64)
            
            h = SHA256.new(message.encode())
            pkcs1_15.new(self.public_key).verify(h, signature)
            messagebox.showinfo("Thành công", "Chữ ký hợp lệ!")
        except (ValueError, TypeError):
            messagebox.showerror("Lỗi", "Chữ ký không hợp lệ!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi xác thực: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RSAApp(root)
    root.mainloop()
