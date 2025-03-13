from werkzeug.security import generate_password_hash

print("Hash Yenyen:", generate_password_hash("yensel123"))
print("Hash Admin:", generate_password_hash("admin123"))  # Cambia "admin123" por la contraseña real
