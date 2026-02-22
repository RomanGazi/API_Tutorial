from flask import Flask, jsonify, request
import logging

app = Flask(__name__)

books = [
    {"id": 1, "name": "Uncle Tom's Cabin", "price": 9.50},
    {"id": 2, "name": "Meditations", "price": 15.75}
]

logging.basicConfig(
    filename="logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

API_KEY = "12345"
book_id_counter = len(books) + 1

@app.before_request
def log_request_info():
    print("Method:", request.method)
    print("URL:", request.url)

@app.before_request
def check_api_key():
    if request.endpoint in ["get_book_list", "add_book"] and request.method in ["GET", "POST"]:
        print("Checking API key for endpoint:", request.endpoint)
        key = request.headers.get("x-api-key")
        if key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        
@app.after_request
def log_response_info(response):
    print("Status:", response.status)
    return response

@app.route("/health", methods=["GET"])
def health_check(): 
    return jsonify({"status": "ok"}), 200

@app.route("/book_list", methods=["GET"])
def get_book_list():
    return jsonify(books), 200

@app.route("/book_list/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((book for book in books if book["id"] == book_id), None)
    if book:
        return jsonify(book), 200
    else:
        return jsonify({"error": "Book not found"}), 404

@app.route("/book_list", methods=["POST"])
def add_book():
    global book_id_counter
    new_book = request.get_json()
    new_book = {
        "id": book_id_counter,
        "name": new_book["name"],
        "price": new_book["price"]
    }
    book_id_counter += 1
    books.append(new_book)
    return jsonify(new_book), 201

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)