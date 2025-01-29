from database import engine

try:
    with engine.connect() as connection:
        print("✅ Successfully connected to MySQL!")
except Exception as e:
    print("❌ Error connecting to MySQL:", e)
