import os
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@postgres_db:5432/ecommerce_db")
