import logging
logging.basicConfig(level=logging.DEBUG)

print("STEP 1: Starting script")

try:
    print("STEP 2: Importing app")
    from app import create_app

    print("STEP 3: Creating app")
    app = create_app()

    print("STEP 4: App created")

except Exception as e:
    import traceback
    print("💥 CRASH DURING INIT:")
    traceback.print_exc()
    raise

print("STEP 5: Starting server")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)