import os
from dotenv import load_dotenv

load_dotenv()

class Environment:
    BASE_URL = os.getenv("KINOPOISK_URL", "https://hd.kinopoisk.ru/")
    API_URL = os.getenv("KINOPOISK_API_URL", "https://kinopoiskapiunofficial.tech/")
