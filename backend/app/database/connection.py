from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment")
engine = create_engine(DATABASE_URL, echo=True)


if __name__ == "__main__":
    from sqlalchemy import text

    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print(result.fetchone())