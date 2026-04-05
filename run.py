import logging
from app import create_app
logging.basicConfig(level=logging.DEBUG)


print("STEP 1: Starting script")

try:
    print("STEP 2: Importing app")
    from app import create_app
    from app.extensions import db

    print("STEP 3: Creating app")
    app = create_app()

    print("STEP 4: App created")

    with app.app_context():
        print("STEP 5: Creating DB")
        db.create_all()
        print("STEP 6: DB created")

except Exception as e:
    import traceback
    print("💥 CRASH DURING INIT:")
    traceback.print_exc()
    raise

print("STEP 7: Starting server")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Running on port {port}")
    app.run(host="0.0.0.0", port=port)