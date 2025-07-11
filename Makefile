CC=gcc
CFLAGS=-Wall -lcrypto

all: digital_signature

digital_signature: digital_signature.c
	$(CC) -o digital_signature digital_signature.c $(CFLAGS)

clean:
	rm -f digital_signature *.pem
