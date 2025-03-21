import os 



DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://advinha_db_user:g5HLgah5N152Oy6R5PPYGS9GkdTSQJyY@dpg-cvemilt2ng1s73chu6g0-a.oregon-postgres.render.com/advinha_db")

class Config:
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "6519b6c6f110a95fa342857c95879d4fa26400fcfb052895ce79e83a569da9c1")
