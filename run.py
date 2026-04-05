import logging
logging.basicConfig(level=logging.DEBUG)

print("STEP 1: Starting script")

try:
    from app import create_app
    from app.extensions import db

    app = create_app()
    print("✅ App created")

    with app.app_context():
        db.create_all()
        print("✅ DB Created")

except Exception as e:
    import traceback
    print("💥 CRASH DURING INIT:")
    traceback.print_exc()
    raise

print("STEP 5: Starting server")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)