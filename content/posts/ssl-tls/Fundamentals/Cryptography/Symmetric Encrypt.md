---
title: Symmetric Encrypt
description:
date: 2026-01-27
image:
categories:
  - ssl/tls
tags:
  - symmetric
draft: false
---
---
## 1. Principle

Imagine you have a **safes**

- **Encryption:** You drop documents to safes, use `Key A` for locked
	
- **Decryption:** Receiver want to take documents, they require have exactly `Key A` to open

### Technique

- **Plaintext:** Original Data (password, credit number,...)
	
- **Ciphertext**: The Data has been scrambled, can't understand
	
- **Secret Key:** String Data use to scramble and restore

### Recipe

- Plaintext + Key = Ciphertext
	
- Ciphertext + Key = Plaintext

## 2. Why SSL/TLS need Symmetric Encryption ?

May you ask: *"Why not use Asymmetric Encryption for security, no need to worry about `Key`"*

This answer lies in **Performance**

- **Speed:** Symmetric Encrypt so speed, Modern CPUs (like Intel, AMD) even have their own hardware instruction set (AES - NI) to handle this in a snap
	
- **Resource**: It consumes significantly less CPU and RAM than Symmetric Encryption

### In SSL/TLS:

- When you download a file about 1GB throught HTTPS

	1. System only use asymmetric encryption in the first few miliseconds to agree on the key
		
	2. After, the entire 1GB of data was encrypted using **Symmetric Encryption** to ensure fast downloads without overloading the server
		
## 3. Fatal Weakness

- If I want to send confidential data for you, I have to sent you the `Key`
	
- If I send `Key` via email/chat, and a hacker intercepts the `Key`, all my data will be exposed
	
- If I meet  you to give you the USB containing the `Key` -> That's not feasible with global internet

### Solution in SSL/TLS

Use the key exchange algorithm (like [Diffie-Hellman](posts/diffie-hellman) or [RSA](posts/rsa)) during the Handshake process allows both parties to generate a **Symmetric Key** without send direct the `Key` over network

## 4. Popular Algorithms

### A. AES (Advanced Encryption Standard)

- Is it currently the most popular and security algorithm
	
- **Key length:** `128-bit` or `256-bit` (AES-128, AES-256)
	
	- *Note: AES-128 is slightly faster, AES-256 safer, but currently AES-128 still extremely safe*

### B. ChaCha20 - New Star

- Strongly supported by Google
	
- **Advantage:** Extremely fast on mobile devices, or CPU older version do not have hardware support for AES
	
- Often used in conjounction with Poly1305 (ChaCha20-Poly1305)

### C. 3DES (Triple DES) - Dead

- It is old technology. Very slow and no longer safe
	
- If you see your server still enable 3DES, disable it immediately. Modern browsers will warning "Not Secure" or block this connect

## 5. Block Ciphers & Stream Ciphers

**Symmetric Encryption** handle data via 2 ways

### A. Stream Ciphers

Encrypt each bite/byte (like flowing water)

### B. Block Ciphers

Cut data to fixed blocks (ex: `128-bit`) next encrypt each block (ex: AES)

## Canvas: [Symmetric Encrypt (canvas).canvas](posts/symmetric-encrypt-canvascanvas)







