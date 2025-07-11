#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/rsa.h>
#include <openssl/pem.h>
#include <openssl/sha.h>
#include <openssl/err.h>

// Function to generate key pair
void generate_key_pair() {
    RSA *rsa = RSA_new();
    BIGNUM *bne = BN_new();
    BN_set_word(bne, RSA_F4);
    RSA_generate_key_ex(rsa, 2048, bne, NULL);

    // Save private key
    FILE *private_key_file = fopen("private.pem", "wb");
    PEM_write_RSAPrivateKey(private_key_file, rsa, NULL, NULL, 0, NULL, NULL);
    fclose(private_key_file);

    // Save public key
    FILE *public_key_file = fopen("public.pem", "wb");
    PEM_write_RSAPublicKey(public_key_file, rsa);
    fclose(public_key_file);

    RSA_free(rsa);
    BN_free(bne);
}

// Function to create message digest (hash)
void create_digest(const unsigned char *message, size_t message_len, unsigned char *digest) {
    SHA256_CTX sha256;
    SHA256_Init(&sha256);
    SHA256_Update(&sha256, message, message_len);
    SHA256_Final(digest, &sha256);
}

// Function to sign a message
unsigned char* sign_message(const char *message, size_t *signature_len) {
    // Read private key
    FILE *private_key_file = fopen("private.pem", "rb");
    RSA *rsa = PEM_read_RSAPrivateKey(private_key_file, NULL, NULL, NULL);
    fclose(private_key_file);

    // Create digest
    unsigned char digest[SHA256_DIGEST_LENGTH];
    create_digest((unsigned char*)message, strlen(message), digest);

    // Sign the digest
    unsigned char *signature = malloc(RSA_size(rsa));
    RSA_private_encrypt(SHA256_DIGEST_LENGTH, digest, signature, rsa, RSA_PKCS1_PADDING);
    *signature_len = RSA_size(rsa);

    RSA_free(rsa);
    return signature;
}

// Function to verify signature
int verify_signature(const char *message, const unsigned char *signature, size_t signature_len) {
    // Read public key
    FILE *public_key_file = fopen("public.pem", "rb");
    RSA *rsa = PEM_read_RSAPublicKey(public_key_file, NULL, NULL, NULL);
    fclose(public_key_file);

    // Decrypt signature
    unsigned char decrypted[SHA256_DIGEST_LENGTH];
    RSA_public_decrypt(signature_len, signature, decrypted, rsa, RSA_PKCS1_PADDING);

    // Create digest of original message
    unsigned char digest[SHA256_DIGEST_LENGTH];
    create_digest((unsigned char*)message, strlen(message), digest);

    // Compare decrypted signature with digest
    int result = memcmp(decrypted, digest, SHA256_DIGEST_LENGTH) == 0;

    RSA_free(rsa);
    return result;
}

int main() {
    // Initialize OpenSSL
    OpenSSL_add_all_algorithms();
    ERR_load_crypto_strings();

    // Generate key pair
    printf("Generating key pair...\n");
    generate_key_pair();
    printf("Keys generated successfully!\n\n");

    // Test message
    const char *message = "Hello, this is a test message!";
    printf("Original message: %s\n", message);

    // Sign message
    size_t signature_len;
    unsigned char *signature = sign_message(message, &signature_len);
    printf("Message signed successfully!\n");

    // Verify signature
    if (verify_signature(message, signature, signature_len)) {
        printf("Signature verification successful!\n");
    } else {
        printf("Signature verification failed!\n");
    }

    // Test with tampered message
    const char *tampered_message = "Hello, this is a modified message!";
    if (verify_signature(tampered_message, signature, signature_len)) {
        printf("Warning: Tampered message verified!\n");
    } else {
        printf("Security working: Tampered message detected!\n");
    }

    // Cleanup
    free(signature);
    EVP_cleanup();
    ERR_free_strings();

    return 0;
}
