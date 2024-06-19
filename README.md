# RestInPeace (R.I.P)

RestInPeace is a file deletion script designed to securely delete files. Utilizing various encryption and overwrite methods, R.I.P ensures that deleted files are irrecoverable.

## Features

- **Secure File Deletion**: Delete files using advanced encryption and overwrite techniques.
- **Multiple Encryption Methods**: Supports AES, ChaCha20, Salsa20, and DES3 encryption methods.
- **Multiple Overwrite Methods**: Supports DoD 5220.22-M, Gutmann, Schneier, Write Zero, and Write Random overwrite methods.
- **Detailed Reports**: Generate comprehensive reports detailing the deletion process.
- **User-Friendly Interface**: Interactive menu-driven interface with colorful outputs.

## Menu Options

1. **Just kill this thing**: Randomly selects encryption and overwrite methods to delete the file securely.
2. **Overwrite Method**: Choose from various overwrite methods to securely delete the file.
3. **Encrypt Method**: Choose from various encryption methods to encrypt the file before deletion.
4. **Encrypt & Overwrite**: Combine encryption and overwrite methods for maximum security.

## Overwrite Methods

- **DoD 5220.22-M**: Three-pass overwrite method.
- **Gutmann**: 35-pass overwrite method.
- **Schneier**: Seven-pass overwrite method.
- **Write Zero**: Single-pass overwrite with zeros.
- **Write Random**: Single-pass overwrite with random data.

## Encryption Methods

- **AES**: Advanced Encryption Standard with 256-bit key size.
- **ChaCha20**: Stream cipher with 256-bit key size.
- **Salsa20**: Stream cipher with 256-bit key size.
- **DES3**: Triple DES encryption with 192-bit key size.

## Installation

### Prerequisites

- Python 3.x
- Tkinter
- PyCryptodome

### Installing Dependencies

```bash
pip install -r requirements.txt
```
### Running the Program

```bash
sudo python3 rip.py
