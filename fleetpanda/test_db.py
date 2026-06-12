from app.database.session import engine
from sqlalchemy import text

with engine.connect() as conn:

    result = conn.execute(text("SELECT @@VERSION"))

    print(result.fetchone())