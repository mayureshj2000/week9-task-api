print("STEP 1: Starting run.py")

try:
    from app import create_app
    print("STEP 2: Imported create_app")

    app = create_app()
    print("STEP 3: App created")

except Exception as e:
    import traceback
    print("💥 CRASH DURING INIT:")
    traceback.print_exc()
    raise

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    print(f"STEP 4: Running on port {port}")
    app.run(host="0.0.0.0", port=port)