from flask import Flask

app = Flask(__name__)

@app.route('/coffe')
def get_all_coffe():
    # get all the coffe reviews from the database
    # Serialize into JSON-format
    return # JSON file.


@app.route('/<profile_id>/reviews')
def get_profile_reviews(profile_id):
    pass


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)