print("Starting app...")

from app import create_app

print("Imported create_app")

app = create_app()

print("App created")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    print(f"Running on port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)