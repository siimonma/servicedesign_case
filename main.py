from flask import Flask,request
from case_project.databases.coffe_review_db import CoffeReviewDB
import json

app = Flask(__name__)
coffeReviewDB = CoffeReviewDB()

@app.route('/coffe')
def get_all_coffe():
    # get all the coffe reviews from the database
    # Serialize into JSON-format
    return # JSON file.


@app.route('/<profile_id>/reviews')
def get_profile_reviews(profile_id):
    reviews = coffeReviewDB.get_user_review(profile_id)
    return reviews

@app.route('/register', methods=['POST'])
def register_user():
    name = request.args['name']
    email = request.args['email']

    # token = create_token()


# URL-form /auth
@app.route('/auth')
def login_user():
    pass


if __name__ == '__main__':
    print(get_profile_reviews(2))
    app.run(host="0.0.0.0", port=5000, debug=True)