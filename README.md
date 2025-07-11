# RSA Encryption and Digital Signature System

A graphical application for performing RSA encryption and digital signature operations, developed in Python using tkinter and pycryptodome libraries.

## Installation

1. Ensure Python 3.x is installed
2. Install required library:
```bash
pip install pycryptodome
```

## Application Overview

| Feature | Description | Input | Output | Security Level |
|---------|------------|--------|---------|----------------|
| **🔑 Key Management** |
| Generate Keys | Creates new RSA key pair | Click "Generate" button | - Public Key (PEM)<br>- Private Key (PEM) | High |
| View Keys | Display current keys | Automatic | PEM formatted keys | Medium |
| **🔒 Encryption/Decryption** |
| Encrypt Message | Encrypts text using public key | - Plain text message<br>- Public key | Base64 encrypted text | High |
| Decrypt Message | Decrypts text using private key | - Encrypted text (Base64)<br>- Private key | Original message | High |
| **✍️ Digital Signature** |
| Sign Message | Creates digital signature | - Message to sign<br>- Private key | Base64 signature | High |
| Verify Signature | Verifies message authenticity | - Original message<br>- Signature<br>- Public key | Verification result | High |

## User Interface Layout

| Tab | Components | Actions Available |
|-----|------------|------------------|
| **Key Management** | - Key generation button<br>- Public key display<br>- Private key display | - Generate new keys<br>- View keys<br>- Copy keys |
| **Encryption** | - Message input field<br>- Encrypt/Decrypt buttons<br>- Result display | - Enter message<br>- Encrypt message<br>- Decrypt message<br>- Copy results |
| **Digital Signature** | - Message input field<br>- Sign/Verify buttons<br>- Signature display | - Enter message<br>- Sign message<br>- Enter signature<br>- Verify signature |

## Process Flow Diagram

```
Key Generation ➔ RSA 2048-bit Keys
    │
    ├─➔ Encryption Flow
    │   ├─➔ Input Message
    │   ├─➔ Encrypt (Public Key)
    │   ├─➔ Base64 Encode
    │   └─➔ Display Result
    │
    └─➔ Signature Flow
        ├─➔ Input Message
        ├─➔ Generate Hash (SHA256)
        ├─➔ Sign (Private Key)
        └─➔ Display Signature
```

## Error Handling Matrix

| Operation | Possible Errors | Handling Method |
|-----------|----------------|-----------------|
| Key Generation | - Memory error<br>- System resource limits | - Error dialog<br>- Automatic cleanup |
| Encryption | - Message too long<br>- Invalid key format | - Size warning<br>- Format validation |
| Decryption | - Invalid Base64<br>- Wrong key | - Format check<br>- Clear error message |
| Signing | - Hash failure<br>- Key not available | - Integrity check<br>- Key validation |
| Verification | - Signature mismatch<br>- Corrupted data | - Verification status<br>- Data validation |

## Main Features

### 1. Key Management
- **Key Pair Generation**: Automatically generates RSA key pair (public and private keys) with 2048-bit length
- **Key Display**: Shows both public and private keys in PEM format

### 2. Encryption and Decryption
- **Encryption**: Uses public key to encrypt messages
- **Decryption**: Uses private key to decrypt messages
- **Format**: Encrypted results are converted to Base64 for easy display and copying

### 3. Digital Signature
- **Message Signing**: Uses private key to create digital signatures
- **Signature Verification**: Uses public key to verify message integrity

## How It Works

### Encryption and Decryption:
1. **Key Generation**:
   - System generates RSA key pair (public and private keys)
   - Public key is used for encryption
   - Private key is used for decryption

2. **Encryption Process**:
   - User enters the message to encrypt
   - System uses PKCS1_OAEP (Optimal Asymmetric Encryption Padding)
   - Result is converted to Base64 format

3. **Decryption Process**:
   - Enter encrypted text (in Base64 format)
   - System decrypts using private key
   - Displays decrypted result

### Digital Signature:
1. **Message Signing**:
   - User enters message to sign
   - System creates SHA256 hash of the message
   - Uses private key to sign the hash
   - Signature is converted to Base64 format

2. **Signature Verification**:
   - Enter original message and signature
   - System generates message hash
   - Uses public key to verify signature
   - Displays verification result

## Security Features

- Uses RSA with 2048-bit key length
- Implements PKCS1_OAEP for encryption
- Uses SHA256 for hashing
- Private key stored only in memory during runtime

## Technical Details

### Encryption Implementation:
```python
# Encryption using PKCS1_OAEP
cipher = PKCS1_OAEP.new(public_key)
encrypted = cipher.encrypt(message.encode())
```

### Digital Signature Implementation:
```python
# Signing using SHA256 and PKCS1_15
h = SHA256.new(message.encode())
signature = pkcs1_15.new(private_key).sign(h)
```

## Important Notes

