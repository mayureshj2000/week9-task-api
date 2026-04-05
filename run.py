import logging
logging.basicConfig(level=logging.DEBUG)
from app import create_app
from app.extensions import db

app = create_app()

with app.app_context():
    try:
        db.create_all()
        print("✅ DB Created")
    except Exception as e:
        print("❌ DB Error:", e)

print("🚀 Starting app...")

try:
    from app import create_app
    print("✅ Imported create_app")

    app = create_app()
    print("✅ App created")

except Exception as e:
    import traceback
    print("💥 CRASH DURING INIT:")
    traceback.print_exc()
    raise

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    print(f"🚀 Running on port {port}")
    app.run(host="0.0.0.0", port=port)