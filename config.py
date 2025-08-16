import os

class Config:
    SECRET_KEY = os.getenv("0eda34defbecee982d6aac7c272c74d6ccfad5f6051fc6d30ae18b08782dcc25", "default-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:Tieungoandong@@3979@db.ywvgigmodfrnovbgraqm.supabase.co:5432/postgres")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
