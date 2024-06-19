#BY K4N0
import os
import sys
import platform
import tempfile
import shutil
from glob import glob
from colorama import Fore, Style, init
from tkinter import Tk, filedialog
import hashlib
import datetime
import time
import subprocess
from Cryptodome.Cipher import AES, ChaCha20, Salsa20, DES3
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad
import random

init(autoreset=True)

BANNER = Fore.RED + """
⠀⠀⣿⠲⠤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣸⡏⠀⠀⠀⠉⠳⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣿⠀⠀⠀⠀⠀⠀⠀⠉⠲⣄⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢰⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠲⣄⠀⠀⠐⡰⠋⢙⣿⣦⡀⠀⠀⠀⠀⠀
⠸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣙⣦⣮⣤⡀⣸⣿⣿⣿⣆⠀⠀⠀⠀
⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⠀⣿⢟⣫⠟⠋⠀⠀⠀⠀
⠀⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣷⣷⣿⡁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⢹⣿⣿⣧⣿⣿⣆⡹⣖⡐⠠⠤⠠⠤
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢾⣿⣤⣿⣿⣿⡟⠹⣿⣿⣿⣿⣷⡀⠄⢀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣧⣴⣿⣿⣿⣿⠏⢧⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠈⢳⡀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡏⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⢳
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠸⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡇⢠⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠃⢸⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣼⢸⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠛⠻⠿⣿⣿⣿⡿⠿⠿⠿⠿⠿⢿⣿⣿⠏⠀
 _______        _____     _______   
|_   __ \      |_   _|   |_   __ \  
  | |__) |       | |       | |__) | 
  |  __ /        | |       |  ___/  
 _| |  \ \_  _  _| |_  _  _| |_     
|____| |___|(_)|_____|(_)|_____|    
                                    

"""

def generate_report(file_path, method, passes, log_details):
    report_path = file_path + ".deletion_report.txt"
    with open(report_path, "w") as report:
        report.write(f"Secure Deletion Technical Report\n")
        report.write(f"================================\n")
        report.write(f"File: {file_path}\n")
        report.write(f"Method: {method}\n")
        report.write(f"Number of Passes: {passes}\n")
        report.write(f"Date/Time: {datetime.datetime.now()}\n")
        report.write(f"Operating System: {platform.system()} {platform.release()}\n")
        try:
            report.write(f"File Size: {os.path.getsize(file_path)} bytes\n")
        except FileNotFoundError:
            report.write("File Size: File not found\n")
        report.write(f"\nAction Details:\n")
        for detail in log_details:
            report.write(f"{detail}\n")
    print(Fore.GREEN + f"Technical report generated: {report_path}")

def generate_general_report(operation, log_details):
    report_path = f"{operation}_report.txt"
    with open(report_path, "w") as report:
        report.write(f"Secure Operation Technical Report\n")
        report.write(f"=================================\n")
        report.write(f"Operation: {operation}\n")
        report.write(f"Date/Time: {datetime.datetime.now()}\n")
        report.write(f"Operating System: {platform.system()} {platform.release()}\n")
        report.write(f"\nAction Details:\n")
        for detail in log_details:
            report.write(f"{detail}\n")
    print(Fore.GREEN + f"Technical report for {operation} generated: {report_path}")

def generate_encryption_report(file_path, enc_method, key_size, iv, original_hash, encrypted_hash, log_details):
    report_path = file_path + ".encryption_report.txt"
    with open(report_path, "w") as report:
        report.write(f"Encryption Technical Report\n")
        report.write(f"===========================\n")
        report.write(f"File: {file_path}\n")
        report.write(f"Encryption Method: {enc_method}\n")
        report.write(f"Key Size: {key_size} bits\n")
        report.write(f"Initialization Vector (IV): {iv.hex()}\n")
        report.write(f"Original File Hash: {original_hash}\n")
        report.write(f"Encrypted File Hash: {encrypted_hash}\n")
        report.write(f"Date/Time: {datetime.datetime.now()}\n")
        report.write(f"Operating System: {platform.system()} {platform.release()}\n")
        report.write(f"\nAction Details:\n")
        for detail in log_details:
            report.write(f"{detail}\n")
    print(Fore.GREEN + f"Encryption report generated: {report_path}")

