import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@127.0.0.1/try_clustering'  # Sesuaikan dengan kredensial database Anda
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)  # Digunakan untuk keamanan (misalnya, untuk session)
