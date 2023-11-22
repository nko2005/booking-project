from werkzeug.security import generate_password_hash

passwords = ["password1", "password2", "password3"]

hashed_passwords = []

for password in passwords:
    hashed_password = generate_password_hash(password)
    hashed_passwords.append(hashed_password)

for password in hashed_passwords:
    print(password)