def hash_file(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def overwrite(file, size, pattern, log_details, pass_num):
    start_time = time.time()
    file.seek(0)
    file.write(pattern * (size // len(pattern)) + pattern[:size % len(pattern)])
    file.flush()
    os.fsync(file.fileno())
    duration = time.time() - start_time
    log_details.append(f"Pass {pass_num}: File overwritten with pattern {pattern.hex()} in {duration:.2f} seconds")
    file.seek(0)
    new_hash = hash_file(file.name)
    log_details.append(f"Pass {pass_num}: File hash after overwrite: {new_hash}")

def delete_temp_files(file_path, passes, log_details):
    temp_dirs = [tempfile.gettempdir(), os.path.dirname(file_path)]
    file_name = os.path.basename(file_path)

    if platform.system() == "Windows":
        temp_patterns = [
            os.path.join(tempfile.gettempdir(), f"~{file_name}"),
            os.path.join(tempfile.gettempdir(), f"{file_name}.tmp"),
            os.path.join(os.path.dirname(file_path), f"~{file_name}"),
            os.path.join(os.path.dirname(file_path), f"{file_name}.tmp")
        ]
    else:
        temp_patterns = [
            os.path.join(tempfile.gettempdir(), f".{file_name}"),
            os.path.join(tempfile.gettempdir(), f"{file_name}~"),
            os.path.join(os.path.dirname(file_path), f".{file_name}"),
            os.path.join(os.path.dirname(file_path), f"{file_name}~")
        ]

    for pattern in temp_patterns:
        for temp_file in glob(pattern):
            try:
                if os.path.isfile(temp_file):
                    log_details.append(f"Found temporary file: {temp_file}")
                    confirm = input(Fore.GREEN + "Do you want to process this temporary file? (y/n): ").strip().lower()
                    if confirm == 'y':
                        file_size = os.path.getsize(temp_file)
                        with open(temp_file, 'rb+') as f:
                            for i in range(passes):
                                pattern = os.urandom(1)  # Use random data for each pass
                                overwrite(f, file_size, pattern, log_details, i+1)
                        log_details.append(f"Temporary file {temp_file} securely processed.")
                        print(Fore.GREEN + f"Temporary file securely processed: {temp_file}")
            except Exception as e:
                log_details.append(f"Error processing temporary file {temp_file}: {e}")
                print(Fore.RED + f"Error processing temporary file: {temp_file}, {e}")

def secure_delete(file_path, passes, method, generate_report_flag, delete_file_flag, log_details):
    try:
        if not os.path.isfile(file_path):
            log_details.append(f"File not found: {file_path}")
            print(Fore.RED + "File not found.")
            return

        initial_hash = hash_file(file_path)
        log_details.append(f"Initial Hash: {initial_hash}")
        
        file_size = os.path.getsize(file_path)
        
        with open(file_path, 'rb+') as f:
            log_details.append(f"File size: {file_size} bytes")
            log_details.append(f"Starting file overwrite...")
            for i in range(passes):
                if method == "DoD 5220.22-M":
                    if i % 3 == 0:
                        pattern = b'\x00'
                    elif i % 3 == 1:
                        pattern = b'\xFF'
                    else:
                        pattern = os.urandom(1)
                elif method == "Gutmann":
                    pattern = os.urandom(1)
                elif method == "Schneier":
                    pattern = os.urandom(1)
                elif method == "Write Zero":
                    pattern = b'\x00'
                elif method == "Write Random":
                    pattern = os.urandom(1)
                overwrite(f, file_size, pattern, log_details, i+1)

        final_hash = hash_file(file_path)
        log_details.append(f"Final Hash: {final_hash}")
        
        log_details.append(f"File processing completed.")
        print(Fore.GREEN + "File securely processed.")
        
        delete_temp_files(file_path, passes, log_details)
        
        if generate_report_flag:
            generate_report(file_path, method, passes, log_details)
        
        if delete_file_flag:
            os.remove(file_path)
            log_details.append(f"Original file deleted.")
            print(Fore.GREEN + "File securely deleted.")
        
    except Exception as e:
        log_details.append(f"Error processing file: {e}")
        print(Fore.RED + f"Error processing file: {e}")

def secure_overwrite(operation_type):
    log_details = []
    try:
        if operation_type == "unused_space":
            result = subprocess.run(['sudo', 'sfill', '-v'], capture_output=True, text=True)
        elif operation_type == "swap_space":
            subprocess.run(['sudo', 'swapoff', '-a'], capture_output=True, text=True)
            result = subprocess.run(['sudo', 'sswap', '-v'], capture_output=True, text=True)
            subprocess.run(['sudo', 'swapon', '-a'], capture_output=True, text=True)
        elif operation_type == "unused_memory":
            result = subprocess.run(['sudo', 'smem', '-v'], capture_output=True, text=True)
        
        log_details.append(result.stdout)
        print(Fore.GREEN + result.stdout)
        generate_general_report(operation_type.replace("_", " ").title(), log_details)
    except Exception as e:
        log_details.append(f"Error during secure overwrite of {operation_type.replace('_', ' ')}: {e}")
        print(Fore.RED + f"Error during secure overwrite of {operation_type.replace('_', ' ')}: {e}")

def encrypt_file(file_path, method, log_details):
    key_size = 256  # Default to 256-bit key size
    key = get_random_bytes(key_size // 8)  # Generate key of appropriate size

    if method == "DES3":
        key_size = 192
        iv = get_random_bytes(8)  # Initialization vector for DES3
    else:
        iv = get_random_bytes(16)  # Initialization vector for AES, ChaCha20, Salsa20

    if method == "AES":
        cipher = AES.new(key, AES.MODE_CBC, iv)
    elif method == "ChaCha20":
        cipher = ChaCha20.new(key=key)
    elif method == "Salsa20":
        cipher = Salsa20.new(key=key)
    elif method == "DES3":
        cipher = DES3.new(key, DES3.MODE_CBC, iv)
    else:
        print(Fore.RED + "Invalid encryption method.")
        return

    original_hash = hash_file(file_path)
    with open(file_path, "rb") as f:
        plaintext = f.read()
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    
    with open(file_path, "wb") as f:
        f.write(ciphertext)
    
    encrypted_hash = hash_file(file_path)

    log_details.append(f"Encryption Method: {method}")
    log_details.append(f"Key Size: {key_size} bits")
    log_details.append(f"Initialization Vector: {iv.hex()}")
    log_details.append(f"Original File Hash: {original_hash}")
    log_details.append(f"Encrypted File Hash: {encrypted_hash}")
    print(Fore.GREEN + f"File encrypted using {method}.")
    
    return key_size, iv, original_hash, encrypted_hash

def select_file():
    root = Tk()
    root.withdraw()  # Hide the main Tkinter window
    file_path = filedialog.askopenfilename()
    root.destroy()
    return file_path

def print_initial_menu():
    print(Fore.CYAN + Style.BRIGHT + BANNER)
    print(Fore.CYAN + Style.BRIGHT + "=====================")
    print(Fore.CYAN + Style.BRIGHT + "  Archive Killer  ")
    print(Fore.CYAN + Style.BRIGHT + "=====================")
    print(Fore.YELLOW + "1. Just kill this thing")
    print(Fore.YELLOW + "2. Overwrite Method")
    print(Fore.YELLOW + "3. Encrypt Method")
    print(Fore.YELLOW + "4. Encrypt & Overwrite")
    print(Fore.YELLOW + "5. Exit")
    print(Fore.CYAN + Style.BRIGHT + "=====================")

def print_overwrite_menu():
    print(Fore.CYAN + Style.BRIGHT + "=====================")
    print(Fore.CYAN + Style.BRIGHT + "  Overwrite Methods  ")
    print(Fore.CYAN + Style.BRIGHT + "=====================")
    print(Fore.YELLOW + "1. Overwrite")
    print(Fore.YELLOW + "2. Overwrite and generate report")
    print(Fore.YELLOW + "3. Overwrite and delete")
    print(Fore.YELLOW + "4. Overwrite, delete and generate report")
    print(Fore.CYAN + Style.BRIGHT + "=====================")

def print_encrypt_menu():
    print(Fore.CYAN + Style.BRIGHT + "=====================")
    print(Fore.CYAN + Style.BRIGHT + "  Encryption Methods  ")
    print(Fore.CYAN + Style.BRIGHT + "=====================")
    print(Fore.YELLOW + "1. Encrypt")
    print(Fore.YELLOW + "2. Encrypt and generate report")
    print(Fore.YELLOW + "3. Encrypt and delete")
    print(Fore.YELLOW + "4. Encrypt, delete and generate report")
    print(Fore.CYAN + Style.BRIGHT + "=====================")

def print_encryption_methods():
    print(Fore.CYAN + Style.BRIGHT + "=====================")
    print(Fore.CYAN + Style.BRIGHT + "  Choose Encryption Method  ")
    print(Fore.CYAN + Style.BRIGHT + "=====================")
    print(Fore.YELLOW + "1. AES")
    print(Fore.YELLOW + "2. ChaCha20")
    print(Fore.YELLOW + "3. Salsa20")
    print(Fore.YELLOW + "4. DES3")
    print(Fore.CYAN + Style.BRIGHT + "=====================")

def print_encrypt_overwrite_menu():
    print(Fore.CYAN + Style.BRIGHT + "=====================")
    print(Fore.CYAN + Style.BRIGHT + "  Encrypt & Overwrite  ")
    print(Fore.CYAN + Style.BRIGHT + "=====================")
    print(Fore.YELLOW + "1. Encrypt & Overwrite")
    print(Fore.YELLOW + "2. Encrypt & Overwrite and generate report")
    print(Fore.YELLOW + "3. Encrypt & Overwrite and delete")
    print(Fore.YELLOW + "4. Encrypt & Overwrite, delete and generate report")
    print(Fore.CYAN + Style.BRIGHT + "=====================")

def print_method_menu():
    print(Fore.CYAN + Style.BRIGHT + "=====================")
    print(Fore.CYAN + Style.BRIGHT + "  Overwrite Methods  ")
    print(Fore.CYAN + Style.BRIGHT + "=====================")
    print(Fore.YELLOW + "1. DoD 5220.22-M")
    print(Fore.YELLOW + "2. Gutmann")
    print(Fore.YELLOW + "3. Schneier")
    print(Fore.YELLOW + "4. Write Zero")
    print(Fore.YELLOW + "5. Write Random")
    print(Fore.CYAN + Style.BRIGHT + "=====================")

def random_encrypt_overwrite_delete(file_path):
    enc_methods = ["AES", "ChaCha20", "Salsa20", "DES3"]
    overwrite_methods = ["DoD 5220.22-M", "Gutmann", "Schneier", "Write Zero", "Write Random"]
    
    enc_method = random.choice(enc_methods)
    overwrite_method = random.choice(overwrite_methods)
    passes = 3 if overwrite_method == "DoD 5220.22-M" else (35 if overwrite_method == "Gutmann" else 7)
    
    log_details = []
    confirm = input(Fore.GREEN + f"Are you sure you want to process the file {file_path}? (y/n): ").strip().lower()
    if confirm != 'y':
        log_details.append(f"Operation canceled by user.")
        print(Fore.RED + "Operation canceled by user.")
        return
    
    print(Fore.YELLOW + f"Encryption method chosen: {enc_method}")
    key_size, iv, original_hash, encrypted_hash = encrypt_file(file_path, enc_method, log_details)
    print(Fore.YELLOW + f"Overwrite method chosen: {overwrite_method}")
    secure_delete(file_path, passes, overwrite_method, False, True, log_details)

def main():
    while True:
        print_initial_menu()
        initial_choice = input(Fore.GREEN + "Choose an option: ")

        if initial_choice == '1':  # Just kill this thing
            file_path = select_file()
            if not file_path:
                print(Fore.RED + "No file selected.")
                continue
            random_encrypt_overwrite_delete(file_path)

        elif initial_choice == '2':  # Overwrite Method
            while True:
                print_overwrite_menu()
                main_choice = input(Fore.GREEN + "Choose an option: ")

                if main_choice == '1':
                    generate_report_flag = False
                    delete_file_flag = False
                elif main_choice == '2':
                    generate_report_flag = True
                    delete_file_flag = False
                elif main_choice == '3':
                    generate_report_flag = False
                    delete_file_flag = True
                elif main_choice == '4':
                    generate_report_flag = True
                    delete_file_flag = True
                else:
                    print(Fore.RED + "Invalid option, please try again.")
                    continue

                file_path = select_file()
                if not file_path:
                    print(Fore.RED + "No file selected.")
                    continue

                print_method_menu()
                method_choice = input(Fore.GREEN + "Choose a method: ")

                if method_choice == '1':
                    method = "DoD 5220.22-M"
                    passes = 3
                elif method_choice == '2':
                    method = "Gutmann"
                    passes = 35
                elif method_choice == '3':
                    method = "Schneier"
                    passes = 7
                elif method_choice == '4':
                    method = "Write Zero"
                    passes = 1
                elif method_choice == '5':
                    method = "Write Random"
                    passes = 1
                else:
                    print(Fore.RED + "Invalid option, please try again.")
                    continue

                log_details = []
                secure_delete(file_path, passes, method, generate_report_flag, delete_file_flag, log_details)
                break

        elif initial_choice == '3':  # Encrypt Method
            while True:
                print_encrypt_menu()
                main_choice = input(Fore.GREEN + "Choose an option: ")

                if main_choice == '1':
                    generate_report_flag = False
                    delete_file_flag = False
                elif main_choice == '2':
                    generate_report_flag = True
                    delete_file_flag = False
                elif main_choice == '3':
                    generate_report_flag = False
                    delete_file_flag = True
                elif main_choice == '4':
                    generate_report_flag = True
                    delete_file_flag = True
                else:
                    print(Fore.RED + "Invalid option, please try again.")
                    continue

                file_path = select_file()
                if not file_path:
                    print(Fore.RED + "No file selected.")
                    continue

                print_encryption_methods()
                enc_method_choice = input(Fore.GREEN + "Choose an encryption method: ")

                if enc_method_choice == '1':
                    enc_method = "AES"
                elif enc_method_choice == '2':
                    enc_method = "ChaCha20"
                elif enc_method_choice == '3':
                    enc_method = "Salsa20"
                elif enc_method_choice == '4':
                    enc_method = "DES3"
                else:
                    print(Fore.RED + "Invalid option, please try again.")
                    continue

                log_details = []
                key_size, iv, original_hash, encrypted_hash = encrypt_file(file_path, enc_method, log_details)

                if delete_file_flag:
                    os.remove(file_path)
                    log_details.append(f"File securely deleted.")
                    print(Fore.GREEN + "File securely deleted.")
                
                if generate_report_flag:
                    generate_encryption_report(file_path, enc_method, key_size, iv, original_hash, encrypted_hash, log_details)

                break

        elif initial_choice == '4':  # Encrypt & Overwrite
            while True:
                print_encrypt_overwrite_menu()
                main_choice = input(Fore.GREEN + "Choose an option: ")

                if main_choice == '1':
                    generate_report_flag = False
                    delete_file_flag = False
                elif main_choice == '2':
                    generate_report_flag = True
                    delete_file_flag = False
                elif main_choice == '3':
                    generate_report_flag = False
                    delete_file_flag = True
                elif main_choice == '4':
                    generate_report_flag = True
                    delete_file_flag = True
                else:
                    print(Fore.RED + "Invalid option, please try again.")
                    continue

                file_path = select_file()
                if not file_path:
                    print(Fore.RED + "No file selected.")
                    continue

                confirm = input(Fore.GREEN + f"Are you sure you want to process the file {file_path}? (y/n): ").strip().lower()
                if confirm != 'y':
                    print(Fore.RED + "Operation canceled by user.")
                    continue

                print_encryption_methods()
                enc_method_choice = input(Fore.GREEN + "Choose an encryption method: ")

                if enc_method_choice == '1':
                    enc_method = "AES"
                elif enc_method_choice == '2':
                    enc_method = "ChaCha20"
                elif enc_method_choice == '3':
                    enc_method = "Salsa20"
                elif enc_method_choice == '4':
                    enc_method = "DES3"
                else:
                    print(Fore.RED + "Invalid option, please try again.")
                    continue

                log_details = []
                key_size, iv, original_hash, encrypted_hash = encrypt_file(file_path, enc_method, log_details)

                print_method_menu()
                method_choice = input(Fore.GREEN + "Choose a method: ")

                if method_choice == '1':
                    method = "DoD 5220.22-M"
                    passes = 3
                elif method_choice == '2':
                    method = "Gutmann"
                    passes = 35
                elif method_choice == '3':
                    method = "Schneier"
                    passes = 7
                elif method_choice == '4':
                    method = "Write Zero"
                    passes = 1
                elif method_choice == '5':
                    method = "Write Random"
                    passes = 1
                else:
                    print(Fore.RED + "Invalid option, please try again.")
                    continue

                secure_delete(file_path, passes, method, generate_report_flag, delete_file_flag, log_details)

                if generate_report_flag:
                    generate_encryption_report(file_path, enc_method, key_size, iv, original_hash, encrypted_hash, log_details)
                    
                break

        elif initial_choice == '5':
            print(Fore.GREEN + "Exiting the program...")
            sys.exit()

        else:
            print(Fore.RED + "Invalid option, please try again.")

if __name__ == "__main__":
    main()
