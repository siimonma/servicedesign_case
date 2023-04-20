from flask import Flask

app = Flask(__name__)

@app.route('/coffe')
def all_coffe():
    # get all the coffe reviews from the database
    # Serialize into JSON-format
    return # JSON file.


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)