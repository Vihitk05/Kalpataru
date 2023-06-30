import hashlib


class MyClass:
    __privateuser = "admin"
    __privatepass = "1234"
    username = str(hashlib.sha256(__privateuser.encode()).hexdigest())
    password = str(hashlib.sha256(__privatepass.encode()).hexdigest())
