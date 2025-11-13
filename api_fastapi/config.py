import os

SECRET_KEY = os.getenv("SECRET_KEY", "dsworkout");
ALGORITHM = 'HS256'