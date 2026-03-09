import hashlib

password = input("Masukkan password: ")
md5 = hashlib.md5(password.encode()).hexdigest()
print(f"MD5: {md5}")