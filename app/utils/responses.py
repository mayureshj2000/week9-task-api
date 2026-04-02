from flask import jsonify

def success_response(data, status_code=200):
    return jsonify({"status": "success", "data": data}), status_code

def error_response(message, status_code=400, errors=None):
    payload = {"status": "error", "message": message}
    if errors:
        payload["errors"] = errors
    return jsonify(payload), status_code