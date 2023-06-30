import hashlib


class MyClass:
    __privateuser = "kalpataru"
    __privatepass = "12345"
    username = str(hashlib.sha256(__privateuser.encode()).hexdigest())
    password = str(hashlib.sha256(__privatepass.encode()).hexdigest())
