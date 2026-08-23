# backend/test_db.py
# to test your database connection and pgvector extension

from app.core.db import init_db, engine
from sqlalchemy import text

print("📡 Initializing database & pgvector extension...")
try:
    init_db()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT extname FROM pg_extension WHERE extname = 'vector';")).fetchone()
        if result:
            print("✅ Database connected & 'pgvector' extension confirmed active!")
        else:
            print("⚠️ Database connected, but 'vector' extension is not active.")
except Exception as e:
    print(f"❌ Database initialization failed: {e}")