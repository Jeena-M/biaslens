from flask import Flask, jsonify

app = Flask(__name__) # app = instance of the Flask application

@app.route('/health', methods=['GET']) # When someone visits /health using the GET method, call health()
def health():
    return jsonify({"status": "ML service is running!"})

if __name__ == "__main__":
    app.run(port=5000)