- Keep private keys secret at all times
- Never share private keys over insecure channels
- Share public keys only with those who need to send encrypted messages or verify signatures
- Maximum message size for encryption is limited by RSA key length
- Base64 encoding is used for easy transfer of encrypted data and signatures

## Security Best Practices

1. **Key Management**:
   - Generate new keys for each session if needed
   - Never export private keys unless absolutely necessary
   - Use secure channels for key distribution

2. **Message Handling**:
   - Verify message integrity before decryption
   - Clear sensitive data from memory after use
   - Use appropriate message padding

3. **System Security**:
   - Keep the Python environment updated
   - Use trusted libraries only
   - Monitor system resources during operation

## Support and Contribution

Feel free to contribute to this project by:
- Reporting issues
- Suggesting improvements
- Adding new features
- Improving documentation

## License

This project is open-source and available under the MIT License.

## Application Screenshots

### 1. Main Application Window
```
+----------------------------------------+
|  RSA Encryption and Digital Signature   |
+----------------------------------------+
|  [Key Management][Encryption][Signature]|
|  +----------------------------------+  |
|  |           Active Tab             |  |
|  +----------------------------------+  |
+----------------------------------------+
```

### 2. Key Management Tab
```
+----------------------------------------+
|            Key Management              |
+----------------------------------------+
|   [Generate New Key Pair]              |
|                                        |
|   Public Key:                          |
|   +--------------------------------+   |
|   |-----BEGIN PUBLIC KEY-----      |   |
|   |MIIBIjANBgkqhkiG9w0BAQEFAAOC...|   |
|   |-----END PUBLIC KEY-----        |   |
|   +--------------------------------+   |
|                                        |
|   Private Key:                         |
|   +--------------------------------+   |
|   |-----BEGIN PRIVATE KEY----      |   |
|   |MIIEvgIBADANBgkqhkiG9w0BAQEF...|   |
|   |-----END PRIVATE KEY-----       |   |
|   +--------------------------------+   |
+----------------------------------------+
```

### 3. Encryption/Decryption Tab
```
+----------------------------------------+
|         Encryption/Decryption          |
+----------------------------------------+
|   Message:                             |
|   +--------------------------------+   |
|   |Enter your message here...      |   |
|   +--------------------------------+   |
|                                        |
|   [Encrypt ↓]        [Decrypt ↑]       |
|                                        |
|   Result:                              |
|   +--------------------------------+   |
|   |encrypted/decrypted text here...|   |
|   +--------------------------------+   |
+----------------------------------------+
```

### 4. Digital Signature Tab
```
+----------------------------------------+
|          Digital Signature             |
+----------------------------------------+
|   Message to Sign:                     |
|   +--------------------------------+   |
|   |Enter message to sign...        |   |
|   +--------------------------------+   |
|                                        |
|   [Sign Message]    [Verify Signature] |
|                                        |
|   Signature:                           |
|   +--------------------------------+   |
|   |Base64 signature appears here...|   |
|   +--------------------------------+   |
+----------------------------------------+
```

### 5. Success/Error Dialogs
```
+-----------------+    +----------------+
|    Success!     |    |     Error     |
+-----------------+    +----------------+
| Operation       |    | Unable to     |
| completed      |    | process:      |
| successfully!   |    | [Error msg]   |
|                 |    |               |
|      [OK]       |    |     [OK]      |
+-----------------+    +----------------+
```

### 6. Process Indicators
```
+----------------------------------+
|         Please Wait...           |
+----------------------------------+
|     [==========------] 65%       |
|  Generating RSA Key Pair...      |
+----------------------------------+
```

### 7. Verification Results
```
+----------------------------------+
|      Signature Verification      |
+----------------------------------+
|  ✓ Signature is valid            |
|  ✓ Message integrity confirmed   |
|  ✓ Sender authenticated         |
|                                  |
|            [Close]              |
+----------------------------------+
```

### 8. Key Operations Flow
```
    Generate Keys
         ↓
 [Public Key][Private Key]
    ↙           ↘
Encrypt       Sign Message
    ↓           ↓
Encrypted    Digital
Message     Signature
    ↓           ↓
Decrypt     Verify
    ↓           ↓
Original    Validation
Message     Result
```

### 9. Error Prevention Alerts
```
+----------------------------------------+
|            ⚠ Warning                   |
+----------------------------------------+
| This operation will:                    |
| - Generate new keys                     |
| - Replace existing keys                 |
| - Clear current data                    |
|                                        |
| Do you want to continue?               |
|                                        |
|    [Continue]        [Cancel]          |
+----------------------------------------+
```

### 10. Message Size Indicator
```
+----------------------------------------+
| Message Size: 256/256 bytes            |
| [■■■■■■■■■■■■■■■■■■■■] 100%          |
|                                        |
| ⚠ Maximum message size reached         |
+----------------------------------------+
```
