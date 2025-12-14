### SecureChat Man-in-the-Middle (MITM) tooling

About
-----
This directory contains a Burp Suite extension and companion MITM server used to demonstrate and exploit a Trust-On-First-Use (TOFU) style vulnerability in the SecureChat application.

Synopsis
--------
The SecureChat protocol flow (simplified):
1. Client sends a login request with a user ID and preferred algorithm.
2. Server replies with a session token, server public keys, and a signature over part of the session token. The client verifies the session signature.
3. After verifying the session signature, the client initiates key exchange by sending its public key and a signature of that key. The server verifies the signature and replies with a verification status. Both parties derive a shared secret.
4. The client sends an encrypted message plus a signature over the ciphertext. The server verifies the signature, decrypts, and reads the plaintext.
5. The server replies with an encrypted response plus a signature. The client verifies and decrypts.

Vulnerability
-------------
Two main weaknesses demonstrated here:
- Unauthenticated login: user IDs are chosen from available IDs without strong authentication, such as passwords.
- TOFU-like trust: when certificate pinning is bypassed, the client has no other way to verify the server identity. If an attacker captures the server's initial session reply, they can establish a MITM and compromise subsequent communication.

Prerequisites
-------------
- Frida
- Burp Suite (with a configurable proxy, custom hosts/ports)
- ADB
- An Android device or emulator (Android API 34 recommended) configured to use the Burp proxy and running Frida server
- Jython (for running the Burp extension in Burp's Python environment)
- Python 2 and Python 3

Setup
-----
1. In Burp Suite: open Settings → Extensions → Python environment and point to the Jython standalone JAR.
2. In Burp Suite → Extender → Extensions, click Add and load `burp_mitm_communicator.py` as a Python extension.

Running
-------
1. Start the Frida server on the Android device and use the provided Frida script to launch the target app.
2. Run the MITM server:

```bash
python mitm_server.py
```

Keep the MITM server running to receive and modify data forwarded by the Burp extension.

3. On the Android app, perform a login (use `group-2` as a user id).

How it works
------------
- `burp_mitm_communicator.py`: a Burp extension (Python 2) that scans HTTP requests/responses for specific URLs and forwards tagged messages to the MITM server over a socket. The extension can replace requests or responses based on the server's instructions.
- `mitm_server.py`: core MITM logic. It receives messages from the Burp extension, processes them according to header tags, and acts as a proxy that can simulate the client or server to manipulate or inspect traffic.
- `ec_curve.py`: contains ECDH-related operations (point addition, scalar multiplication). It uses projective coordinates internally and can return affine `(x, y)` coordinates when needed.

Files of interest
-----------------
- `burp_mitm_communicator.py` — Burp extension integration
- `mitm_server.py` — MITM server and manipulation logic
- `ec_curve.py` — elliptic curve / ECDH utilities

Notes
-----
This code is intended for research, education, and authorized security testing only. Do not use it against systems for which you do not have explicit permission.